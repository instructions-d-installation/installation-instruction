
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
    pretty_key = key.replace('_', '-')
    option_name = f'--{pretty_key}'
    option_type = value.get('type', 'string')
    option_description = value.get('description', '') or description.get(key, "")
    option_default = value.get('default', None)

    if "enum" in value:
        # Replace spaces with underscores in enum values to match internal representations
        enum_choices = [item.replace(' ', '_') for item in value["enum"]]
        option_type = Choice(enum_choices, case_sensitive=False)
    elif option_type == 'array' and value.get('items', {}).get('enum'):
        choice_enum = [item.replace(' ', '_') for item in value['items']['enum']]
        option_type = Choice(choice_enum, case_sensitive=False, multiple=True)
        if option_default is None:
            option_default = ()
        elif isinstance(option_default, list):
            option_default = tuple(option_default)
        else:
            option_default = ()
    else:
        option_type = SCHEMA_TO_CLICK_TYPE_MAPPING.get(option_type, click.STRING)

    # For conditional options, set required based on 'required_args'
    # conditional options are not required unless specified
    required = key in required_args

    is_flag = (option_type == click.BOOL)
    if is_flag and required:
        option_name = f"{option_name}/--no-{pretty_key}"

    # Add a note to the description if it's a conditional option
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
    if 'allOf' in schema:
        for subschema in schema['allOf']:
            extract_options(subschema, current_required_args, description, is_conditional, options_dict)
    if 'anyOf' in schema:
        for subschema in schema['anyOf']:
            extract_options(subschema, current_required_args, description, is_conditional, options_dict)
    if 'oneOf' in schema:
        for subschema in schema['oneOf']:
            extract_options(subschema, current_required_args, description, is_conditional, options_dict)
    if 'then' in schema:
        # When entering a 'then' clause, set is_conditional to True
        extract_options(schema['then'], current_required_args, description, is_conditional=True, options_dict=options_dict)
    if 'else' in schema:
        extract_options(schema['else'], current_required_args, description, is_conditional, options_dict)

    return options_dict.values()


def _get_flags_and_options(schema: dict, misc: dict = None) -> list[Option]:
    """
    Generates Click flags and options from a JSON schema.
    :param schema: Schema which contains the options.
    :param misc: Additional descriptions and pretty print names nested.
    :type schema: dict
    :return: List of all the click options from the schema.
    :rtype: list[Option]
    """
    description = misc.get("description", {}) if misc is not None else {}
    required_args = set(schema.get('required', []))
    options = extract_options(schema, required_args, description)
    return list(options)

def handle_conditions(ctx, param, value):
    """
    Handle conditions to check if conditional options should be present.
    """
    # Convert any tuple values to lists
    for k, v in ctx.params.items():
        if isinstance(v, tuple):
            ctx.params[k] = list(v)

    # Additional custom validation can be added here if needed

    return value
