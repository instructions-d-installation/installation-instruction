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


try:
    from yaml import safe_load
except ImportError:
    from yaml import safe_load

import json

from jsonschema import validate

from jinja2 import Environment, Template


import installation_instruction.helpers as helpers


class InstallationInstruction:
    """
    Class holding schema and template for validating and rendering installation instruction.
    """

    def validate_and_render(self, input: dict) -> tuple[str, bool]:
        """
        Validates user input against schema and renders with the template.
        Returns installation instructions and False. 
        If template '[[ERROR]]' is called returns error message and True.

        :param input: Enduser input.
        :ptype input: dict
        :return: Returns instructions as string and False. Or Error and True.
        :rtpye: (str, bool)
        :raise Exception: If no delimiter is found.
        """
        validate(input, self.schema)
        instruction = self.template.render(input)
        
        if error := helpers._get_error_message_from_string(instruction):
            return (error, True)
        
        instruction = helpers._replace_whitespace_in_string(instruction)

        return (instruction, False)


    def __init__(self, config: str) -> None:
        """
        :param config: Config file with schema and template seperated by ------ delimiter.
        :raise Exception: If schema part of config is neither valid json nor valid yaml.
        """
        (schema, template) = helpers._split_string_at_delimiter(config)
        try:
            self.schema = json.load(schema)
        except:
            try:
                self.schema = safe_load(schema)
            except:
                raise Exception("Schema is neither a valid json nor a valid yaml.")

        self.template = helpers._load_template_from_string(template)
