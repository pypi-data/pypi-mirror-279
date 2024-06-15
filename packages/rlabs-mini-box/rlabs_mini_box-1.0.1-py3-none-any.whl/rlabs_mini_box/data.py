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
    Data
'''
from typing import Any
from typing import Optional
from typing import ClassVar
from typing import cast
import json
import logging
from pathlib import Path
import importlib

from rlabs_mini_box import logger
from rlabs_mini_box import directory
from rlabs_mini_box.error import ConfigError
from rlabs_mini_box.error import OperationError

MODULE_OPERATIONS_RELATIVE_PATH = Path(__file__).parent / "operations"
JSON_INDENT = 2

class Box:
    '''
        Box
    '''
    log_level: ClassVar[Optional[int]]
    logger: ClassVar[logging.Logger]
    operations_log_dir: ClassVar[Optional[Path]] = None
    __must_log_operations: ClassVar[bool] = False

    def __init__(self,
            data: list | dict | None = None,
        ) -> None:
        '''
            Init

            Params:
                - data: data to process
        '''
        self.__import_operations(
            MODULE_OPERATIONS_RELATIVE_PATH,
            "rlabs_mini_box.operations"
        )

        self._data = data

        # log initial data
        if Box.__must_log_operations:
            logger.log_operation(
                cast(
                    Path,
                    Box.operations_log_dir
                ),
                "initial data",
                self.data(),
                cast(
                    int,
                    Box.log_level
                )
            )

    def data(self) -> list | dict | None:
        '''
            Data

            Returns the data in the Box
        '''
        return self._data

    @staticmethod
    def config(
        log_level: Optional[int] = logging.INFO,
        logger_override: Optional[logging.Logger] = None,
        operations_log_dir: Optional[Path] = None
    ) -> None:
        '''
            config

            Configures the Box class.
        '''
        Box.log_level = log_level
        Box.operations_log_dir = operations_log_dir
        Box.__must_log_operations = operations_log_dir is not None

        if operations_log_dir is not None and not isinstance(operations_log_dir, Path):
            raise ConfigError(
                "'operations_log_dir' must be of type Path"
            )

        # Set up logging
        if Box.log_level and logger_override:
            raise ValueError(
                "log_level and logger_override are mutually exclusive. "
                "Please provide one or the other."
            )

        if logger_override:
            Box.logger = logger_override
        else:
            Box.logger = logger.stdout(
                __name__,
                cast(
                    int,
                    Box.log_level
                )
            )

        logger.enable_pretty_tracebacks()

        # Setups operations logging
        if Box.__must_log_operations:
            directory.create_empty_dir(
                cast(
                    Path,
                    operations_log_dir
                )
            )

    def __getattr__(self, name):
        '''
            __getattr__

            Map to Step

            Intercepts the call to a method that doesn't exist (presumably a step)
            and redirects it to the corresponding step module.

            Assumes step modules are loaded in the global namespace
            (i.e. have been imported).

            Raises:
                AttributeError if the step module doesn't exist.
        '''
        def operation_function(*args, **kwargs):

            if self._data is None:

                # skip operation
                Box.logger.warning(
                    f"None data (skipping operation {name})"
                )
                box_object = self

            else:
                # apply operation
                try:
                    apply_function = globals()[name].apply
                except KeyError:
                    raise AttributeError(
                        f"'{self.__class__.__name__}' object has no attribute '{name}'"
                    )

                try:
                    box_object = apply_function(
                        self,
                        Box.logger,
                        *args,
                        **kwargs
                    )
                except Exception as error:
                    raise OperationError(
                        name,
                        f"{str(type(error).__name__)}: {error}"
                    )from error

            # log operation
            if Box.__must_log_operations:

                logger.log_operation(
                    Box.operations_log_dir,
                    name,
                    box_object.data(),
                    Box.log_level
                )

            return box_object


        return operation_function

    def __import_operations(self, operations_dir: Path, module_address: str) -> None:
        '''
            Import Operations

            Dynamically imports all the Operations from the directory
            'operations_dir'. Assumes the directory contains only operations. Ignores
            anything with '__' in the filename.

            For each file in 'operations_dir', it will import:

                module_address.filename

            Params:
                - operations_dir: directory containing operations
                - module_address: module address to use when importing
        '''
        # gather all operation available
        # from the filenames in the operations_dir
        operations = [
            file.stem
            for file in operations_dir.iterdir()
            if file.is_file() and file.suffix == ".py" and "__" not in file.stem
        ]

        # import
        for operation in operations:
            globals()[operation] = importlib.import_module(f"{module_address}.{operation}")

