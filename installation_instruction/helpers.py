
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

from tempfile import TemporaryDirectory
import os.path
from os.path import isfile, isdir
import re

from jinja2 import Template
from jinja2.sandbox import SandboxedEnvironment

import click
import git

CONFIG_FILE_NAME = "install.cfg"
ALLOWED_GIT_URL_PREFIXES = ["http://", "https://", "git://", "ssh://", "ftp://", "ftps://"]

def _red_echo(text: str):
    click.echo(click.style(text, fg="red"))

def _is_remote_git_repository(url: str) -> bool:
    """
    Checks if the given URL might be a remote git repository.

    todo: Make this more robust. Check if it is actually a valid git repository by calling it.

    :param url: URL to be checked.
    :type url: str
    :return: True if the URL is a remote git repository, else False.
    :rtype: bool
    """
    return any([url.startswith(prefix) for prefix in ALLOWED_GIT_URL_PREFIXES])

def _clone_git_repo(url: str) -> TemporaryDirectory:
    """
    Clones a git repository to a temporary directory.

    :param url: URL of the remote git repository.
    :type url: str
    :return: `TemporaryDirectory` object with git repo.
    :rtype: tempfile.TemporaryDirectory
    """
    temp_dir = TemporaryDirectory()
    git.Repo.clone_from(url, temp_dir.name, multi_options=["--depth=1"])
    return temp_dir
    
def _config_file_is_in_folder(dir_path: str) -> str | None:
    """
    Checks if the file `install.cfg` is in the folder.

    :param dir_path: Path to the folder.
    :type dir_path: str
    :return: Path to the `install.cfg` file if it exists, else None.
    :rtype: str or None
    """
    install_cfg_path = os.path.join(dir_path, CONFIG_FILE_NAME)
    if os.path.isfile(install_cfg_path):
        return install_cfg_path
    return None

def _get_install_config_file(path: str) -> tuple[TemporaryDirectory|None, str]:
    """
    Checks wether path is a git url or a dir, finds the config file and asserts that said file is a file.

    :param path: Url, path to dir or file.
    :type path: str
    :return: Returns a tuple with a temporary dir needed for cloning a git repository (on distruction temporary dir is deleted), and the found config file path.
    :rtype: tuple[TemporaryDirectory|None, str]
    """
    config_file = path
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

    return (temp_dir, config_file)

def _get_error_message_from_string(string: str) -> str | None:
    """
    Parses error message of error given by using jinja macro `RAISE_JINJA_MACRO_STRING`. If no error message is found returns `None`.

    :param string: This is the raw error string where an error message might be.
    :type string: str
    :return: Error message if found else None.
    :rtpye: str or None
    """
    reg = re.compile(r"^.*\'\[ERROR\]\s*(?P<errmsg>.*?)\s*\'.*$", re.S)
    matches = reg.search(string)
    if matches is None:
        return None
    return matches.group("errmsg")

def _replace_whitespace_in_string_and_split_it(string: str) -> list[str]:
    """
    Replaces eol whitespaces of a string with a single whitespace or none.

    :param string: String to be processed.
    :type string: str
    :return: String where whitespace is replaced with one whitespace and whitspace before and after are stripped.
    :rtype: str
    """
    multiline_string = str.splitlines(string)
    string_list = []
    for s in multiline_string:
        s = s.strip()
        if s:
            string_list += [re.sub(r"\s{2,}", " ", s, 0)]
    return string_list

def _split_string_at_delimiter(string: str) -> tuple[str, str]:
    """
    Extracts part before and after the delimiter "------" or more.

    :param string: The string with a delimiter.
    :type string: str
    :raise Exception: If no delimiter is found.
    :return: Returns a tuple with the part before and after the delimiter.
    :rtype: tuple[str, str]
    """
    reg = re.compile(r"^\s*(?P<schema>.*?)\s*\-{6,}\s*(?P<template>.*?)\s*$", re.S)
    matches = reg.search(string)
    if matches is None:
        raise Exception("No delimiter (------) found.")
    return (
                matches.group("schema"),
                matches.group("template")
            )

def _load_template_from_string(string: str) -> Template:
    """
    Returns `jinja2.Template`.

    :param string: String to be processed.
    :type string: str
    :return: jinja2 Template object.
    :rtype: jinja2.Template
    """
    env = SandboxedEnvironment(
        trim_blocks=True,
        lstrip_blocks=True
    )
    return env.from_string(string)