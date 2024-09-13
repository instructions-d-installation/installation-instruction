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
import os
import click
import json

from .__init__ import __version__, __description__, __repository__, __author__, __author_email__, __license__
from .get_flags_and_options_from_schema import _get_flags_and_options
from .installation_instruction import InstallationInstruction
from .helpers import _make_pretty_print_line_breaks, _is_remote_git_repository, _clone_git_repo, _config_file_is_in_folder


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

def _red_echo(text: str):
    click.echo(click.style(text, fg="red"))


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

        temp_dir = None
        if _is_remote_git_repository(config_file):
            try:
                temp_dir = _clone_git_repo(config_file)
            except Exception as e:
                _red_echo("Error (cloning git repository):\n\n" + str(e))
                exit(1)
            config_file = temp_dir.name
        if isdir(config_file):
            if path := _config_file_is_in_folder(config_file):
                config_file = path
            else:
                if temp_dir is not None:
                    _red_echo("Config file not found in repository.")
                else:
                    _red_echo(f"Config file not found in folder {config_file}")
                exit(1)
        if not isfile(config_file):
            _red_echo(f"{config_file} is not a file.")
            exit(1)
        
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
    
class ConfigCommandGroup(click.Group):
    """
    Custom click command group class for default commands with subcommands.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            subcommand_metavar="CONFIG_FILE/FOLDER/GIT_REPO_URL [OPTIONS]...",
            options_metavar="",
        )

    def get_command(self, ctx, config_file: str , **kwargs) -> click.Command|None:
        click.echo(kwargs)
        temp_dir = None
        if _is_remote_git_repository(config_file):
            try:
                temp_dir = _clone_git_repo(config_file)
            except Exception as e:
                _red_echo("Error (cloning git repository):\n\n" + str(e))
                exit(1)
            config_file = temp_dir.name
        if isdir(config_file):
            if path := _config_file_is_in_folder(config_file):
                config_file = path
            else:
                if temp_dir is not None:
                    _red_echo("Config file not found in repository.")
                else:
                    _red_echo(f"Config file not found in folder {config_file}")
                exit(1)
        if not isfile(config_file):
            _red_echo(f"{config_file} is not a file.")
            exit(1)
        
        try:
            instruction = InstallationInstruction.from_file(config_file)
            options = _get_flags_and_options(instruction.schema, getattr(instruction, "misc", None))
        except Exception as e:
            _red_echo("Error (parsing options from schema): " + str(e))
            exit(1)

        def callback(**kwargs):
            schema = instruction.parse_schema()
            with open("installation_instruction\PATH_TO_DEAFAULT_FILE.json", "r") as f:
                PATH_TO_DEFAULT_FILE = json.load(f)
            if ctx.obj["MODE"] == "add":
                new_file= False
                if not isfile(PATH_TO_DEFAULT_FILE):
                    PATH_TO_DEFAULT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),"DEFAULT_DATA.json")
                    with open("installation_instruction\PATH_TO_DEAFAULT_FILE.json", "w") as f:
                        json.dump(PATH_TO_DEFAULT_FILE,f)
                    click.echo(f"successfully created a new file at:")
                    click.echo(PATH_TO_DEFAULT_FILE)
                    new_file = True
                #if not new_file:
                    #given_param = {k for k in kwargs.items() if ctx.get_parameter_source(k) == click.core.ParameterSource.COMMANDLINE}
                default_data = {}
                if not new_file:
                    with open(PATH_TO_DEFAULT_FILE,"r") as f:
                        default_data = json.load(f)
                title = schema.get("title")
                new_project = True
                if title in default_data.keys():
                    new_project = False
                defaults_settings = {}
                if not new_project:
                    defaults_settings = default_data.get(title)
                
                for option in options:
                    if option.name in kwargs.keys():
                        if type(option.type) == click.Choice:
                            if kwargs.get(option.name) in option.type.choices:
                                defaults_settings[option.name]= kwargs.get(option.name)
                            else:
                                _red_echo(f"There is no {kwargs.get(option.name)} option in {option.name}")
                        else:
                            if type(option.type)== click.types.StringParamType:
                                defaults_settings[option.name]= kwargs.get(option.name)
                            elif type(option.type)== click.types.IntParamType:
                                defaults_settings[option.name]= kwargs.get(option.name)
                            elif type(option.type)== click.types.FloatParamType:
                                defaults_settings[option.name]= kwargs.get(option.name)
                            elif type(option.type)== click.types.BoolParamType:
                                defaults_settings[option.name] = kwargs.get(option.name, False)
                    elif new_project:
                        if option.required:
                            if option.default:
                                defaults_settings[option.name]= option.default
                            else:
                                if type(option.type)== click.types.Choice:
                                    defaults_settings[option.name]= option.type.choices[0]
                                elif type(option.type)== click.STRING:
                                    defaults_settings[option.name]=" "
                                elif type(option.type)== click.INT:
                                    defaults_settings[option.name]= 1
                                elif type(option.type)== click.FLOAT:
                                    defaults_settings[option.name]= 1.0
                                elif type(option.type)== click.BOOL:
                                    defaults_settings[option.name]= False
                
                default_data[title] = defaults_settings
                with open(PATH_TO_DEFAULT_FILE,"w") as f:
                    json.dump(default_data, f,indent= 4)
                if new_file:
                    click.echo("successfully created a new default file.")
                if new_project:
                    click.echo(f"successfully added {title} to the default_data.")
                else:
                    click.echo(f"successfully applied changes to {title} in the default_data.")

            elif ctx.obj["MODE"] == "remove":
                if not isfile(PATH_TO_DEFAULT_FILE):
                    _red_echo(f"There exists no Default File to remove from.")
                    exit(1)
                
                with open(PATH_TO_DEFAULT_FILE,"r") as f:
                    default_data = json.load(f)
                title = schema.get("title")
                deleted_item = default_data.pop(title,None)
                if not deleted_item:
                    _red_echo(f"There exists no project to remove.")
                else:
                    with open(PATH_TO_DEFAULT_FILE,"w") as f:
                        json.dump(default_data, f,indent=4)
                    click.echo(f"successfully deleted {title} from the default_data.") 
                    if not default_data:
                        os.remove(PATH_TO_DEFAULT_FILE)
                        click.echo(f"removed default file as it was empty.") 

            elif ctx.obj["MODE"] == "list":
                if not isfile(PATH_TO_DEFAULT_FILE):
                    _red_echo(f"There exists no default file to list projects from.")
                    exit(1)
                with open(PATH_TO_DEFAULT_FILE,"r") as f:
                    default_data = json.load(f)
                
                title = schema.get("title")
                if not default_data.get(title,False):
                    click.echo(f"{title} has no entry in the default file.")
                else:
                    click.echo(f"{title} has the following default configurations:")
                    click.echo(default_data.get(title))
            
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

@click.group( context_settings={"help_option_names": ["-h", "--help"]}, help="Default command to create custom default settings with add, remove, and list.")
@click.pass_context
def default(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('default needs a subcommand.(add, remove or list)')

@default.command(cls=ConfigCommandGroup,help="Add a new project configuration or change existing ones.")
@click.pass_context
def add(ctx):
    ctx.obj['MODE'] = "add"

@default.command(cls=ConfigCommandGroup, help="Remove an existing default configuration of a project.")
@click.pass_context
def remove(ctx):
    ctx.obj['MODE'] = "remove"

@default.command(cls=ConfigCommandGroup, help="Lists default configurations of a project.")
@click.pass_context
def list(ctx):
    ctx.obj['MODE'] = "list"

@click.group(context_settings={"help_option_names": ["-h", "--help"]}, help=__description__)
@click.version_option(version=__version__, message=VERSION_STRING)
@click.pass_context
def main(ctx):
    ctx.ensure_object(dict)

main.add_command(show)
main.add_command(install)
main.add_command(default)

if __name__ == "__main__":
    main()
    
