#  Copyright 2021, 2023  Dominik Sekotill <dom.sekotill@kodo.org.uk>
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Miscellaneous useful functions
"""

from __future__ import annotations

from collections.abc import Callable
from time import sleep
from time import time


def wait(predicate: Callable[[], bool], timeout: float = 120.0) -> None:
	"""
	Block and periodically call "predictate" until it returns True, or the time limit passes
	"""
	end = time() + timeout
	left = timeout
	while left > 0.0:
		sleep(
			10 if left > 60.0 else
			5 if left > 10.0 else
			1,
		)
		left = end - time()
		if predicate():
			return
	raise TimeoutError
