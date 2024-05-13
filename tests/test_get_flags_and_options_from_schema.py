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
import click
import yaml

def test_get_flags_and_options():
    example_schema = '''$schema: https://json-schema.org/draft/2020-12/schema
$id: https://github.com/instructions-d-installation/installation-instruction/examples/scikit-learn/scikit-learn-instruction.schema.yml
title: Scikit-learn installation schema
description: This is a Schema to construct installation instructions for the python package scikit-learn by Timo Ege.
type: object
properties:
  os:
    title: Operating System
    description: The operating system in which the package is installed.
    enum: 
      - Windows
      - macOS
      - Linux
    default: Windows

  packager:
    title: Packager
    description: The package manager of your choosing.
    enum: 
      - pip
      - conda
    default: pip

  virtualenv:
    title: Use pip virtualenv
    description: Choose if you want to use a virtual environment to install the package.   
    type: boolean 
    default: false

  compute_platform:
    title: Compute Platform
    description: Should your gpu or your cpu handle the task?
    anyOf:
      - title: CUDA 11.8
        const: cu118
      - title: CUDA 12.1
        const: cu121
    default: cu118

required:
  - os
  - packager

additionalProperties: false'''
    example = yaml.safe_load(example_schema)
    options = get_flags_and_options(example)

    assert len(options) == 4
    assert options[0]['name'] == '--os'
    assert options[0]['description'] == "The operating system in which the package is installed."
    assert options[0]['required'] == True
    assert options[1]['name'] == '--packager'
    assert options[1]['description'] == "The package manager of your choosing."
    assert options[1]['required'] == True
    assert options[2]['name'] == '--virtualenv'
    assert options[2]['description'] == "Choose if you want to use a virtual environment to install the package."
    assert options[2]['required'] == False
    assert options[3]['name'] == '--compute_platform'
    assert options[3]['description'] == "CUDA 11.8\nCUDA 12.1"
    assert options[3]['required'] == False