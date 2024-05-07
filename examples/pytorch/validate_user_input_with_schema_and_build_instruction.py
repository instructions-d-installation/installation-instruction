try:
    from yaml import CLoader as Loader, CDumper as Dumper, load
except ImportError:
    from yaml import Loader, Dumper

from jsonschema import validate

from jinja2 import Environment, Template



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




schema = load_yml('instruction_pytorch.schema.yml')
input = load_yml('potential_user_input.yml')
#bad_input = load_yml('bad_user_input.yml')



print("Test valid input.")
validate(input, schema)
print("It worked!")


# print("Test invalid input.")
# validate(bad_input, schema)
# print("It worked!")


template = load_template("instruction_pytorch.md.jinja")

instructions = template.render(input)
print(instructions)
