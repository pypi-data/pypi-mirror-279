from collections.abc import Callable
from typing import Iterator
from typing import TypeVar
from typing import overload

from typing_extensions import Concatenate
from typing_extensions import ParamSpec

from .runner import Context

ContextT = TypeVar("ContextT", bound=Context, contravariant=True)
ReturnT = TypeVar("ReturnT", covariant=True)
Params = ParamSpec("Params")


@overload
def use_fixture(
	fixture_func: Callable[Concatenate[ContextT, Params], Iterator[ReturnT]],
	context: ContextT,
	*args: Params.args,
	**kwargs: Params.kwargs,
) -> ReturnT: ...

@overload
def use_fixture(
	fixture_func: Callable[Concatenate[ContextT, Params], ReturnT],
	context: ContextT,
	*args: Params.args,
	**kwargs: Params.kwargs,
) -> ReturnT: ...


@overload
def fixture(
	func: Callable[Params, ReturnT],
	name: str = ...,
	pattern: str = ...,
) -> Callable[Params, ReturnT]: ...

@overload
def fixture(
	name: str = ...,
	pattern: str = ...,
) -> Callable[[Callable[Params, ReturnT]], Callable[Params, ReturnT]]: ...
