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
    Run Manual Test
    (entry point)

    For help type:
      poetry run manual-test-run --help

'''
from time import sleep
import os
import logging
import json
from pathlib import Path

from rlabs_mini_api.request import GET
from rlabs_mini_api.request import POST
from rlabs_mini_api.request import DELETE
from rlabs_mini_api.request import PUT
from rlabs_mini_api.request import Request


GITLAB_API_URL = "https://gitlab.com/api/v4"
DUMMY_TEST_GROUP_ID = 79866152

def main():
    '''
        main
    '''

    ##
    ##  There's no main in a package, this is just a sample
    ##  for when building the classes
    ##
    ##  Replace this with a test
    ##

    # Configure for all requests
    Request.config(
        GITLAB_API_URL,
        { "PRIVATE-TOKEN": os.environ['TOKEN'] },
        log_level=logging.DEBUG,
        response_log_dir=Path("../logs")
    )

    ## -- Delete variable --
    DELETE                          \
        .groups                     \
        .id(DUMMY_TEST_GROUP_ID)    \
        .variables                  \
        .key("dummy_var")           \
        .exec(1,1)

    sleep(2)
    response = GET                          \
        .groups                             \
        .id(DUMMY_TEST_GROUP_ID)            \
        .variables(page=1, per_page=100)    \
        .exec(3,2)

    vars = [
        { var['key'] :  var['value'] }
        for var in response.python_data
    ]

    print(json.dumps(vars, indent=2))

    ## -- Create variable --
    POST                            \
        .groups                     \
        .id(DUMMY_TEST_GROUP_ID)    \
        .variables(
            key="dummy_var",
            value="dummy_val"
        )                           \
        .exec(1,1)

    sleep(2)
    response = GET                          \
        .groups                             \
        .id(DUMMY_TEST_GROUP_ID)            \
        .variables(page=1, per_page=100)    \
        .exec(3,2)

    vars = [
        { var['key'] :  var['value'] }
        for var in response.python_data
    ]

    print(json.dumps(vars, indent=2))

    ## -- Update variable --
    PUT(data={
        "value": "UPDATED_VALUE"
    })                              \
        .groups                     \
        .id(DUMMY_TEST_GROUP_ID)    \
        .variables                  \
        .key("dummy_var")           \
        .exec(1,1)

    sleep(2)
    response = GET                          \
        .groups                             \
        .id(DUMMY_TEST_GROUP_ID)            \
        .variables(page=1, per_page=100)    \
        .exec(3,2)

    vars = [
        { var['key'] :  var['value'] }
        for var in response.python_data
    ]

    print(json.dumps(vars, indent=2))



if __name__ == "__main__":
    main()
