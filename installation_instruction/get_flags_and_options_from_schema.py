
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
from os.path import isfile
import os
import click
import json
import platformdirs


SCHEMA_TO_CLICK_TYPE_MAPPING = {
    "string": click.STRING,
    "integer": click.INT,
    "number": click.FLOAT,
    "boolean": click.BOOL,
}

def _parse_option(key, value, required_args, description, is_conditional=False):
    """
    Helper function to parse individual options, including conditional ones.
    """
    pretty_key = key.replace('_', '-').replace(' ', '-')
    option_name = f'--{pretty_key}'
    option_type = value.get('type', 'string')
    option_description = value.get('description', '') or description.get(key, "")
    option_default = value.get('default', None)

    if "enum" in value:
        # Preserve spaces in enum choices by not replacing them with underscores
        enum_choices = value["enum"]
        option_type = Choice(enum_choices, case_sensitive=False)
    elif option_type == 'array' and value.get('items', {}).get('enum'):
        choice_enum = value['items']['enum']
        option_type = Choice(choice_enum, case_sensitive=False, multiple=True)
        if option_default is None:
            option_default = ()
        elif isinstance(option_default, list):
            option_default = tuple(option_default)
        else:
            option_default = ()
    else:
        option_type = SCHEMA_TO_CLICK_TYPE_MAPPING.get(option_type, click.STRING)

    required = key in required_args and option_default is None

    is_flag = (option_type == click.BOOL)
    if is_flag and required:
        option_name = f"{option_name}/--no-{pretty_key}"

    if is_conditional:
        option_description += " [Conditional]"

    return Option(
        param_decls=[option_name],
        type=option_type,
        help=option_description,
        required=required,
        default=option_default,
        show_default=True,
        show_choices=True,
        is_flag=is_flag,
    )

def extract_options(schema, required_args, description, is_conditional=False, options_dict=None):
    """
    Recursively extract options from the schema, including conditional clauses.
    """
    if options_dict is None:
        options_dict = {}
    # Update the required_args with the required fields from this schema
    current_required_args = required_args | set(schema.get('required', []))

    if 'properties' in schema:
        for key, value in schema['properties'].items():
            option = _parse_option(key, value, current_required_args, description, is_conditional)
            # Avoid duplicates
            option_key = option.name
            options_dict[option_key] = option

    # Recursively process allOf, anyOf, oneOf, etc.
    for keyword in ['allOf', 'anyOf', 'oneOf']:
        if keyword in schema:
            for subschema in schema[keyword]:
                extract_options(subschema, current_required_args, description, is_conditional, options_dict)

    # Process conditional 'if-then' clauses
    if 'if' in schema and 'then' in schema:
        then_schema = schema['then']
        # Mark options in 'then' as conditional
        extract_options(then_schema, current_required_args, description, is_conditional=True, options_dict=options_dict)

    if 'else' in schema:
        else_schema = schema['else']
        # Options in 'else' can also be conditional
        extract_options(else_schema, current_required_args, description, is_conditional=True, options_dict=options_dict)

    return options_dict

def _get_flags_and_options(schema: dict, misc: dict = None, inst: bool = False) -> list[Option]:
    """
    Generates Click flags and options from a JSON schema.

    :param schema: Schema which contains the options.
    :param misc: Additional descriptions and pretty print names nested.
    :type schema: dict
    :param inst: Flag indicating if installation mode is active.
    :type inst: bool
    :return: List of all the Click options from the schema.
    :rtype: list[Option]
    """
    options = []
    alt_default = {}
    required_args = set(schema.get('required', []))

    description = misc.get("description", {}) if misc is not None else {}

    # Handle installation defaults if 'inst' is True
    change_default = False
    if inst:
        project_title = schema.get("$id")
        user_data_dir = platformdirs.user_data_dir("default_data_local", "installation_instruction")
        PATH_TO_DEFAULT_FILE = os.path.join(user_data_dir, "DEFAULT_DATA.json")
        default_data = {}
        if isfile(PATH_TO_DEFAULT_FILE):
            with open(PATH_TO_DEFAULT_FILE, "r") as f:
                default_data = json.load(f)
        if project_title in default_data.keys():
            default_data = default_data.get(project_title)
            change_default = True

    # Extract options recursively
    options_dict = extract_options(schema, required_args, description)

    for option in options_dict.values():
        # Adjust defaults based on installation mode
        key = option.name.lstrip('--').replace('-', '_')  # Convert to internal key format
        if change_default and key in default_data.keys():
            option.default = default_data.get(key)
            option.required = False  # Override required if default is present
        else:
            if not inst:
                # If not in installation mode, clear defaults and make optional
                option.default = None
                option.required = False

        options.append(option)

    if not inst:
        return options, alt_default
    return options

def handle_conditions(ctx, param, value):
    """
    Handle conditions to check if conditional options should be present.
    """
    # Convert any tuple values to lists
    for k, v in ctx.params.items():
        if isinstance(v, tuple):
            ctx.params[k] = list(v)

    return value
