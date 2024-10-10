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


"""
Code of the click custom commands `install`, `show` and `default`.
The commands `install` and `show` are ConfigReadCommand instances
while the subcommands `add`, `remove` and `list` from the multi command default 
are ConfigCommandGroup instances.
"""

from sys import exit
from os.path import isfile, isdir
from subprocess import run
import os
import click
import json
import platformdirs
import platform

from .__init__ import __version__, __description__, __repository__, __author__, __author_email__, __license__
from .get_flags_and_options_from_schema import _get_flags_and_options
from .installation_instruction import InstallationInstruction
from .helpers import _red_echo, _get_install_config_file


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
            options = _get_flags_and_options(instruction.schema, getattr(instruction, "misc", None),inst=True)
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
                _red_echo("Error: " + "\n".join(inst[0]))
                exit(1)
            if ctx.obj["MODE"] == "show":
                click.echo("\n".join(inst[0]))
            elif ctx.obj["MODE"] == "install":
                for command in inst[0]:
                    result = run(command, shell=True, text=True, capture_output=True)
                    if result.returncode != 0:
                        _red_echo("Installation failed with:\n" + command + "\n\n" + result.stdout + "\n" + result.stderr)
                        exit(1)
                    else:
                        if ctx.obj["INSTALL_VERBOSE"]:
                            click.echo(result.stdout.strip())
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
        
        (_temp_dir, config_file) = _get_install_config_file(config_file)

        user_data_dir = platformdirs.user_data_dir("default_data_local","installation_instruction")
        os.makedirs(user_data_dir, exist_ok=True)
        PATH_TO_DEFAULT_FILE = os.path.join(user_data_dir, "DEFAULT_DATA.json")
        ctx.obj['path'] = PATH_TO_DEFAULT_FILE
        default_data = {}
        if isfile(PATH_TO_DEFAULT_FILE):
            with open(PATH_TO_DEFAULT_FILE,"r") as f:
                default_data = json.load(f)
            ctx.obj['default_data'] = default_data
            ctx.obj['new_file'] = False
        else:
            ctx.obj['new_file'] = True
        try:
            instruction = InstallationInstruction.from_file(config_file)
            schema = instruction.parse_schema()
            title = schema.get("$id")
            ctx.obj['title'] = title
            options, ctx.obj['defaults'] = _get_flags_and_options(instruction.schema, getattr(instruction, "misc", None)) 
        except Exception as e:
            _red_echo("Error (parsing options from schema): " + str(e))
            exit(1)

        def callback(**kwargs):
            new_file = ctx.obj['new_file']
            PATH_TO_DEFAULT_FILE = ctx.obj['path']
            if ctx.obj["MODE"] == "add":
                orig_default = ctx.obj['defaults']
                default_data = {}
                if not new_file:
                    with open(PATH_TO_DEFAULT_FILE,"r") as f:
                        default_data = json.load(f)
                title = ctx.obj['title']
                exist_project = title in default_data.keys()
                defaults_settings = {}
                if exist_project:
                    defaults_settings = default_data.get(title)
                for option in options:
                    if option.name in kwargs.keys():
                        if kwargs.get(option.name) == None:
                            pass
                        elif type(option.type) == click.Choice:
                            if kwargs.get(option.name) in option.type.choices:
                                defaults_settings[option.name]= kwargs.get(option.name)
                            else:
                                _red_echo(f"There is no {kwargs.get(option.name)} option in {option.name}")
                        else:
                            if type(option.type)== click.types.StringParamType:
                                defaults_settings[option.name]= kwargs.get(option.name)
                            elif type(option.type)== click.types.IntParamType:
                                try:
                                    def_val = int(kwargs.get(option.name))
                                except ValueError:
                                    _red_echo(f"{kwargs.get(option.name)} is no int!")
                                    exit(1)
                                defaults_settings[option.name]= def_val
                            elif type(option.type)== click.types.FloatParamType:
                                try:
                                    def_val = float(kwargs.get(option.name))
                                except ValueError:
                                    _red_echo(f"{kwargs.get(option.name)} is no float!")
                                    exit(1)
                                defaults_settings[option.name]= def_val
                            elif type(option.type)== click.types.BoolParamType:
                                if defaults_settings.get(option.name) == True:
                                    defaults_settings[option.name] = False
                                else:
                                    defaults_settings[option.name] = kwargs.get(option.name, False)
                remove = []
                for key in defaults_settings.keys():
                    if str(defaults_settings.get(key)) == str(orig_default.get(key)):
                        remove.append(key)
                for key in remove:
                    defaults_settings.pop(key)
                if defaults_settings:
                    default_data[title] = defaults_settings
                else:
                    default_data.pop(title)
                if not default_data:
                    os.remove(PATH_TO_DEFAULT_FILE)
                    click.echo(f"removed default file as all setting were the same like the defaults of the developer.") 
                else:
                    with open(PATH_TO_DEFAULT_FILE,"w") as f:
                        json.dump(default_data, f,indent= 4)
                    if new_file:
                        click.echo("successfully created a new default file at:")
                        click.echo(PATH_TO_DEFAULT_FILE)
                    if exist_project:
                        click.echo(f"successfully added {title} to the default_data.")
                    else:
                        click.echo(f"successfully applied changes to {title} in the default_data.")

            elif ctx.obj["MODE"] == "remove":
                if not isfile(PATH_TO_DEFAULT_FILE):
                    _red_echo(f"There exists no Default File to remove from.")
                    exit(1)
                
                with open(PATH_TO_DEFAULT_FILE,"r") as f:
                    default_data = json.load(f)
                title = ctx.obj['title']
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
                
                title = ctx.obj['title']
                if not default_data.get(title,False):
                    click.echo(f"{title} has no entry in the default file.")
                else:
                    click.echo("")
                    click.echo(f"{title} has the following user default configurations:")
                    click.echo("")
                    dic = default_data.get(title)
                    for i in dic.keys():
                        click.echo(f"{i}: {dic.get(i)}")
                    click.echo("")
            
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
@click.pass_context
def show(ctx):
    ctx.obj['MODE'] = "show"

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

main.add_command(cat)
main.add_command(show)
main.add_command(install)
main.add_command(default)

if __name__ == "__main__":
    main()
    
