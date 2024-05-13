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

def get_flags_and_options(schema: dict) -> list:
    """
    Generates Click flags and options from a JSON schema.

    :param schema: schema which contains the options
    :type ditcionary: dict
    :return: list of all the clickoptions from the schema
    :rtype: list
    """
    options = []
    required_args = set(schema.get('required', []))

    for key, value in schema.get('properties', {}).items():
        option_name = '--{}'.format(key)
        option_type = value.get('type', 'string')
        option_description = value.get('description', '')

        if 'anyOf' in value:
            type_options = [t['title'] for t in value['anyOf'] if 'title' in t]
            option_description = '\n'.join(type_options)

        if option_type == 'string':
            option_type = click.STRING
        elif option_type == 'integer':
            option_type = click.INT
        elif option_type == 'number':
            option_type = click.FLOAT
        elif option_type == 'boolean':
            option_type = click.BOOL
        else:
            option_type = click.STRING

        required = False
        if key in required_args:
            required = True

        options.append({
            'name': option_name,
            'type': option_type,
            'description': option_description,
            'required': required
        })

    return options