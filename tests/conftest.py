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
import glob

example_schemas = {
    "pytorch":"examples/pytorch/pytorch-instruction.schema.yml.jinja",
    "scikit":"examples/scikit-learn/scikit-learn-instruction.schema.yml.jinja",
    "spacy":"examples/spacy/spacy-instruction.schema.yml.jinja"
}

_user_input_data = []
_user_input_name = []

for filename in glob.glob(os.path.join(os.path.split(__file__)[0], "data", "*valid_data.*")):
    with open(filename, "r") as f:
        try:
            with open(filename, "r") as f:
                _user_input_data.append(json.load(f))
                _user_input_name.append(os.path.basename(filename))
        except:
            with open(filename, "r") as f:
                split = f.readlines()
                split[0] = split[0][:-1]
                _user_input_data.append((split[0],split[1] == 'True'))
                _user_input_name.append(os.path.basename(filename))

packages = []
for i in _user_input_name:
    package = i.split("_")[0]
    if package not in packages:
        packages.append(package)

test_data = []
for package in packages:
    valid_id = _user_input_name.index(f"{package}_valid_data.json")
    invalid_id = _user_input_name.index(f"{package}_invalid_data.json")
    expected_value = _user_input_name.index(f"{package}_expected_valid_data.txt")
    tested_file_path = example_schemas.get(package)
    test_data.append([tested_file_path,_user_input_data[valid_id],_user_input_data[invalid_id],_user_input_data[expected_value]])


def pytest_generate_tests(metafunc):
    if "user_input_tests" in metafunc.fixturenames:
        metafunc.parametrize("user_input_tests",test_data)


@pytest.fixture
def test_data_flags_options():
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'flags_options_example.schema.yml')
    with open(file_path,"r") as file:
        example = yaml.safe_load(file)
    
    return example

