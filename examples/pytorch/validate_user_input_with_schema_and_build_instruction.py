try:
    from yaml import CLoader as Loader, CDumper as Dumper, load
except ImportError:
    from yaml import Loader, Dumper

from jsonschema import validate

from jinja2 import Environment, Template

import re


def load_yml(path: str) -> dict:
    with open(path, 'r') as file:
        input_str = file.read()
        
    return load(input_str, Loader=Loader)

def load_template(path: str) -> Template:
    with open(path, 'r') as file:
        template_str = file.read()

    env = Environment(
        trim_blocks=True,
        lstrip_blocks=True
    )

    return env.from_string(template_str)

def get_error_message(parsed_template: str) -> str|None:
    reg = re.compile(".*\[\[ERROR\]\]\s*(?P<errmsg>.*?)\s*\[\[ERROR\]\].*", re.S)
    matches = reg.search(parsed_template)
    if matches is None:
        return None
    return matches.group("errmsg")

def replace_blank_space(string: str) -> str:
    return re.sub("\s{1,}", " ", string, 0, re.S).strip()


schema = load_yml('instruction_pytorch.schema.yml')
input = load_yml('potential_user_input.yml')



print("Test valid input.")
validate(input, schema)
print("It worked!")

template = load_template("instruction_pytorch.txt.jinja")

instructions = template.render(input)
instructions = replace_blank_space(instructions)

if errmsg := get_error_message(instructions):
    print(errmsg)
else:
    print(instructions)