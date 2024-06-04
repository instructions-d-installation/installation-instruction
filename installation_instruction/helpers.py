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

import re
from jinja2 import Environment, Template

from urllib.parse import urlparse
import git
import tempfile
import shutil
import os

def is_git_repo_url(url):
    parsed_url = urlparse(url)
    return all([parsed_url.scheme, parsed_url.netloc, parsed_url.path]) and url.endswith('.git')

def clone_git_repo(url):
    # Create a temporary directory
    temp_dir = tempfile.TemporaryDirectory()
    repo_dir = temp_dir.name
    git.Repo.clone_from(url, repo_dir)
    return repo_dir, temp_dir
    
def check_and_download_install_cfg(repo_dir):
    install_cfg_path = os.path.join(repo_dir, 'install.cfg')
    if os.path.isfile(install_cfg_path):
        temp_file_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_file_dir, 'install.cfg')
        shutil.copy(install_cfg_path, temp_file_path)
        return temp_file_path, temp_file_dir
    return None, None

def _find_config_file_in_folder(folder_path: str) -> str | None:
    """
    Finds file with the name `install.cfg` in the folder and returns its path if it exists.
    """
    if folder_path.startswith('http://') or folder_path.startswith('https://'):
        # It's a URL, handle it accordingly
        repo_dir, temp_dir = clone_git_repo(folder_path)
        install_cfg_path, install_cfg_temp_dir = check_and_download_install_cfg(repo_dir)
        if install_cfg_path:
            print(f"install.cfg found and downloaded to: {install_cfg_path}")
            return install_cfg_path
        else:
            print("install.cfg not found in the repository root.")
        # Clean up the cloned repository
        temp_dir.cleanup()
    elif os.path.isfile(folder_path):
        return folder_path
    return folder_path

def make_pretty_print_line_breaks(string):
    """
    Replaces `&& ` with a newline character.

    :param string: String to be processed.
    :type string: str
    :return: String with `&& ` replaced with newline character.
    :rtype: str
    """
    return re.sub(r"\s?&&\s?", "\n", string, 0, re.S)

def get_error_message_from_string(string):
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

def replace_whitespace_in_string(string):
    """
    Replaces eol and whitespaces of a string with a single whitespace.

    :param string: String to be processed.
    :type string: str
    :return: String where whitespace and eol is replaced with one whitespace and whitespace before and after are stripped.
    :rtype: str
    """
    return re.sub(r"\s{1,}", " ", string, 0, re.S).strip()

def split_string_at_delimiter(string):
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

def load_template_from_string(string):
    """
    Returns `jinja2.Template`.

    :param string: String to be processed.
    :type string: str
    :return: jinja2 Template object.
    :rtype: jinja2.Template
    """
    env = Environment(
        trim_blocks=True,
        lstrip_blocks=True
    )
    return env.from_string(string)


_find_config_file_in_folder('https://github.com/KanushkaGupta/sample.git')