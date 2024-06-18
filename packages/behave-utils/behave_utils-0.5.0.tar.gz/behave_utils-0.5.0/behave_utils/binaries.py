#  Copyright 2021-2023  Dominik Sekotill <dom.sekotill@kodo.org.uk>
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Start and manage a test Kubernetes cluster with Kubernetes-in-Docker (kind)
"""

from __future__ import annotations

import platform
import re
from abc import ABC
from abc import abstractmethod
from collections.abc import Iterator
from io import BytesIO
from pathlib import Path
from shutil import copyfileobj
from tarfile import TarFile
from typing import IO

import requests
import xdg
from packaging.version import Version

from behave_utils.json import JSONObject
from behave_utils.url import URL

CACHE_DIR: Path = xdg.xdg_cache_home() / "behave-testing"


class DownloadableExecutable(ABC):
	"""
	Base class for downloading static binaries to local paths

	Subclasses should implement `get_latest` and `get_stream` methods.  They may use the
	"kernel", "arch" and "goarch" attributes to select the correct source for the current
	platform.

	Subclasses must also provide the "name" attribute, either as a class or instance
	attribute.  It is used to generate a cache path.

	Users of the subclasses SHOULD ONLY call the `get_binary` method to get a path pointing
	to a locally cached copy of the downloaded binary.
	"""

	# Map of `uname -m` output to architecture values accepted by Go
	# Many Go binaries include the architecture value accepted by `go` in their names, so
	# the "goarch" class attribute is added for convenience, generated from this map.
	# This map may not be fully complete. Only non-equal values need to be added.
	GOARCH_MAP = {
		"i386": "386",
		"i686": "386",
		"x86": "386",

		"x86_64": "amd64",

		"armv6l": "arm",
		"armv7l": "arm",

		"aarch64": "arm64",
	}

	kernel = platform.system().lower()
	arch = platform.machine()
	goarch = GOARCH_MAP.get(arch, arch)

	name: str

	def __init__(self, version: str = "latest"):
		self.version = version

	@abstractmethod
	def get_latest(self, session: requests.Session) -> str:
		"""
		Return the latest release string for a supported binary

		Implementations must discover and return the latest release or tag string

		`session` is provided for performing HTTP requests.  Although its use is not
		required, it has and automatic code check hook so there is no need to manually check
		the return code and handle errors.
		"""
		raise NotImplementedError

	@abstractmethod
	def get_stream(self, session: requests.Session, version: str) -> IO[bytes]:
		"""
		Return a stream that emits the requested version of a supported binary

		Implementations must perform a request for the binary and return a file-like reader

		The return object must be a readable FileIO like instance, returning bytes.  If the
		source is uncompressed the "raw" attribute of a `requests.Response` object opened
		with `stream=True` will suffice.  See examples below.

		`version` specifies the wanted version of the binary, which MAY be different from
		the "version" instance attribute.  Other attributes such as "kernel" and "arch" (or
		"goarch" if appropriate) MUST be honoured when selecting a source.

		`session` is provided for performing HTTP requests.  Although its use is not
		required, it has and automatic code check hook so there is no need to manually check
		the return code and handle errors.


		Examples:

		1) Get an uncompressed binary:

		>>> def get_stream(session: requests.Session, version: str) -> IO[bytes]:
		...     url = "https://example.com/binary"
		...     return session.get(url, stream=True).raw


		2) Get a binary from a GZip compressed tar archive, storing the tar file in memory:

		Note: Avoid this for very large downloads. Unfortunately the Python tarfile
		implementation cannot handle non-seekable streams.

		>>> from tarfile import TarFile

		>>> def get_stream(session: requests.Session, version: str) -> IO[bytes]:
		...     url = "https://example.com/binary.tar.gz"
		...     buf = BytesIO(session.get(url).content)
		...     tar = TarFile.gzopen("buffer", fileobj=buf)
		...     return tar.extractfile(self.name)


		3) Get a binary from a GZip compressed tar archive, storing the tar file in the file
		system:

		>>> from tarfile import TarFile
		>>> from tempfile import TemporaryFile
		>>> from shutil import copyfileobj

		>>> def get_stream(session: requests.Session, version: str) -> IO[bytes]:
		...     url = "https://example.com/binary.tar.gz"
		...     resp = session.get(url, stream=True)
		...     temp = TemporaryFile()
		...     copyfileobj(resp.raw, temp)
		...     tar = TarFile.gzopen("buffer", fileobj=temp)
		...     return tar.extractfile(self.name)
		"""
		raise NotImplementedError

	def get_binary(self) -> Path:
		"""
		Return a Path to a locally cached executable, downloading it if necessary
		"""
		CACHE_DIR.mkdir(0o775, True, True)
		version = self.version

		with requests.Session() as session:
			assert isinstance(session.hooks["response"], list)
			session.hooks["response"].append(lambda r, *a, **k: r.raise_for_status())

			if version == "latest":
				version = self.get_latest(session)

			binary = CACHE_DIR / f"{self.name}-{version}-{self.kernel}-{self.arch}"
			if binary.exists():
				return binary

			stream = self.get_stream(session, version)

			try:
				with binary.open("wb") as f:
					copyfileobj(stream, f)
			except BaseException:
				binary.unlink()
				raise
			binary.chmod(0o755)

		return binary


class DownloadableDocker(DownloadableExecutable):
	"""
	Download class for the Docker client binary
	"""

	URL = "https://download.docker.com/{kernel}/static/stable/{arch}/docker-{version}.tgz"
	LATEST_URL = "https://download.docker.com/{kernel}/static/stable/{arch}/"
	VERSION_RE = re.compile(rb'href="docker-(?P<release>[0-9.]+).tgz"')

	name = "docker"

	def get_latest(self, session: requests.Session) -> str:
		"""
		Return latest Docker release
		"""
		url = self.LATEST_URL.format(kernel=self.kernel, arch=self.arch)
		doc = session.get(url).content
		latest = max(self._extract_versions(doc))
		return str(latest)

	def get_stream(self, session: requests.Session, version: str) -> IO[bytes]:
		"""
		Return a stream that emits theDocker CLI binary
		"""
		url = self.URL.format(version=version, kernel=self.kernel, arch=self.arch)
		buf = BytesIO(session.get(url).content)
		tar = TarFile.gzopen("buffer", fileobj=buf)
		stream = tar.extractfile("docker/docker")
		if stream is None:
			raise FileNotFoundError(f"'docker/docker' in {url}")
		return stream

	@classmethod
	def _extract_versions(cls, doc: bytes) -> Iterator[Version]:
		for match in cls.VERSION_RE.finditer(doc):
			yield Version(match.group("release").decode())


class DownloadableKubeTools(DownloadableExecutable):
	"""
	Download class for the kubernetes binaries "kubectl", "kubelet" and "kubeadm"
	"""

	URL = "https://dl.k8s.io/release/{version}/bin/{kernel}/{arch}/{name}"
	LATEST_URL = "https://dl.k8s.io/release/stable.txt"

	def __init__(self, name: str, version: str = "latest"):
		DownloadableExecutable.__init__(self, version)
		self.name = name
		self._latest = ""

	def get_latest(self, session: requests.Session) -> str:
		"""
		Return that latest release of Kubernetes
		"""
		if not self._latest:
			self._latest = session.get(self.LATEST_URL).content.decode().strip()
		return self._latest

	def get_stream(self, session: requests.Session, version: str) -> IO[bytes]:
		"""
		Return a stream that emits the requested Kubernetes binary
		"""
		url = self.URL.format(version=version, kernel=self.kernel, arch=self.goarch, name=self.name)
		stream: IO[bytes] = session.get(url, stream=True).raw
		return stream


class DownloadableCrictl(DownloadableExecutable):
	"""
	Download class for the "crictl" binary
	"""

	URL = "https://github.com/kubernetes-sigs/cri-tools/releases/download/{version}/crictl-{version}-{kernel}-{arch}.tar.gz"
	LATEST_URL = "https://api.github.com/repos/kubernetes-sigs/cri-tools/releases/latest"

	name = "cri"

	def get_latest(self, session: requests.Session) -> str:
		"""
		Return the latest "crictl" release
		"""
		json = JSONObject.from_string(session.get(self.LATEST_URL).content)
		return json.path("$.name", str).replace("cri-tools ", "")

	def get_stream(self, session: requests.Session, version: str) -> IO[bytes]:
		"""
		Return a stream that emits the requested "crictl" binary
		"""
		url = self.URL.format(version=version, kernel=self.kernel, arch=self.goarch)
		buf = BytesIO(session.get(url).content)
		tar = TarFile.gzopen("buffer", fileobj=buf)
		stream = tar.extractfile("crictl")
		if stream is None:
			raise FileNotFoundError(f"'crictl' in {url}")
		return stream


class DownloadableKind(DownloadableExecutable):
	"""
	Download class for the "kind" (Kubernetes-in-Docker) binary
	"""

	URL = "https://kind.sigs.k8s.io/dl/{version}/kind-{kernel}-{arch}"
	LATEST_URL = "https://api.github.com/repos/kubernetes-sigs/kind/releases/latest"

	name = "kind"

	def get_latest(self, session: requests.Session) -> str:
		"""
		Return the latest Kind binary
		"""
		json = JSONObject.from_string(session.get(self.LATEST_URL).content)
		return json.path("$.name", str)

	def get_stream(self, session: requests.Session, version: str) -> IO[bytes]:
		"""
		Return a stream that emits the requested Kind binary
		"""
		url = self.URL.format(version=version, kernel=self.kernel, arch=self.goarch)
		stream: IO[bytes] = session.get(url, stream=True).raw
		return stream
