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
   Error
'''

from rlabs_mini_box import logger
from typing import Any

class PrettyError(Exception):
    '''
       Custom Base Error

       This is the base class for all custom errors.

       Pretty Logs error to stdout and exits with -1
    '''
    def __init__(self, msg: str):
        super().__init__(msg)

class DataBoxTypeError(PrettyError):
    '''
       DataBoxTypeError

       Custom error for type validation in MiniBox.

       Params:
          - key: The key where the error occurred.
          - expected_type: The expected type of the field.
          - received_type: The actual type of the field received.
    '''
    def __init__(self, key: str, expected_type: type, received_type: type):
        msg = (
            f"Field '{key}' is expected to be of type '{expected_type.__name__}', "
            f"but received type '{received_type.__name__}'."
        )
        super().__init__(msg)
        self.key = key
        self.expected_type = expected_type
        self.received_type = received_type

class OperationInvalidType(Exception):
    '''
        StepError
    '''
    def __init__(self, operation_name: str, data_type: Any) -> None:
        super().__init__(
            f"Operation '{operation_name}' not supported for data type '{data_type}'"
        )

class ConfigError(Exception):
    '''
        ConfigError
    '''
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class OperationError(Exception):
    '''
        OperationError
    '''
    def __init__(self, name: str, msg: str) -> None:
        super().__init__(
            f"Operation '{name}' failed with error: {msg}"
        )
