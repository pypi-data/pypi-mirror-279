'''
    Response
'''
import logging
from dataclasses import dataclass
from rlabs_mini_box.data import Box
from typing import Any
from typing import Dict
from typing import Optional
from typing import ClassVar


@dataclass
class Response:
    attempts_made: int
    status_code: int
    headers: Dict[str, str]
    text: str
    python_data: Optional[Any]
    json_data: Optional[str]
    databox: Optional[Box]

    __logger: ClassVar[Optional[logging.Logger]] = None
