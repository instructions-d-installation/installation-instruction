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

from installation_instruction.installation_instruction import InstallationInstruction

@pytest.mark.parametrize("test_data_user_input",["pytorch_invalid_data.txt","pytorch_valid_data.txt"])
def test_validate_and_render_pytorch(test_data_user_input):
    
    test_data = test_data_user_input
    file_name = test_data[0]
    user_input = test_data[1]
    install = InstallationInstruction.from_file("examples/pytorch/pytorch-instruction.schema.yml.jinja")

    if "_valid_" in file_name:
        good_installation_instruction = install.validate_and_render(user_input)

        assert ('Windows does not support ROCm!', True) == good_installation_instruction
    elif "_invalid_" in file_name:
        with pytest.raises(Exception):
            install.validate_and_render(user_input)

@pytest.mark.parametrize("test_data_user_input",["scikit_invalid_data.txt","scikit_valid_data.txt"])
def test_validate_and_render_scikit(test_data_user_input):
    test_data = test_data_user_input
    file_name = test_data[0]
    user_input = test_data[1]

    install = InstallationInstruction.from_file("examples/scikit-learn/scikit-learn-instruction.schema.yml.jinja")

    if "_valid_" in file_name:
        good_installation_instruction = install.validate_and_render(user_input)

        assert ('pip install -U scikit-learn', False) == good_installation_instruction

    elif "_invalid_" in file_name:
        with pytest.raises(Exception):
            install.validate_and_render(user_input)
