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
from os.path import isfile, isdir
from subprocess import run
import platform

import click
from yaml import safe_dump

from .__init__ import __version__, __description__, __repository__, __author__, __author_email__, __license__
from .get_flags_and_options_from_schema import _get_flags_and_options
from .installation_instruction import InstallationInstruction
from .helpers import _make_pretty_print_line_breaks, _red_echo, _get_install_config_file


VERSION_STRING = f"""Version: installation-instruction {__version__}
Copyright: (C) 2024 {__author_email__}, {__author__}
License: {__license__}
Repository: {__repository__}"""

def _get_system(option_types):
    """
    Returns the os from the list of possible os systems defined in the schema.

    :param option_types: list of system from the schema.
    :type option_types: list
    :return: os system from input list or None.
    :rtype: string or None
    """    
    
    system = platform.system()
    system_names = {
        'Linux': 'linux',
        'Darwin': 'mac',
        'Windows': 'win',
    }
    
    new_default = system_names.get(system,None)
    for type in option_types:
        if new_default in type.lower(): 
            return type

    return None


class ConfigReadCommand(click.MultiCommand):
    """
    Custom click command class to read config file, folder or git repository and show installation instructions with parameters.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            subcommand_metavar="CONFIG_FILE/FOLDER/GIT_REPO_URL [OPTIONS]...",
            options_metavar="",
        )


    def get_command(self, ctx, config_file: str) -> click.Command|None:

        (_temp_dir, config_file) = _get_install_config_file(config_file)
        
        try:
            instruction = InstallationInstruction.from_file(config_file)
            options = _get_flags_and_options(instruction.schema, getattr(instruction, "misc", None))
        except Exception as e:
            _red_echo("Error (parsing options from schema): " + str(e))
            exit(1)

        #set new default value for __os__ Option
        for option in options:
            if '__os__' in option.name:
                system_default = _get_system(option.type.choices)
                if system_default:
                    option.default = system_default

        def callback(**kwargs):
            inst = instruction.validate_and_render(kwargs)
            if inst[1]:
                _red_echo("Error: " + inst[0])
                exit(1)
            if ctx.obj["MODE"] == "show":
                if ctx.obj["RAW"]:
                    click.echo(inst[0])
                else:
                    click.echo(_make_pretty_print_line_breaks(inst[0]))
            elif ctx.obj["MODE"] == "install":
                result = run(inst[0], shell=True, text=True, capture_output=True)
                if result.returncode != 0:
                    _red_echo("Installation failed with:\n" + str(result.stdout) + "\n" + str(result.stderr))
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

@click.command(help="Shows source of installation instructions config file.")
@click.argument("path")
def cat(path):
    (_temp_dir, config_file) = _get_install_config_file(path)
    with open(config_file, "r") as file:
        config_string = file.read()
    print(config_string)

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

main.add_command(cat)
main.add_command(show)
main.add_command(install)

if __name__ == "__main__":
    main()
    
