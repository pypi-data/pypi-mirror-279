#  Copyright 2021-2024  Dominik Sekotill <dom.sekotill@kodo.org.uk>
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Management and control for MySQL database fixtures
"""

from __future__ import annotations

import atexit
from collections.abc import Iterator
from collections.abc import Sequence
from importlib import resources
from os import environ
from pathlib import Path
from time import sleep
from typing import TYPE_CHECKING
from typing import ClassVar

from behave import fixture

from .docker import Cli
from .docker import Container
from .docker import Image
from .docker import Mount
from .docker import Network
from .docker import inspect
from .secret import make_secret
from .utils import wait

if TYPE_CHECKING:
	from behave.runner import FeatureContext
	from typing_extensions import Self


INIT_DIRECTORY = Path("/docker-entrypoint-initdb.d")


class MysqlContainer(Container):
	"""
	Container subclass for a database container
	"""

	_inst: ClassVar[Self|None] = None

	def __init__(
		self,
		version: str = "latest",
		init_files: Sequence[Path] = [],
	):
		volumes: list[Mount] = [(path, INIT_DIRECTORY / path.name) for path in init_files]
		volumes.append(Path("/var/lib/mysql"))
		Container.__init__(
			self,
			Image.pull(f"mysql/mysql-server:{version}"),
			volumes=volumes,
		)

	@classmethod
	def get_running(cls, version: str = "latest") -> MysqlContainer:
		"""
		Return a running instance of MysqlContainer

		Depending on what is currently running the container may have to be started, which
		is a long operation.
		"""
		if (inst := cls._inst or cls.get_labeled(version)):
			return inst
		with resources.path(__package__, "init.sql") as init:
			cls._inst = self = cls(version, [init])
			self.start()
			sleep(20)
			if environ.get("BEHAVE_UTILS_MYSQL_KEEP", "0") == "0":
				atexit.register(self.stop, rm=True)
			wait(lambda: self.run(['/healthcheck.sh']).returncode == 0, timeout=240)
			return self

	@classmethod
	def get_labeled(cls, version: str) -> Self|None:
		"""
		Return any existing running container matching the given version

		This method will clean up stopped or out-of-date containers. A container is
		considered out-of-date if it is labeled with the requested version but has
		a different SHA-ID to the image available on Docker Hub tagged with that version.
		"""
		# cls._inst = ...


class Mysql:
	"""
	A database instance for test fixtures' use

	If created with a non-`None` 'server' it MUST be a *running* Container instance or
	`ValueError` will be raised.

	If 'server' is `None` a running MysqlContainer instance will be retrieved or created
	using the value of 'version' as a MySQL image tag.
	"""

	def __init__(
		self, *,
		version: str = "latest",
		network: Network|None = None,
		server: Container|None = None,
	):
		if server and not server.is_running():
			raise ValueError(f"{server} is not running")
		self._server = server or MysqlContainer.get_running(version)
		self._network = network

		self.name = f"behave-{make_secret(5)}"
		self.user = f"behave-user-{make_secret(5)}"
		self.password = make_secret(20)

	def __enter__(self) -> Self:
		if self._network:
			self._server.connect(self._network)
		self._server.run(
			["mysql"],
			input=f"""
			CREATE DATABASE IF NOT EXISTS `{self.name}`;
			CREATE USER IF NOT EXISTS '{self.user}'@'%'
			  IDENTIFIED BY '{self.password}';
			GRANT ALL ON TABLE `{self.name}`.* TO '{self.user}'@'%';
			""".encode("utf-8"),
			check=True,
		)
		return self

	def __exit__(self, *exc_info: object) -> None:
		if self._network:
			self._server.disconnect(self._network)
		self._server.run(
			["mysql"],
			input=f"""
			DROP USER '{self.user}'@'%';
			DROP DATABASE `{self.name}`;
			""".encode("utf-8"),
		)

	def get_location(self) -> str:
		"""
		Return a "host:port" string for connecting to the database from other containers
		"""
		host = inspect(self._server).path("$.Config.Hostname", str)
		return f"{host}:3306"

	def run_commands(self, sql: str|Path) -> None:
		"""
		Run SQL commands as the superuser on the database, from either strings or files

		This is mostly intended for initialising database fixtures with data.
		"""
		if isinstance(sql, str):
			self.mysql(input=sql, check=True)
			return
		with sql.open("rb") as fh:
			self.mysql(stdin=fh, check=True)

	@property
	def mysql(self) -> Cli:
		"""
		Run "mysql" commands
		"""
		return Cli(self._server, "mysql", self.name)

	@property
	def mysqladmin(self) -> Cli:
		"""
		Run "mysqladmin" commands
		"""
		return Cli(self._server, "mysqladmin", self.name)

	@property
	def mysqldump(self) -> Cli:
		"""
		Run "mysqldump" commands
		"""
		return Cli(self._server, "mysqldump", self.name)


@fixture
def snapshot_rollback(context: FeatureContext, /, database: Mysql) -> Iterator[None]:
	"""
	Manage the state of a database as a revertible fixture

	At the end of the fixture's lifetime it's state at the beginning is restored.  This
	allows for faster fixture turn-around than restarting the database.
	"""
	snapshot = database.mysqldump(deserialiser=bytes)
	yield
	database.mysql(input=snapshot)
