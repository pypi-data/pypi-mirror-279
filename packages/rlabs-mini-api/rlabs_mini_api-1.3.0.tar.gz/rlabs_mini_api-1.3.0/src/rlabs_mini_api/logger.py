#
# Copyright (C) 2024 RomanLabs, Rafael Roman Otero
# This file is part of RLabs Mini API.
#
# RLabs Mini API is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RLabs Mini API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with RLabs Mini API. If not, see <http://www.gnu.org/licenses/>.
#
'''
    logger.py
'''
import logging
import json
import rich
from rich.logging import RichHandler
from rich.traceback import install
from pathlib import Path
from typing import Any

from rlabs_mini_api import config

logged_filenames: dict= {}

def enable_pretty_tracebacks() -> None:
    '''
        Enable Pretty Traceback

        Uses rich to print pretty tracebacks
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

def log_response(
        output_dir: Path,
        request_type: str,
        request_url: str,
        request_headers: dict,
        response_data: Any,
        log_level: int
    ) -> None:
    '''
        Log Response

        Params:
            - output_dir: Output
            - request_type: Request type
            - request_url: Request URL
            - request_headers: Request headers
            - response_data: Response data

        Sample log:


    '''
    JSON_INDENT=2

    if log_level and log_level > logging.DEBUG:
        return

    filename = f"{request_type}_{request_url.replace("/", "_")}"

    # deduplicate logs for the same request URL
    if filename not in logged_filenames:
        logged_filenames[filename] = 1
        dedup_suffix = ""
    else:
        logged_filenames[filename] += 1
        dedup_suffix = str(logged_filenames[filename])

    if not dedup_suffix:
        log_path = output_dir / f"{filename}.log"
    else:
        log_path = output_dir / f"{filename}_{dedup_suffix}.log"

    with open(log_path, "a") as file:
        file.write(
            f"{request_type} {request_url}\n\n"
        )
        file.write(
            f"{json.dumps(request_headers, indent=2)}\n\n"
        )
        file.write(
            f"-------------------------------------\n"
            f"              Response               \n"
            f"-------------------------------------\n"
        )
        if isinstance(response_data, dict) or isinstance(response_data, list):
            file.write(
                json.dumps(
                    response_data,
                    indent=JSON_INDENT
                )
            )
        else:
            file.write(str(response_data))

        file.write('\n')

