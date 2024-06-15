#
# Copyright (C) 2024 RomanLabs, Rafael Roman Otero
# This file is part of RLabs MiniBox.
#
# RLabs MiniBox is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RLabs MiniBox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with RLabs MiniBox. If not, see <http://www.gnu.org/licenses/>.
#
'''
    Filter
'''
import inspect
import logging
from typing import Callable

from rlabs_mini_box.data import Box
from rlabs_mini_box.error import OperationInvalidType

def apply(self: Box, logger: logging.Logger, function: Callable) -> Box:
    '''
        Apply
    '''
    function_code = inspect.getsource(function).strip()

    logger.debug(
        f"Operation: Filter\n"
        f"Filter Function:   \n{function_code}"
    )

    if isinstance(self._data, dict):
        self._data = {
            key: self._data[key]
            for key in self._data if function(key)
        }
    elif isinstance(self._data, list):
        self._data = [
            d for d in self._data if function(d)
        ]
    else:
        raise OperationInvalidType(
            "filter",
            type(self._data)
        )

    return self
