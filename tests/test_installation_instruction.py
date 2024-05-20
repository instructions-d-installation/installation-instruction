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


from pytest import raises

from installation_instruction.installation_instruction import InstallationInstruction

def test_validate_and_render_pytorch():
    valid_user_input = {
        "build": "preview",
        "os": "win",
        "package": "pip",
        "compute_platform": "ro60"
    }
    
    bad_user_input = {
        "build": "preview",
        "os": "win",
        "package": "piiip",
        "compute_platform": "ro60"
    }   

    install = InstallationInstruction.from_file("examples/pytorch/pytorch-instruction.schema.yml.jinja")

    good_installation_instruction = install.validate_and_render(valid_user_input)

    assert ('Windows does not support ROCm!', True) == good_installation_instruction

    with raises(Exception):
        install.validate_and_render(bad_user_input)


def test_validate_and_render_scikit():
    valid_user_input = {
        "os": "Windows",
        "packager": "pip",
        "virtualenv": False
    }

    invalid_user_input = {
        "os": "Kali",
        "packager": "pip",
        "virtualenv": False
    }

    install = InstallationInstruction.from_file("examples/scikit-learn/scikit-learn-instruction.schema.yml.jinja")

    good_installation_instruction = install.validate_and_render(valid_user_input)

    assert ('pip install -U scikit-learn', False) == good_installation_instruction

    with raises(Exception):
        install.validate_and_render(invalid_user_input)

def test_validate_and_render_spacy():
    valid_user_input = {
        "os": "Windows",
        "platform": "x86",
        "package": "pip",
        "hardware": "CPU"
    }

    invalid_user_input = {
        "os": "Windows",
        "platform": "x86",
        "package": "forge",
        "hardware": "CPU"
    }

    install = InstallationInstruction.from_file("examples/scikit-learn/scikit-learn-instruction.schema.yml.jinja")

    good_installation_instruction = install.validate_and_render(valid_user_input)

    assert ('pip install -U scikit-learn', False) == good_installation_instruction

    with raises(Exception):
        install.validate_and_render(invalid_user_input)
