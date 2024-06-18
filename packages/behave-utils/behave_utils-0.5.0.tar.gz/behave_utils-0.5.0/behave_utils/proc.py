#  Copyright 2021-2023  Dominik Sekotill <dom.sekotill@kodo.org.uk>
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Manage processes asynchronously with stdio capture
"""

from __future__ import annotations

import io
import sys
from collections.abc import Callable
from collections.abc import Iterator
from collections.abc import MutableMapping
from collections.abc import MutableSequence
from collections.abc import Sequence
from copy import copy
from functools import partial
from os import PathLike
from os import fspath
from os import write as fdwrite
from subprocess import DEVNULL
from subprocess import PIPE
from subprocess import CalledProcessError
from typing import IO
from typing import TYPE_CHECKING
from typing import Any
from typing import BinaryIO
from typing import Literal
from typing import SupportsBytes
from typing import TextIO
from typing import TypeVar
from typing import Union
from typing import overload
from warnings import warn

import trio.abc

if TYPE_CHECKING:
	from typing_extensions import Self

T = TypeVar('T')
Deserialiser = Callable[[memoryview], T]

Argument = Union[str, bytes, PathLike[str], PathLike[bytes]]
PathArg = Argument  # deprecated
Arguments = Sequence[Argument]
MutableArguments = MutableSequence[Argument]
Environ = MutableMapping[str, str]


def coerce_args(args: Arguments) -> Iterator[str]:
	"""
	Ensure path-like arguments are converted to strings
	"""
	for arg in args:
		arg = fspath(arg)
		yield arg if isinstance(arg, str) else arg.decode()


@overload
def exec_io(
	cmd: Arguments, *,
	input: bytes = b'',
	deserialiser: Deserialiser[T],
	**kwargs: Any,
) -> T: ...


@overload
def exec_io(
	cmd: Arguments, *,
	input: bytes = b'',
	deserialiser: None = None,
	**kwargs: Any,
) -> int: ...


def exec_io(
	cmd: Arguments, *,
	input: bytes = b'',
	deserialiser: Deserialiser[Any]|None = None,
	**kwargs: Any,
) -> Any:
	"""
	Execute a command, handling output asynchronously

	If input is provided it will be fed to the process' stdin.
	If a deserialiser is provided it will be used to parse stdout data from the process.

	Stderr and stdout (if no deserialiser is provided) will be written to `sys.stderr` and
	`sys.stdout` respectively.

	Note that the data is written, not redirected.  If either `sys.stdout` or `sys.stderr`
	is changed to an IO-like object with no file descriptor, this will still work.
	"""
	if deserialiser and 'stdout' in kwargs:
		raise TypeError("Cannot provide 'deserialiser' with 'stdout' argument")
	if "data" in kwargs:
		if input:
			raise TypeError("both 'input' and the deprecated 'data' keywords provided")
		warn(DeprecationWarning("the 'data' keyword argument is deprecated, use 'input'"))
		input = kwargs.pop("data")
	if input and 'stdin' in kwargs:
		raise TypeError("Cannot provide 'input' with 'stdin' argument")
	stdout: IO[str]|IO[bytes]|int = io.BytesIO() if deserialiser else kwargs.pop('stdout', sys.stdout)
	stderr: IO[str]|IO[bytes]|int = kwargs.pop('stderr', sys.stderr)
	proc = trio.run(_exec_io, cmd, input, stdout, stderr, kwargs)
	if deserialiser:
		assert isinstance(stdout, io.BytesIO)
		return deserialiser(stdout.getbuffer())
	return proc.returncode


@overload
async def aexec_io(
	cmd: Arguments, *,
	input: bytes = b'',
	deserialiser: Deserialiser[T],
	**kwargs: Any,
) -> T: ...


@overload
async def aexec_io(
	cmd: Arguments, *,
	input: bytes = b'',
	deserialiser: None = None,
	**kwargs: Any,
) -> int: ...


async def aexec_io(
	cmd: Arguments, *,
	input: bytes = b"",
	deserialiser: Deserialiser[Any]|None = None,
	**kwargs: Any,
) -> Any:
	"""
	Execute a command asynchronously, handling writing output to sys.stdout and sys.stderr

	If input is provided it will be fed to the process' stdin.
	If a deserialiser is provided it will be used to parse stdout data from the process.

	Stderr and stdout (if no deserialiser is provided) will be written to `sys.stderr` and
	`sys.stdout` respectively.

	Note that the data is written, not redirected.  If either `sys.stdout` or `sys.stderr`
	is changed to an IO-like object with no file descriptor, this will still work.
	"""
	if deserialiser and 'stdout' in kwargs:
		raise TypeError("Cannot provide 'deserialiser' with 'stdout' argument")
	if input and 'stdin' in kwargs:
		raise TypeError("Cannot provide 'input' with 'stdin' argument")
	stdout: IO[str]|IO[bytes]|int = io.BytesIO() if deserialiser else kwargs.pop('stdout', sys.stdout)
	stderr: IO[str]|IO[bytes]|int = kwargs.pop('stderr', sys.stderr)
	proc = await _exec_io(cmd, input, stdout, stderr, kwargs)
	if deserialiser:
		assert isinstance(stdout, io.BytesIO)
		return deserialiser(stdout.getbuffer())
	return proc.returncode


async def _exec_io(
	cmd: Arguments,
	data: bytes,
	stdout: IO[str]|IO[bytes]|int,
	stderr: IO[str]|IO[bytes]|int,
	kwargs: dict[str, Any],
) -> trio.Process:
	async with trio.open_nursery() as nursery:
		stdin = kwargs.pop('stdin') if 'stdin' in kwargs else PIPE if data else DEVNULL
		proc: trio.Process = await nursery.start(
			partial(
				trio.run_process, [*coerce_args(cmd)],
				stdin=stdin,
				stdout=PIPE, stderr=PIPE,
				check=False,
				**kwargs,
			),
		)
		assert proc.stdout is not None and proc.stderr is not None
		nursery.start_soon(_passthru, proc.stderr, stderr)
		nursery.start_soon(_passthru, proc.stdout, stdout)
		if data:
			assert proc.stdin is not None
			async with proc.stdin as stdin:
				await stdin.send_all(data)
	return proc


async def _passthru(in_stream: trio.abc.ReceiveStream, out_stream: IO[str]|IO[bytes]|int) -> None:
	try:
		if not isinstance(out_stream, int):
			out_stream = out_stream.fileno()
	except (OSError, AttributeError):
		# cannot get file descriptor, probably a memory buffer
		if isinstance(out_stream, (BinaryIO, io.BytesIO)):
			async def write(data: bytes) -> None:
				assert isinstance(out_stream, (BinaryIO, io.BytesIO))
				out_stream.write(data)
		else:
			async def write(data: bytes) -> None:
				assert isinstance(out_stream, (TextIO, io.StringIO))
				out_stream.write(data.decode())
	else:
		# is/has a file descriptor, out_stream is now that file descriptor
		async def write(data: bytes) -> None:
			assert isinstance(out_stream, int)
			data = memoryview(data)
			remaining = len(data)
			while remaining:
				await trio.lowlevel.wait_writable(out_stream)
				written = fdwrite(out_stream, data)
				data = data[written:]
				remaining -= written

	while True:
		data = await in_stream.receive_some()
		if not data:
			return
		await write(data)


class _ExecutorBase(list[Argument]):

	def __init__(self, *cmd: Argument):
		self[:] = cmd

	def get_arguments(
		self,
		cmd: Arguments,
		kwargs: MutableMapping[str, Any],
		has_input: bool,
		is_query: bool,
		deserialiser: Deserialiser[Any]|None,
	) -> Arguments:
		"""
		Override to amend command arguments and kwargs for exec_io() prior to execution
		"""
		return cmd

	def subcommand(self, *args: Argument) -> Self:
		"""
		Return a new Executor instance of the same class with additional arguments appended

		The returned instance is created as a shallow copy; if attribute values need to be
		copied, subclasses must implement __copy__().
		(see https://docs.python.org/3/library/copy.html)
		"""
		new = copy(self)
		new.extend(args)
		return new


class Executor(_ExecutorBase):
	"""
	Manage calling executables with composable argument lists

	Subclasses may add or amend the argument list just prior to execution by implementing
	`get_arguments`.

	Any arguments passed to the constructor will prefix the arguments passed when the object
	is called.
	"""

	@overload
	def __call__(
		self,
		*args: Argument,
		input: str|bytes|SupportsBytes|None = ...,
		deserialiser: Deserialiser[T],
		query: Literal[False] = False,
		**kwargs: Any,
	) -> T: ...

	@overload
	def __call__(
		self,
		*args: Argument,
		input: str|bytes|SupportsBytes|None = ...,
		deserialiser: None = None,
		query: Literal[True],
		**kwargs: Any,
	) -> int: ...

	@overload
	def __call__(
		self,
		*args: Argument,
		input: str|bytes|SupportsBytes|None = ...,
		deserialiser: None = None,
		query: Literal[False] = False,
		**kwargs: Any,
	) -> None: ...

	def __call__(
		self,
		*args: Argument,
		input: str|bytes|SupportsBytes|None = None,
		deserialiser: Deserialiser[Any]|None = None,
		query: bool = False,
		**kwargs: Any,
	) -> Any:
		"""
		Execute the configure command with the given arguments

		Input:
			Any bytes passed as "input" will be fed into the process' stdin pipe.

		Output:
			If "deserialiser" is provided it will be called with a memoryview of a buffer
			containing any bytes from the process' stdout; whatever is returned by
			"deserialiser" will be returned.

			If "query" is true the return code of the process will be returned.

			Otherwise nothing is returned.

			Note that "deserialiser" and "query" are mutually exclusive; if debugging is
			enabled an AssertionError will be raised if both are non-None/non-False, otherwise
			"query" is ignored.

		Errors:
			If "query" is not true any non-zero return code will cause CalledProcessError to
			be raised.
		"""
		assert not deserialiser or not query

		# Check interferes with query, simulate it not being accepted
		if "check" in kwargs:
			raise TypeError(
				f"{self.__class__.__name__}.__call__() got an unexpected keyword "
				"argument 'check'",
			)

		data = (
			b"" if input is None else
			input.encode() if isinstance(input, str) else
			bytes(input)
		)
		cmd = self.get_arguments(
			[*self, *args], kwargs,
			has_input=bool(data),
			is_query=query,
			deserialiser=deserialiser,
		)

		if deserialiser:
			return exec_io(cmd, input=data, deserialiser=deserialiser, **kwargs)

		rcode = exec_io(cmd, input=data, **kwargs)
		if query:
			return rcode
		if 0 != rcode:
			raise CalledProcessError(rcode, ' '.join(coerce_args(cmd)))
		return None


class AsyncExecutor(_ExecutorBase):
	"""
	An asynchronous variant of `Executor`; when called it returns an awaitable coroutine
	"""

	@overload
	async def __call__(
		self,
		*args: Argument,
		input: str|bytes|SupportsBytes|None = ...,
		deserialiser: Deserialiser[T],
		query: Literal[False] = False,
		**kwargs: Any,
	) -> T: ...

	@overload
	async def __call__(
		self,
		*args: Argument,
		input: str|bytes|SupportsBytes|None = ...,
		deserialiser: None = None,
		query: Literal[True],
		**kwargs: Any,
	) -> int: ...

	@overload
	async def __call__(
		self,
		*args: Argument,
		input: str|bytes|SupportsBytes|None = ...,
		deserialiser: None = None,
		query: Literal[False] = False,
		**kwargs: Any,
	) -> None: ...

	async def __call__(
		self,
		*args: Argument,
		input: str|bytes|SupportsBytes|None = None,
		deserialiser: Deserialiser[Any]|None = None,
		query: bool = False,
		**kwargs: Any,
	) -> Any:
		"""
		Execute the configure command with the given arguments

		Input:
			Any bytes passed as "input" will be fed into the process' stdin pipe.

		Output:
			If "deserialiser" is provided it will be called with a memoryview of a buffer
			containing any bytes from the process' stdout; whatever is returned by
			"deserialiser" will be returned.

			If "query" is true the return code of the process will be returned.

			Otherwise nothing is returned.

			Note that "deserialiser" and "query" are mutually exclusive; if debugging is
			enabled an AssertionError will be raised if both are non-None/non-False, otherwise
			"query" is ignored.

		Errors:
			If "query" is not true any non-zero return code will cause CalledProcessError to
			be raised.
		"""
		assert not deserialiser or not query

		data = (
			b"" if input is None else
			input.encode() if isinstance(input, str) else
			bytes(input)
		)
		cmd = self.get_arguments(
			[*self, *args], kwargs,
			has_input=bool(data),
			is_query=query,
			deserialiser=deserialiser,
		)

		if deserialiser:
			return await aexec_io(cmd, input=data, deserialiser=deserialiser, **kwargs)

		rcode = await aexec_io(cmd, input=data, **kwargs)
		if query:
			return rcode
		if 0 != rcode:
			raise CalledProcessError(rcode, ' '.join(coerce_args(cmd)))
		return None
