#  Copyright 2021, 2023  Dominik Sekotill <dom.sekotill@kodo.org.uk>
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
JSON classes for container types (objects and arrays)
"""

from __future__ import annotations

from collections.abc import Callable
from types import GenericAlias
from typing import TYPE_CHECKING
from typing import Any
from typing import TypeVar
from typing import overload

import orjson
from jsonpath import JSONPath

if TYPE_CHECKING:
	from typing_extensions import Self

__all__ = [
	"JSONObject",
	"JSONArray",
]


class JSONPathMixin:

	T = TypeVar('T', bound=object)
	C = TypeVar('C', bound=object)

	@overload
	def path(self, path: str, kind: type[T], convert: None = None) -> T: ...

	@overload
	def path(self, path: str, kind: type[T], convert: Callable[[T], C]) -> C: ...

	def path(self, path: str, kind: type[T]|GenericAlias, convert: Callable[[T], C]|None = None) -> T|C:
		result = JSONPath(path).parse(self)
		if "*" not in path:
			try:
				result = result[0]
			except IndexError:
				raise KeyError(path) from None
		if isinstance(kind, GenericAlias):
			kind = kind.__origin__
		if not isinstance(result, kind):
			raise TypeError(f"{path} is wrong type; expected {kind}; got {type(result)}")
		if convert is None:
			return result
		return convert(result)


class JSONObject(JSONPathMixin, dict[str, Any]):
	"""
	A dict for JSON objects that implements `.path` for getting child items by a JSON path
	"""

	@classmethod
	def from_string(cls, string: bytes) -> Self:
		"""
		Create a JSONObject from a JSON string
		"""
		obj = orjson.loads(string)
		if not isinstance(obj, dict):
			raise TypeError(f"expected a JSON mapping, got {type(obj)}")
		return cls(obj)


class JSONArray(JSONPathMixin, list[Any]):
	"""
	A list for JSON arrays that implements `.path` for getting child items by a JSON path
	"""

	@classmethod
	def from_string(cls, string: bytes) -> Self:
		"""
		Create a JSONArray from a JSON string
		"""
		obj = orjson.loads(string)
		if not isinstance(obj, list):
			raise TypeError(f"expected a JSON array, got {type(obj)}")
		return cls(obj)
