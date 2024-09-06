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


from jinja2 import Template
from installation_instruction import helpers
from installation_instruction.installation_instruction import InstallationInstruction


def test_get_error_message_from_string_with_macro():
    example_config = r"""
type: object
properties:
   err:
      type: boolean
------
something
{{ raise("test message") if err }}
something
"""

    install = InstallationInstruction(example_config)

    assert install.validate_and_render({ "err": True }) == ("test message", True)
    assert install.validate_and_render({ "err": False }) == ("something something", False)



def test_get_error_message_from_string_with_err_message():
    err_string = """
    abcd
    '[ERROR] Mac does not support ROCm or CUDA!'
    
    efg
    """
    msg = helpers._get_error_message_from_string(err_string)
    assert msg == "Mac does not support ROCm or CUDA!"

def test__get_error_message_from_string_without_err_message():
    err_string = """
    abcd
    
    efg
    """
    msg = helpers._get_error_message_from_string(err_string)
    assert msg is None

def test_replace_whitespace_in_string():
    string = """
     python     -m pip
    install

    installation_instruction

    """
    res = helpers._replace_whitespace_in_string_and_split_it(string)
    assert res == [
        "python -m pip"
        "install"
        "installation_instruction"
    ]


def test_split_string_at_delimiter_with_delimiter():
    string = """
os:
 - win
 - mac
something:

------

{% if os == 'win' %}
    do stuff
{% endif %}

    """

    schema = """os:
 - win
 - mac
something:"""
    
    template = """{% if os == 'win' %}
    do stuff
{% endif %}"""
    
    (parsed_schema, parsed_template) = helpers._split_string_at_delimiter(string)
    assert schema == parsed_schema
    assert template == parsed_template

def test_is_remote_git_repository():
    assert helpers._is_remote_git_repository("https://github.com/instructions-d-installation/web-installation-instruction.git")
    assert not helpers._is_remote_git_repository("./instructions-d-installation/web-installation-instruction.git")
