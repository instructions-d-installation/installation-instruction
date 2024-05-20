# Copyright 2024 Adam McKellar, Kanushka Gupta, Timo Ege

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import pytest
import os
import yaml
import json


@pytest.fixture
def test_data_flags_options():
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'flags_options_example.schema.yml')
    with open(file_path,"r") as file:
        return yaml.safe_load(file)

@pytest.fixture
def test_data_user_input(request):
    file_name = request.param
    file_path = os.path.join(os.path.dirname(__file__), 'data', file_name)
    with open(file_path,"r") as file:
        data = file.read()
    test_input = json.loads(data)
    return [file_name,test_input]

