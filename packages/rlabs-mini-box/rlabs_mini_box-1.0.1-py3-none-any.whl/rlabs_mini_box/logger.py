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
    logger.py
'''
import logging
import json
import rich
from pathlib import Path
from typing import Any
from rich.logging import RichHandler
from rich.traceback import install

from rlabs_mini_box import config

current_operation_num: int = 0

def enable_pretty_tracebacks() -> None:
    '''
        Enable Pretty Traceback

        Uses rich to print pretty tracebacks.
    '''
    install()

def stdout(name: str, log_level: int) -> logging.Logger:
    '''
        Sets up a logger that logs to stdout

        Uses RichHandler to pretty print logs
    '''
    words_to_highlight = config.log_words_to_highlight

    handler = RichHandler(
        show_time=config.log_show_time,
        keywords=[w.lower() for w in words_to_highlight] + \
                 [w.upper() for w in words_to_highlight] + \
                 [w.capitalize() for w in words_to_highlight]
    )

    logger = CustomLogger(name)
    logger.setLevel(log_level)
    formatter = logging.Formatter(config.log_formatter)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

class CustomLogger(logging.Logger):
    '''
        Extends the logging.Logger class
        with  custom methods
    '''
    def flush(self) -> None:
        '''
            Flush

            Flushes the logger
        '''
        for handler in self.handlers:
            handler.flush()

    def inspect(obj: object, title: str) -> None:
        '''
            Inspect

            Wrapper for rich's inspect
        '''
        rich.inspect(
            obj,
            title=title,
            docs=False
        )

def log_operation(
        output_dir: Path,
        operation_name: str,
        data: Any,
        log_level: int
    ) -> None:
    '''
        Log Operation

        Logs the operation data to a file, only
        if the log level is DEBUG or lower.

        Params:
            - output_dir: Output
            - operation_name: Operation name
            - data: Data to log
            - log_level: Log level
    '''
    global current_operation_num
    JSON_INDENT=2

    if log_level and log_level > logging.DEBUG:
        return

    log_path = output_dir / f"{current_operation_num}_{operation_name}.log"

    with open(log_path, "a") as file:

        if current_operation_num == 0:
            file.write(
                f"\nType: {str(type(data))}\n\n"
            )
        else:
            file.write(
                f"\nOperation: {operation_name}"
                f"\nType: {str(type(data))}\n\n"
            )
        file.write(
            f"-------------------------------------\n"
            f"                Data                 \n"
            f"-------------------------------------\n"
        )
        if isinstance(data, dict) or isinstance(data, list):
            file.write(
                json.dumps(
                    data,
                    indent=JSON_INDENT
                )
            )
        elif isinstance(data, str):
            file.write("'''\n")
            file.write(str(data))
            file.write("\n'''")
        else:
            file.write(str(data))

        file.write('\n')

        current_operation_num += 1
