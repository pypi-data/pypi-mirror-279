#  Copyright 2021-2024  Dominik Sekotill <dom.sekotill@kodo.org.uk>
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Commands for managing Docker for fixtures
"""

from __future__ import annotations

import codecs
import hashlib
import ipaddress
import json
import logging
from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import MutableMapping
from collections.abc import MutableSequence
from contextlib import contextmanager
from enum import Enum
from os import PathLike
from os import environ
from os import fspath
from pathlib import Path
from secrets import token_hex
from shutil import which
from subprocess import DEVNULL
from subprocess import PIPE
from subprocess import CalledProcessError
from subprocess import CompletedProcess
from subprocess import Popen
from subprocess import run
from types import TracebackType
from typing import IO
from typing import TYPE_CHECKING
from typing import Any
from typing import NewType
from typing import Protocol
from typing import Union
from typing import cast
from urllib.parse import urlparse

from .binaries import DownloadableDocker
from .json import JSONArray
from .json import JSONObject
from .proc import Argument
from .proc import Arguments
from .proc import Deserialiser
from .proc import Environ
from .proc import Executor
from .proc import MutableArguments
from .proc import exec_io
from .utils import wait

if TYPE_CHECKING:
	from typing_extensions import Self

LOCALHOST = ipaddress.IPv4Address(0x7f000001)

ShaID = NewType("ShaID", str)

MountPath = Union[PathLike[bytes], PathLike[str]]
HostMount = tuple[MountPath, MountPath]
NamedMount = tuple[str, MountPath]
Mount = Union[HostMount, NamedMount, MountPath]
Volumes = MutableSequence[Mount]

IPAddress = Union[ipaddress.IPv4Address, ipaddress.IPv6Address]

DOCKER: Argument
match which("docker"):
	case None:
		DOCKER = DownloadableDocker().get_binary()
	case str(path):
		DOCKER = Path(path)


def utf8_decode(buffer: bytes) -> str:
	"""
	Return a decoded string from a bytes-like sequence of bytes
	"""
	return codecs.getdecoder("utf-8")(buffer)[0]


def docker(*args: Argument, **env: str) -> None:
	"""
	Run a Docker command, with output going to stdout
	"""
	run([DOCKER, *args], env={**environ, **env}, check=True)


def docker_output(*args: Argument, **env: str) -> str:
	"""
	Run a Docker command, capturing and returning its stdout
	"""
	proc = run([DOCKER, *args], env={**environ, **env}, check=True, stdout=PIPE, text=True)
	return proc.stdout.strip()


def docker_quiet(*args: Argument, **env: str) -> None:
	"""
	Run a Docker command, directing its stdout to /dev/null
	"""
	run([DOCKER, *args], env={**environ, **env}, check=True, stdout=DEVNULL)


def inspect(item: DockerItem|str) -> JSONObject:
	"""
	Get the result of inspecting a Docker item instance, or string identifier
	"""
	if not isinstance(item, str):
		item = item.get_id()
	with Popen([DOCKER, 'inspect', item], stdout=PIPE) as proc:
		assert proc.stdout is not None
		results = json.load(proc.stdout)
	assert isinstance(results, list)
	assert len(results) == 1 and isinstance(results[0], dict)
	return JSONObject(results[0])


def _get_docker_host_ip() -> IPAddress:
	"""
	Return an IP address from the DOCKER_HOST environment variable, or a loopback address

	This function is *far* from complete, and there needs to be a much better way of
	accessing ports on the Docker host.

	Currently, only IP addresses are supported, not names.
	"""
	url = environ.get("DOCKER_HOST")
	if url is None:
		return LOCALHOST
	if not "://" in url:
		url = f"tcp://{url}"
	purl = urlparse(url)
	if not purl.hostname or purl.scheme not in ("tcp", "ssh"):
		return LOCALHOST
	return ipaddress.ip_address(purl.hostname)


def _hash_cmd(cmd: Arguments) -> str:
	hash = hashlib.sha256()
	for arg in cmd:
		arg = fspath(arg)
		hash.update(arg.encode("utf-8") if isinstance(arg, str) else arg)
	return f"@cmd:{hash.hexdigest()}"


class IPv4Address(ipaddress.IPv4Address):
	"""
	Subclass of IPv4Address that handle's docker idiosyncratic tendency to add a mask suffix
	"""

	@classmethod
	def with_suffix(cls, address: str) -> Self:
		"""
		Construct an instance with a suffixed bitmask size
		"""
		address, *_ = address.partition("/")
		return cls(address)


class IPProtocol(Enum):
	"""
	IP protocols supported by Docker port forwarding
	"""

	TCP = 'tcp'
	UDP = 'udp'


class DockerItem(Protocol):
	"""
	Protocol for all Docker item classes
	"""

	def get_id(self) -> ShaID:
		"""
		Return an identifier for the Docker item
		"""


class Image:
	"""
	Docker image items
	"""

	_cache = dict[str, ShaID]()

	def __init__(self, iid: ShaID):
		self.iid = iid

	@classmethod
	def build(cls, context: Path, target: str = "", **build_args: str|None) -> Self:
		"""
		Build an image from the given context

		Build arguments are ignored if they are None to make it easier to supply (or not)
		arguments from external lookups without complex argument composing.
		"""
		cmd: Arguments = [
			b"build", context, f"--target={target}",
			*(f"--build-arg={arg}={val}" for arg, val in build_args.items() if val is not None),
		]
		key = _hash_cmd(cmd)
		try:
			iid = cls._cache[key]
		except KeyError:
			docker(*cmd, DOCKER_BUILDKIT='1')
			iid = ShaID(docker_output(*cmd, '-q', DOCKER_BUILDKIT='1'))
			cls._cache[key] = iid
		return cls(iid)

	@classmethod
	def pull(cls, repository: str) -> Self:
		"""
		Pull an image from a registry
		"""
		try:
			iid = cls._cache[repository]
		except KeyError:
			docker(b"pull", repository)
			iid = cls._process_image(repository)
		return cls(iid)

	@classmethod
	def _process_image(cls, reference: str) -> ShaID:
		report = inspect(reference)
		iid = report.path("$.Id", str, ShaID)
		cls._cache.update(
			((tag, iid) for tag in report.path("$.RepoTags", list[str])),
			reference=iid,
		)
		return iid

	def get_id(self) -> ShaID:
		"""
		Return an identifier for the Docker Image
		"""
		return self.iid


class Container:
	"""
	Docker container items

	Instances can be used as context managers that ensure the container is stopped on
	exiting the context.
	"""

	DEFAULT_ALIASES = tuple[str]()

	def __init__(
		self,
		image: Image,
		cmd: Arguments = [], *,
		volumes: Volumes = [],
		env: Environ = {},
		network: Network|None = None,
		entrypoint: HostMount|Argument|None = None,
		privileged: bool = False,
		publish: bool|list[int] = False,
	):
		if isinstance(entrypoint, tuple):
			volumes = [*volumes, entrypoint]
			entrypoint = entrypoint[1]

		self.image = image
		self.cmd = cmd
		self.volumes = volumes
		self.env = env
		self.entrypoint = entrypoint
		self.privileged = privileged
		self.publish = publish
		self.networks = dict[Network, tuple[IPAddress, tuple[str, ...]]]()
		self.cid: ShaID|None = None

		if network:
			self.connect(network, *self.DEFAULT_ALIASES)

	def __enter__(self) -> Self:
		return self

	def __exit__(self, etype: type[BaseException], exc: BaseException, tb: TracebackType) -> None:
		try:
			if self.cid and exc:
				self.show_logs()
			self.stop(rm=True)
		except Exception:
			logging.getLogger(__name__).exception("ignoring exception while stopping")

	@contextmanager
	def started(self) -> Iterator[Self]:
		"""
		Return a context manager that ensures the container is started when the context is entered
		"""
		with self:
			self.start()
			wait(lambda: self.is_running(raise_on_exit=True))
			yield self

	def is_running(self, raise_on_exit: bool = False) -> bool:
		"""
		Return whether the container is running
		"""
		if self.cid is None:
			return False
		details = inspect(self)
		if details.path('$.State.Status', str) == 'exited':
			code = details.path('$.State.ExitCode', int)
			if code != 0:
				logging.getLogger(__name__).warning(
					f"container {self.cid} exited ({code})",
				)
			if raise_on_exit:
				cmd = details.path("$.Config.Entrypoint", list[str])
				cmd.extend(details.path("$.Config.Cmd", list[str]))
				raise CalledProcessError(code, cmd)
		return (
			self.cid is not None
			and details.path('$.State.Running', bool)
		)

	def get_id(self) -> ShaID:
		"""
		Return an identifier for the Docker Container
		"""
		if self.cid is not None:
			return self.cid

		opts: MutableArguments = [
			f"--env={name}={val}" for name, val in self.env.items()
		]

		for vol in self.volumes:
			if isinstance(vol, tuple):
				src = fspath(vol[0])
				dst = fspath(vol[1])
				if isinstance(src, bytes):
					src = src.decode()
				if isinstance(dst, bytes):
					dst = dst.decode()
				arg: Argument = f"{src}:{dst}"
			else:
				arg = vol
			opts.extend((b"--volume", arg))

		if self.entrypoint:
			opts.extend((b"--entrypoint", self.entrypoint))

		if self.privileged:
			opts.append(b"--privileged")

		if isinstance(self.publish, list):
			opts.extend(f"--publish={p}" for p in self.publish)
		elif self.publish:
			opts.append(b"--publish-all")
		else:
			opts.append(b"--network=none")

		self.cid = ShaID(
			docker_output(
				b"container", b"create",
				"--label", "uk.org.kodo.behave-utils",
				*opts, self.image.iid, *self.cmd,
			),
		)
		assert self.cid

		# Disconnect the "none" network specified as the starting network
		if not self.publish:
			docker_quiet(b"network", b"disconnect", b"none", self.cid)

		# Connect any pre-configured networks
		for network, (address, aliases) in self.networks.items():
			self._connect_network(self.cid, network, address, aliases)

		return self.cid

	def start(self) -> None:
		"""
		Start the container
		"""
		if self.is_running():
			return
		docker_quiet(b"container", b"start", self.get_id())
		assert inspect(self).path('$.State.Status', str) != 'created', \
			"please report this at https://code.kodo.org.uk/dom/behave-utils/-/issues/11"

	def stop(self, rm: bool = False) -> None:
		"""
		Stop the container
		"""
		if self.cid is None:
			return
		try:
			if self.is_running():
				docker_quiet(b"container", b"stop", self.cid)
		finally:
			if rm:
				docker_quiet(b"container", b"rm", self.cid)
				self.cid = None

	def connect(
		self,
		network: Network,
		*aliases: str,
		address: ipaddress.IPv4Address|ipaddress.IPv6Address|None = None,
	) -> None:
		"""
		Connect the container to a Docker network

		Any aliases supplied will be resolvable to the container by other containers on the
		network.
		"""
		if network in self.networks:
			if self.networks[network][1] == aliases:
				return
			if self.cid is not None:
				docker(b"network", b"disconnect", str(network), self.cid)

		if address is None:
			address = network.reserve_address()
		self.networks[network] = address, aliases

		if self.cid is not None:
			self._connect_network(self.cid, network, address, aliases)

	@staticmethod
	def _connect_network(
		contrid: str,
		network: Network,
		address: IPAddress,
		aliases: Iterable[str],
	) -> None:
		opts = [f'--alias={a}' for a in aliases]
		opts.append(
			f"--ip={address}" if isinstance(address, ipaddress.IPv4Address) else
			f"--ip6={address}",
		)
		docker(b"network", b"connect", *opts, str(network), contrid)

	def disconnect(self, network: Network) -> None:
		"""
		Disconnect the container from a Docker network

		Raises `KeyError` if the network was not connected to with `Container.connect()`.
		"""
		del self.networks[network]
		if self.cid is not None:
			docker(b"network", b"disconnect", str(network), self.cid)

	def show_logs(self) -> None:
		"""
		Print the container logs to stdout
		"""
		if self.cid:
			docker(b"logs", self.cid)

	def get_exec_args(self, cmd: Arguments, interactive: bool = False) -> MutableArguments:
		"""
		Return a full argument list for running "cmd" inside the container
		"""
		return [DOCKER, b"exec", *((b"-i",) if interactive else []), self.get_id(), *cmd]

	def run(
		self,
		cmd: Arguments,
		*,
		stdin: IO[Any]|int|None = None,
		stdout: IO[Any]|int|None = None,
		stderr: IO[Any]|int|None = None,
		capture_output: bool = False,
		check: bool = False,
		input: bytes|None = None,
		timeout: float|None = None,
	) -> CompletedProcess[bytes]:
		"""
		Run "cmd" to completion inside the container and return the result
		"""
		self.is_running(raise_on_exit=True)
		interactive = input is not None or stdin is not None
		return run(
			self.get_exec_args(cmd, interactive),
			stdin=stdin, stdout=stdout, stderr=stderr,
			capture_output=capture_output,
			check=check, timeout=timeout, input=input,
		)

	def exec(
		self,
		cmd: Arguments,
		*,
		stdin: IO[Any]|int|None = None,
		stdout: IO[Any]|int|None = None,
		stderr: IO[Any]|int|None = None,
	) -> Popen[bytes]:
		"""
		Execute "cmd" inside the container and return a process object once started
		"""
		return Popen(
			self.get_exec_args(cmd),
			stdin=stdin, stdout=stdout, stderr=stderr,
		)

	def get_external_ports(self, port: int, proto: IPProtocol = IPProtocol.TCP) -> Iterable[tuple[IPAddress, int]]:
		"""
		Yield (address, port) combinations exposed on the host that map to the given container port
		"""
		name = f"{port}/{proto.name.lower()}"
		ports = inspect(self).path(
			f"$.NetworkSettings.Ports.{name}",
			list[dict[str, str]],
		)
		if not ports:
			raise KeyError(f"port {name} has not been published")
		for portd in ports:
			addr = ipaddress.ip_address(portd["HostIp"])
			port = int(portd["HostPort"])
			yield (_get_docker_host_ip() if addr.is_unspecified else addr), port


class Network:
	"""
	A Docker network
	"""

	DOCKER_SUBNET = ipaddress.IPv4Network("172.16.0.0/12")

	def __init__(self, name: str|None = None) -> None:
		self._name = name or f"br{token_hex(6)}"
		self._nid: ShaID|None = None
		self._assigned = set[ipaddress.IPv4Address]()

	def __str__(self) -> str:
		return self._name

	def __repr__(self) -> str:
		cls = type(self)
		return f"<{cls.__module__}.{cls.__name__} {self._name}>"

	def __eq__(self, other: Any) -> bool:
		if not isinstance(other, Network):
			return self._name == str(other)
		return self._name == other._name

	def __hash__(self) -> int:
		return self._name.__hash__()

	def __enter__(self) -> Network:
		self.create()
		return self

	def __exit__(self, etype: type[BaseException], exc: BaseException, tb: TracebackType) -> None:
		try:
			self.destroy()
		except CalledProcessError:
			logging.getLogger(__name__).error(f"network removal failed while stopping")
		except Exception:
			logging.getLogger(__name__).exception("ignoring exception while stopping")

	@property
	def name(self) -> str:
		"""
		Return the name of the Docker network
		"""
		return self._name

	def get_id(self) -> ShaID:
		"""
		Return an identifier for the Docker Network
		"""
		if self._nid is None:
			self.create()
		assert self._nid is not None
		return self._nid

	def create(self) -> None:
		"""
		Create the network
		"""
		subnet = self.get_free_subnet()
		gateway = next(subnet.hosts())
		try:
			self._nid = ShaID(
				docker_output(
					b"network", b"create", self._name,
					f"--subnet={subnet}", f"--gateway={gateway}",
				),
			)
		except CalledProcessError:
			data = exec_io(
				[DOCKER, b"network", b"inspect", self._name],
				deserialiser=JSONArray.from_string,
			)
			if len(data) == 0:
				raise
			self._nid = data.path("$[0].Id", str, ShaID)
			self._assigned.update(
				data.path(
					"$[0].IPAM.Config[*].Gateway",
					list[str], lambda ls: (IPv4Address(s) for s in ls),
				),
			)
		else:
			self._assigned.add(gateway)
		assert self._nid is not None
		assert len(self._assigned) > 0, \
			"Expected gateways address(es) to be added to assigned addresses set"

	def destroy(self) -> None:
		"""
		Remove the network
		"""
		if self._nid:
			docker_quiet(b"network", b"rm", self._nid)

	@classmethod
	def get_free_subnet(cls) -> ipaddress.IPv4Network:
		"""
		Return a free private subnet
		"""
		networks = exec_io(
			[DOCKER, b"network", b"ls", b"--format={{.ID}}"],
			deserialiser=utf8_decode,
		).splitlines()
		subnets = exec_io(
			[DOCKER, b"network", b"inspect"] + cast(list[Argument], networks),
			deserialiser=JSONArray.from_string,
		).path(
			"$[*].IPAM.Config[*].Subnet", list[str],
			lambda subnets: {ipaddress.ip_network(net) for net in subnets},
		)
		for subnet in cls.DOCKER_SUBNET.subnets(8):
			if not any(net.overlaps(subnet) for net in subnets):
				return subnet
		raise LookupError(f"No free subnets found in subnet {cls.DOCKER_SUBNET}")

	def reserve_address(self) -> ipaddress.IPv4Address:
		"""
		Return a free address in the network

		Note that the address is not reserved; any changes made to the network such as
		adding a container may invalidate the assurance that the address is free.
		"""
		# TODO: support IPv6
		data = inspect(self)
		# Considering only the first listed subnet
		net = data.path("$.IPAM.Config[0].Subnet", str, ipaddress.IPv4Network)

		# Recycle some old code for an assertion about assigned addresses
		if __debug__:
			reserved: set[ipaddress.IPv4Address] = data.path(
				"$.Containers.*.IPv4Address", list[str],
				lambda addrs: {IPv4Address.with_suffix(a) for a in addrs},
			)
			reserved.add(data.path("$.IPAM.Config[0].Gateway", str, IPv4Address))
			missing = reserved - self._assigned
			assert len(missing) == 0, f"Missing addresses from assigned set: {missing}"

		# Optimise for CPython 3.x without early binding
		assigned = self._assigned

		for addr in net.hosts():
			if addr not in assigned:
				assigned.add(addr)
				return addr
		raise LookupError(f"No free addresses found in subnet {net}")


class Cli(Executor):
	"""
	Manage calling executables in a container

	Any arguments passed to the constructor will prefix the arguments passed when the object
	is called.
	"""

	def __init__(self, container: Container, *cmd: Argument):
		Executor.__init__(self, *cmd)
		self.container = container

	def get_arguments(
		self,
		cmd: Arguments,
		kwargs: MutableMapping[str, Any],
		has_input: bool,
		is_query: bool,
		deserialiser: Deserialiser[Any]|None,
	) -> Arguments:
		"""
		Prefix the command arguments with a command necessary for executing in a container
		"""
		return self.container.get_exec_args(cmd, interactive=has_input)
