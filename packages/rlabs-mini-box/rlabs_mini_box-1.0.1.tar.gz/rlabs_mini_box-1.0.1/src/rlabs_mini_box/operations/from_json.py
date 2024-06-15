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
    ToPython
'''
import json
import logging

from rlabs_mini_box.data import Box
from rlabs_mini_box.error import OperationInvalidType

def apply(self: Box, logger: logging.Logger) -> Box:
    '''
        Apply
    '''
    logger.debug(
        f"Operation: From JSON"
    )

    try:
        self._data = json.loads(self._data)
    except json.JSONDecodeError:
        logger.warning(
            f"fecthed data is not valid JSON ."
            f"\nHere's a small sample data: {str(self._data)[:100]}..."
            "\nCarrying on, setting data to None"
        )
        self._data = None

    return self
