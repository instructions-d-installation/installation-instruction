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
from jsonschema import validate, Draft202012Validator, exceptions
from jinja2.exceptions import UndefinedError

import installation_instruction.helpers as helpers


RAISE_JINJA_MACRO_STRING = """
{% macro raise(error) %}
    {{ None['[ERROR] ' ~ error][0] }}
{% endmacro %}
"""

COMMAND_JINJA_MACRO_STRING = """
{% macro command() %}
    {% filter replace("\n", "") %}
        {{ caller() }}
    {% endfilter %} 
{% endmacro %}
"""

MACROS = [
    RAISE_JINJA_MACRO_STRING,
    COMMAND_JINJA_MACRO_STRING,
]


class InstallationInstruction:
    """
    Class holding schema and template for validating and rendering installation instruction.
    """

    def validate_and_render(self, input: dict) -> tuple[list[str], bool]:
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
                return ([errmsg], True)
            else:
                raise e
        
        instruction = helpers._replace_whitespace_in_string_and_split_it(instruction)

        return (instruction, False)
    
    def parse_schema(self) -> dict:
        """
        Parses schema into a dict.

        This is only important for merging enum, anyOf and oneOf into one type.

        :return: Schema as dict.
        :rtype: dict
        """
        result = {}

        result["title"] = self.schema.get("title", "")
        result["description"] = self.schema.get("description", "")
        result["properties"] = {}

        pretty = self.misc.get("pretty", {})
        description = self.misc.get("description", {})

        for key, value in self.schema.get('properties', {}).items():

            result["properties"][key] = {
                "title": value.get("title", "") or pretty.get(key, key),
                "description": value.get("description", "") or description.get(key, ""),
                "type": value.get("type", "string"),
                "default": value.get("default", None),
                "key": key,
            }
            if "enum" in value:
                result["properties"][key]["enum"] = [
                    {
                        "title": pretty.get(e, e),
                        "key": e,
                        "description": description.get(e, ""),
                    } for e in value["enum"]
                ]
                result["properties"][key]["type"] = "enum"
                
        return result


    def __init__(self, config: str) -> None:
        """
        Returns `InstallationInstruction` from config string. This also adds raise macro to template.

        :param config: Config string with schema and template seperated by delimiter.
        :raise Exception: If schema part of config is neither valid json nor valid yaml.
        :raise Exception: If no delimiter is found.
        """
        (schema_str, template) = helpers._split_string_at_delimiter(config)
        try:
            schema = json.load(schema_str)
        except:
            try:
                schema = safe_load(schema_str)
            except:
                raise Exception("Schema is neither a valid json nor a valid yaml.")
            
        if "schema" in schema:
            self.schema = schema["schema"]
            self.misc = {key: schema[key] for key in schema if key != "schema"}
        else:
            self.schema = schema
            self.misc = {}
        
        try:
            Draft202012Validator.check_schema(self.schema)
        except exceptions.SchemaError as e:
            raise Exception(f"The given schema file is not a valid json schema.\n\n{e}")
        self.template = helpers._load_template_from_string("".join(MACROS)  + template)


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

