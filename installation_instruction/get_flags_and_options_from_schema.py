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

def _get_flags_and_options(schema: dict) -> list[Option]:
    """
    Generates Click flags and options from a JSON schema.

    :param schema: Schema which contains the options.
    :type schema: dict
    :return: List of all the clickoptions from the schema.
    :rtype: list[Option]
    """
    options = []
    required_args = set(schema.get('required', []))

    for key, value in schema.get('properties', {}).items():
        orig_key = key
        key = key.replace('_', '-').replace(' ', '-')
        option_name = '--{}'.format(key)
        option_type = value.get('type', 'string')
        option_description = value.get('description', '')
        option_default = value.get('default', None)

        if 'anyOf' in value:
            option_type = Choice( [c['const'] for c in value['anyOf'] if 'const' in c] )
        elif "enum" in value:
            option_type = Choice( value["enum"] )
        else:
            option_type = SCHEMA_TO_CLICK_TYPE_MAPPING.get(option_type, click.STRING)

        required = (orig_key in required_args) and option_default is None
        is_flag=(option_type == click.BOOL)
        if is_flag and required:
            option_name = option_name + "/--no-{}".format(key)

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

    return options