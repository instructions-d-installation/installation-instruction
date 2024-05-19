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

from sys import argv, exit
from os.path import isfile

import click

from .get_flags_and_options_from_schema import get_flags_and_options
from .installation_instruction import InstallationInstruction


class ConfigReadCommand(click.MultiCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            subcommand_metavar="CONFIG [OPTIONS]...",
            options_metavar="",
        )

    def get_command(self, ctx, config_file: str) -> click.Command:
        if not isfile(config_file):
            print("Config file not found.")
            exit(1)

        instruction = InstallationInstruction.from_file(config_file)
        options = get_flags_and_options(instruction.schema)

        def callback(**kwargs):
            inst = instruction.validate_and_render(kwargs)
            if not inst[1]:
                print(inst[0])
                exit(0)
            else:
                print(inst[0])
                exit(1)

        return click.Command(
            name=config_file,
            params=options,
            callback=callback,
        )


@click.command(cls=ConfigReadCommand)
def main():
    pass


if __name__ == "__main__":
    main()