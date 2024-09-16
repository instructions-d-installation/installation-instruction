
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

with open("tests/data/example_data.json","r") as f:
    data_test = json.load(f)


def pytest_generate_tests(metafunc):
    if "user_input_tests" in metafunc.fixturenames:
        metafunc.parametrize("user_input_tests",data_test)


@pytest.fixture
def test_data_flags_options():
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'flags_options_example.schema.yml')
    with open(file_path,"r") as file:
        example = yaml.safe_load(file)
    
    return example["schema"]

@pytest.fixture
def test_data_flags_options_config_string_with_empty_template():
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'flags_options_example.schema.yml')
    with open(file_path,"r") as file:
        example = file.read()

    example += "\n------\nsomething"
    
    return example

@pytest.fixture
def test_data_flags_options():
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'spacy_example.schema.yml')
    with open(file_path,"r") as file:
        example = yaml.safe_load(file)
    
    return example["schema"]

@pytest.fixture
def test_data_flags_options_config_string_with_empty_template():
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'spacy_example.schema.yml')
    with open(file_path,"r") as file:
        example = file.read()

    example += "\n------\nsomething"
    
    return example

