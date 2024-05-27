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

from sys import exit
from os.path import isfile
from subprocess import run

import click

from .__init__ import __version__, __description__, __repository__, __author__, __author_email__, __license__
from .get_flags_and_options_from_schema import get_flags_and_options
from .installation_instruction import InstallationInstruction
from .helpers import _make_pretty_print_line_breaks

VERSION_STRING = f"""Version: installation-instruction {__version__}
Copyright: (C) 2024 {__author_email__}, {__author__}
License: {__license__}
Repository: {__repository__}"""


class ConfigReadCommand(click.MultiCommand):
    """
    Custom click command class to read config file and show installation instructions with parameters.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            subcommand_metavar="CONFIG_FILE [OPTIONS]...",
            options_metavar="",
        )

    def get_command(self, ctx, config_file: str) -> click.Command|None:

        # @Kanushka add here your logic. I thought of the following steps:
        # Check if config_file is an url.
        # If yes create a temporary dir. Or do something equivalent.
        # Find out if said url is a file or a git repo.
        # If is a file then download it to the temporary dir.
        # If is a git repo then clone it to the temporary dir and find the actual config file "install.cfg".
        # Overwrite config_file with the path to the config file.
        #
        # It be nice if you implement and use the `function helpers._find_config_file_in_folder`.
        # Please take a look into helpers.py for the functions definition.

        if not isfile(config_file):
            click.echo("Config file not found.")
            return None

        try:
            instruction = InstallationInstruction.from_file(config_file)
            options = get_flags_and_options(instruction.schema)
        except Exception as e:
            click.echo(click.style("Error (parsing options from schema): " + str(e), fg="red"))
            exit(1)


        def callback(**kwargs):
            inst = instruction.validate_and_render(kwargs)
            if inst[1]:
                click.echo(click.style("Error: " + inst[0], fg="red"))
                exit(1)
            if ctx.obj["MODE"] == "show":
                if ctx.obj["RAW"]:
                    click.echo(inst[0])
                else:
                    click.echo(_make_pretty_print_line_breaks(inst[0]))
            elif ctx.obj["MODE"] == "install":
                result = run(inst[0], shell=True, text=True, capture_output=True)
                if result.returncode != 0:
                    click.echo(click.style("Installation failed with:\n" + str(result.stdout) + "\n" + str(result.stderr), fg="red"))
                    exit(1)
                else:
                    if ctx.obj["INSTALL_VERBOSE"]:
                        click.echo(str(result.stdout))
                    click.echo(click.style("Installation successful.", fg="green"))

            exit(0)
            

        return click.Command(
            name=config_file,
            params=options,
            callback=callback,
        )


@click.command(cls=ConfigReadCommand, help="Shows installation instructions for your specified config file and parameters.")
@click.option("--raw", is_flag=True, help="Show installation instructions without pretty print.", default=False)
@click.pass_context
def show(ctx, raw):
    ctx.obj['MODE'] = "show"
    ctx.obj['RAW'] = raw

@click.command(cls=ConfigReadCommand, help="Installs with config and parameters given.")
@click.option("-v", "--verbose", is_flag=True, help="Show verbose output.", default=False)
@click.pass_context
def install(ctx, verbose):
    ctx.obj['MODE'] = "install"
    ctx.obj['INSTALL_VERBOSE'] = verbose

@click.group(context_settings={"help_option_names": ["-h", "--help"]}, help=__description__)
@click.version_option(version=__version__, message=VERSION_STRING)
@click.pass_context
def main(ctx):
    ctx.ensure_object(dict)

main.add_command(show)
main.add_command(install)

if __name__ == "__main__":
    main()