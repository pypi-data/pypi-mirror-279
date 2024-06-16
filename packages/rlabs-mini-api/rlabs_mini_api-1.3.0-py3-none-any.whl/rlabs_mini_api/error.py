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
    error.py
'''
from rlabs_mini_api import logger

class PrettyError(Exception):
    '''
        Custom Base Error

        This is the base class for all custom errors.

        Pretty Logs error to stdout and exits with -1
    '''
    def __init__(self, msg: str):
        super().__init__(msg)

class MaxAttemptsError(PrettyError):
    '''
        Max Attempts Error

        This error is raised when the maximum number of attempts
        has been reached when trying to execute a request.
    '''
    def __init__(self, msg: str):
        super().__init__(msg)
