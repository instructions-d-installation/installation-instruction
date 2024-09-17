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

import click
from click import Option, Choice
import os
import platformdirs
import json
from os.path import isfile

SCHEMA_TO_CLICK_TYPE_MAPPING = {
    "string": click.STRING,
    "integer": click.INT,
    "number": click.FLOAT,
    "boolean": click.BOOL,
}

def _get_flags_and_options(schema: dict, misc: dict = None, inst: bool = False) -> list[Option]:
    """
    Generates Click flags and options from a JSON schema.

    :param schema: Schema which contains the options.
    :param misc: Additional descriptions and pretty print names nested.
    :type schema: dict
    :return: List of all the clickoptions from the schema.
    :rtype: list[Option]
    """
    options = []
    alt_default = {}
    required_args = set(schema.get('required', []))

    description = misc.get("description", {}) if misc is not None else {}

    change_default = False
    if inst:
        project_title = schema.get("$id")
        user_data_dir = platformdirs.user_data_dir("default_data_local","installation_instruction")
        PATH_TO_DEFAULT_FILE = os.path.join(user_data_dir, "DEFAULT_DATA.json")
        default_data = {}
        if isfile(PATH_TO_DEFAULT_FILE):
            with open(PATH_TO_DEFAULT_FILE,"r") as f:
                default_data = json.load(f)
        if project_title in default_data.keys():
            default_data = default_data.get(project_title)
            change_default = True


    for key, value in schema.get('properties', {}).items():
        pretty_key = key
        pretty_key = pretty_key.replace('_', '-').replace(' ', '-')
        option_name = '--{}'.format(pretty_key)
        option_type = value.get('type', 'string')
        option_description = value.get('description', '') or description.get(key, "")
        if change_default and key in default_data.keys():
            option_default = default_data.get(key)
        else:
            option_default = value.get('default', None)
        if "enum" in value:
            option_type = Choice( value["enum"] )
        else:
            option_type = SCHEMA_TO_CLICK_TYPE_MAPPING.get(option_type, click.STRING)

        required = (key in required_args) and option_default is None
        is_flag=(option_type == click.BOOL)
        if is_flag and required:
            option_name = option_name + "/--no-{}".format(pretty_key)
        if not inst:
            alt_default[key]=option_default
            required = False
            option_default = None
        options.append(Option(
            param_decls=[option_name],
            type=option_type,
            help=option_description,
            required=required,
            default=option_default,
            show_default=True,
            show_choices=True,
            is_flag=is_flag,
        ))
    if not inst:
        return options, alt_default
    return options