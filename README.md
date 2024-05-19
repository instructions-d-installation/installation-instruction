<div align="center">

# `installation-instruction`

**Library for checking and parsing installation instruction schemas.**

![GitHub License](https://img.shields.io/github/license/instructions-d-installation/installation-instruction)
[![Documentation Status](https://readthedocs.org/projects/installation-instruction/badge/?version=latest)](https://installation-instruction.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/instructions-d-installation/installation-instruction/graph/badge.svg?token=5AIH36HYG3)](https://codecov.io/gh/instructions-d-installation/installation-instruction)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Finstructions-d-installation%2Finstallation-instruction.svg?type=small)](https://app.fossa.com/projects/git%2Bgithub.com%2Finstructions-d-installation%2Finstallation-instruction?ref=badge_small)

</div>

## CLI Usage

```
Usage: ibi [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  show  Shows installation instructions for your specified config file...
```

Options are dynamically created with the schema part of the config file.   

> [!TIP]
> Show help for a config file with: `ibi show CONFIG_FILE --help`.


## Config

The config is comprised of a single file. (Currently there is no fixed filename.) 
For ease of use you should use the file extension `.yml.jinja` and develope said config file as two seperate files at first.
The config file has two parts delimited by `------` (6 or more `-`).   
The first part is the schema (*What is valid user input?*). The second part is the template (*What is the actual command for said user input?*).
The first part must be a valid [JSON Schema](https://json-schema.org/) in [JSON](https://www.json.org/json-en.html) or to JSON capabilites restricted [YAML](https://yaml.org/) and the second part must be a valid [jinja2 template](https://jinja.palletsprojects.com/en/3.0.x/templates/).
The exception to this is that `anyOf` and `oneOf` are only usable for enum like behaviour on the schema side.
Instead of an `enum` you might want to use `anyOf` with `const` and `tile` properties.
The `title` of a property is used for the pretty print name, while the `description` is used for the help message.
There exists a jinja2 macro called `raise`, which is usefull if there is actually no installation instruction for said user input.
All lineends in the template are removed after render, which means that commands can be splitted within the template (`conda install {{ "xyz" if myvar else "abc" }}` ).
This also means that multiple commands need to be chained via `&&`.
For examples please look at the [examples folder](./examples/).


## Installation

The Python package `installation_instruction` can be installed from PyPI:

```
python -m pip install installation_instruction
```

## Development installation

If you want to contribute to the development of `installation_instruction`, we recommend
the following editable installation from this repository:

```
python -m pip install --editable .[tests]
```

Having done so, the test suite can be run using `pytest`:

```
python -m pytest
```

## Contributors

* [Adam McKellar](https://github.com/WyvernIXTL) [dev@mckellar.eu](mailto:dev@mckellar.eu)
* [Kanushka Gupta](https://github.com/KanushkaGupta)
* [Timo Ege](https://github.com/TimoEg) [Timoege@online.de](mailto:Timoege@online.de)


## Acknowledgments

This repository was set up using the [SSC Cookiecutter for Python Packages](https://github.com/ssciwr/cookiecutter-python-package).


## License Scan

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Finstructions-d-installation%2Finstallation-instruction.svg?type=large&issueType=license)](https://app.fossa.com/projects/git%2Bgithub.com%2Finstructions-d-installation%2Finstallation-instruction?ref=badge_large&issueType=license)
