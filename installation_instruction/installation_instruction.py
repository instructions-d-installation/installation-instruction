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


from yaml import safe_load
import json
from jsonschema import validate
from jinja2 import Environment, Template
from jinja2.exceptions import UndefinedError

import installation_instruction.helpers as helpers


RAISE_JINJA_MACRO_STRING = """
{% macro raise(error) %}
    {{ None['[ERROR] ' ~ error][0] }}
{% endmacro %}
"""


class InstallationInstruction:
    """
    Class holding schema and template for validating and rendering installation instruction.
    """

    def validate_and_render(self, input: dict) -> tuple[str, bool]:
        """
        Validates user input against schema and renders with the template.
        Returns installation instructions and False. 
        If jinja macro `raise` is called returns error message and True.

        :param input: Enduser input.
        :ptype input: dict
        :return: Returns instructions as string and False. Or Error and True.
        :rtpye: (str, bool)
        :raise Exception: If schema or user input is invalid.
        """
        validate(input, self.schema)

        try:
            instruction = self.template.render(input)
        except UndefinedError as e:
            if errmsg := helpers._get_error_message_from_string(str(e)):
                return (errmsg, True)
        
        instruction = helpers._replace_whitespace_in_string(instruction)

        return (instruction, False)


    def __init__(self, config: str) -> None:
        """
        Returns `InstallationInstruction` from config string. This also adds raise macro to template.

        :param config: Config string with schema and template seperated by delimiter.
        :raise Exception: If schema part of config is neither valid json nor valid yaml.
        :raise Exception: If no delimiter is found.
        """
        (schema, template) = helpers._split_string_at_delimiter(config)
        try:
            self.schema = json.load(schema)
        except:
            try:
                self.schema = safe_load(schema)
            except:
                raise Exception("Schema is neither a valid json nor a valid yaml.")

        self.template = helpers._load_template_from_string(RAISE_JINJA_MACRO_STRING+template)


    @classmethod
    def from_file(cls, path: str):
        """
        Returns class initialized via config file from path.

        :param path: Path to config file.
        :ptype path: str
        :return: InstallationInstruction class
        :rtype: InstallationInstruction
        """
        with open(path, 'r') as file:
            config = file.read()
        return cls(config)

