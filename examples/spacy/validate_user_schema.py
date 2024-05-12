try:
    from yaml import CLoader as Loader, CDumper as Dumper, load
except ImportError:
    from yaml import Loader, Dumper

from jsonschema import validate

from jinja2 import Template



def load_yml(path: str) -> dict:
    with open(path, 'r') as file:
        input_str = file.read()
        
    return load(input_str, Loader=Loader)

def load_template(path: str) -> Template:
    with open(path, 'r') as file:
        template_str = file.read()

    return Template(template_str)




schema = load_yml('instruction_spacy.schema.yml')
input = load_yml('user_input_2.yml')


print("Test valid input.")
validate(input, schema)
print("It worked!")



template = load_template("instruction_spacy.md.jinja")

instructions = template.render(input)
print(instructions)
