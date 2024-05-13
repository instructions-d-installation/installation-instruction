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


from installation_instruction.get_flags_and_options_from_schema import get_flags_and_options
from installation_instruction.helpers import _split_string_at_delimiter
import yaml

def test_get_flags_and_options():
    with open("examples/scikit-learn/scikit-learn-instruction.schema.yml.jinja", 'r') as file:
        example_scikit = file.read()
    example_schema, example_jinja = _split_string_at_delimiter(example_scikit)
    dict_schema = yaml.safe_load(example_schema)
    options = get_flags_and_options(dict_schema)

    assert len(options) == 3
    assert options[0].name == '--os'
    assert options[0].help == "The operating system in which the package is installed. Choices: Windows, macOS, Linux (default: Windows)"
    assert options[1].name == '--packager'
    assert options[1].help == "The package manager of your choosing. Choices: pip, conda (default: pip)"
    assert options[2].name == '--virtualenv'
    assert options[2].help == "Choose if you want to use a virtual environment to install the package. (default: False)"
