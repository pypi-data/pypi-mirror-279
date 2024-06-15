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
import httpx
import time
import json
import logging
from typing import ClassVar
from typing import Dict
from typing import Optional
from typing import Any
from typing import cast
from dataclasses import dataclass
from pathlib import Path

from rlabs_mini_api.error import MaxAttemptsError
from rlabs_mini_api import logger
from rlabs_mini_api import directory

@dataclass
class Response:
    attempts_made: int
    status_code: int
    headers: Dict[str, str]
    text: str
    python_data: Optional[Any]
    json_data: Optional[str]

    __logger: ClassVar[logging.Logger] = None

class RequestMeta(type):
    def __getattr__(cls, path_part: str) -> 'Request':
        return Request(cls._http_method).__append_path(path_part)

    def __call__(cls, *args: Any, **kwargs: Any) -> 'Request':
        return Request(cls._http_method, *args, **kwargs)

class Request:
    '''
        Request
    '''
    base_url: ClassVar[str] = ''
    headers: ClassVar[Dict[str, str]] = {}
    log_level: ClassVar[Optional[int]] = logging.INFO
    logger_override: ClassVar[Optional[logging.Logger]] = None
    logger: ClassVar[logging.Logger]
    response_log_dir: ClassVar[Optional[Path]] = None
    must_log_response: ClassVar[bool] = False

    def __init__(
            self,
            http_method: str = 'GET',
            data: Optional[Dict[str, Any]] = None,
            content: Optional[bytes] = None
        ) -> None:
        '''
            Init
        '''
        #
        # set as private to avoid name collisions
        # when users do Get.content() for example
        #
        self._path: str = Request.base_url
        self._http_method: str = http_method
        self._params: list[Dict[str, Any]] = []
        self._data: Optional[Dict[str, Any]] = data
        self._content: Optional[bytes] = content

    @staticmethod
    def config(
        base_url: str,
        headers: Dict[str, str],
        log_level: Optional[int] = None,
        logger_override: Optional[logging.Logger] = None,
        response_log_dir: Optional[Path] = None
    ) -> None:
        '''
            config

            Configures the base URL and headers for all requests
        '''
        Request.base_url = base_url
        Request.headers = headers
        Request.response_log_dir = response_log_dir
        Request.must_log_response = response_log_dir is not None

        # Set up logging
        if log_level and logger_override:
            raise ValueError(
                "log_level and logger_override are mutually exclusive. "
                "Please provide one or the other."
            )

        if not log_level and not logger_override:
            raise ValueError(
                "log_level or logger_override must be provided."
            )

        if logger_override:
            Request.logger = logger_override
            Request.log_level = logger_override.getEffectiveLevel()
        else:
            Request.logger = logger.stdout(
                __name__,
                cast(
                    int,
                    log_level
                )
            )
            Request.log_level = log_level

        logger.enable_pretty_tracebacks()

        # Setups response logging
        if Request.must_log_response:
            directory.create_empty_dir(
                cast(
                    Path,
                    response_log_dir
                )
            )


    def __getattr__(
            self,
            path_part: str
        ) -> 'Request':
        '''
            __getattr__

            Captures get attribute calls

            Returns a new Request object with
            the path part appended to the current path
        '''
        return self.__append_path(path_part)

    def __call__(
            self,
            *args: Any,
            **kwargs: Any
        ) -> 'Request':
        '''
            __call__

            Captures call to object

            If arguments are passed, replaces the last path part
            Otherwise, appends the keyword arguments as query parameters
        '''
        if args:
            #
            # Split the path into parts, replace the last part with the argument
            #
            # e.g. Given
            #           self.path = "groups/id" and args = (123,)
            #      This will:
            #           change self.path to "groups/123"
            #
            path_parts = self._path.split('/')
            path_parts[-1] = str(args[0])
            self._path = '/'.join(path_parts)

        if kwargs:
            self._params.append(kwargs)

        return self

    def __append_path(self, path_part: str) -> 'Request':
        '''
            Append Path

            Appends a path part to the current path
        '''
        if self._path:
            self._path = f"{self._path}/{path_part}"
        else:
            self._path = path_part
        return self

    def build_url(self) -> str:
        '''
            Build URL

            Constructs the full URL with query parameters

            Example:
                Given
                    self.path = "https://example.com/api/resource"
                and
                    self.params = [{"key1": "value1", "key2": "value2"}]

                This will return:

                    "https://example.com/api/resource?key1=value1&key2=value2"
        '''
        query_string = ''

        if self._params:
            param_list = [
                f"{key}={value}"
                for param_dict in self._params
                for key, value in param_dict.items()
            ]
            query_string = '?' + '&'.join(param_list)

        return self._path + query_string

    def exec(
            self,
            retries: int = 3,
            retry_base_delay: float = 0.5
        ) -> Response:
        '''
            Exec

            Executes the request with retries

            Params:
                retries: Number of retries to attempt
                retry_base_delay: float = Delay between retries in seconds

            Returns:
                A Response object with the following attributes:
                    attempts_made: Number of attempts made
                    status_code: HTTP status code
                    headers: Response headers
                    text: Response text
                    python_data: Parsed JSON response if content-type is application/json
                    json_data: JSON string of the parsed response

            Raises:
                MaxAttemptsError: If max retries are reached
        '''

        attempt = 0

        while True:

            attempt += 1

            url = self.build_url()

            Request.logger.debug(
                f"{self._http_method} {url}"
            )

            try:
                with httpx.Client() as client:

                    match self._http_method:
                        case 'GET':
                            response = client.get(
                                url,
                                headers=Request.headers
                            )
                        case 'POST':
                            if self._content:
                                response = client.post(
                                    url,
                                    headers=Request.headers,
                                    content=self._content
                                )
                            else:
                                response = client.post(
                                    url,
                                    headers=Request.headers,
                                    json=self._data
                                )
                        case 'PUT':
                            if self._content:
                                response = client.put(
                                    url,
                                    headers=Request.headers,
                                    content=self._content
                                )
                            else:
                                response = client.put(
                                    url,
                                    headers=Request.headers,
                                    json=self._data
                                )
                        case 'DELETE':
                            response = client.delete(
                                url,
                                headers=Request.headers
                            )
                        case _:
                            raise ValueError(
                                f"Unsupported HTTP method: {self._http_method}"
                            )

                    response.raise_for_status()

                    try:
                        python_data = response.json()
                    except json.JSONDecodeError:
                        python_data = None

                    json_data = json.dumps(python_data, indent=2) if python_data else None

                    if Request.must_log_response:

                        logger.log_response(
                            cast(
                                Path,
                                Request.response_log_dir
                            ),
                            self._http_method,
                            url.replace(Request.base_url, '').lstrip('/'),
                            Request.headers,
                            python_data,
                            cast(
                                int,
                                Request.log_level
                            )
                        )

                    return Response(
                        attempts_made=attempt,
                        status_code=response.status_code,
                        headers=dict(response.headers),
                        text=response.text,
                        python_data=python_data,
                        json_data=json_data
                    )

            except httpx.RequestError as e:

                Request.logger.warning(
                    f"Attempt {attempt} of {retries}: {e}"
                )

                if attempt >= retries:
                    raise MaxAttemptsError(
                        f"Max retries reached: {e}"
                    )

                # Sleep for an exponentially increasing delay
                delay = retry_base_delay*(2.0**attempt-1)

                Request.logger.debug(
                    f"Retrying in {delay} seconds"
                )

                time.sleep(delay)

class GET(metaclass=RequestMeta):
    '''
        GET
    '''
    _http_method: str = 'GET'

class DELETE(metaclass=RequestMeta):
    '''
        DELETE
    '''
    _http_method: str = 'DELETE'

class POST(metaclass=RequestMeta):
    '''
        POST
    '''
    _http_method: str = 'POST'

    def __call__(
        cls,
        data: Optional[Dict[str, Any]] = None,
        *args: Any,
        **kwargs: Any
    ) -> Request:

        return Request(
            cls._http_method,
            data
        )

class PUT(metaclass=RequestMeta):
    '''
        PUT
    '''
    _http_method: str = 'PUT'

    def __call__(
        cls,
        data: Optional[Dict[str, Any]] = None,
        content: Optional[bytes] = None,
        *args: Any,
        **kwargs: Any
    ) -> Request:

        return Request(
            cls._http_method,
            data
        )
