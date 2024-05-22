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


def _make_pretty_print_line_breaks(string: str) -> str:
    return re.sub(r"\s?&&\s?", "\n", string, 0, re.S)

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

def _replace_whitespace_in_string(string: str) -> str:
    """
    Replaces eol and whitespaces of a string with a single whitespace.

    :param string: String to be processed.
    :type string: str
    :return: String where whitespace and eol is replaced with one whitespace and whitspace before and after are stripped.
    :rtype: str
    """
    return re.sub(r"\s{1,}", " ", string, 0, re.S).strip()

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
    env = Environment(
        trim_blocks=True,
        lstrip_blocks=True
    )
    return env.from_string(string)
