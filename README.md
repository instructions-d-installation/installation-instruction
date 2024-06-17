<div align="center">

# `installation-instruction`

**Library and CLI for generating installation instructions from json schema and jinja templates.**

[![GitHub License](https://img.shields.io/github/license/instructions-d-installation/installation-instruction)](./LICENSE)
[![PyPI - Version](https://img.shields.io/pypi/v/installation-instruction)](https://pypi.org/project/installation-instruction/)
[![Documentation Status](https://readthedocs.org/projects/installation-instruction/badge/?version=latest)](https://installation-instruction.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/instructions-d-installation/installation-instruction/graph/badge.svg?token=5AIH36HYG3)](https://codecov.io/gh/instructions-d-installation/installation-instruction)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Finstructions-d-installation%2Finstallation-instruction.svg?type=small)](https://app.fossa.com/projects/git%2Bgithub.com%2Finstructions-d-installation%2Finstallation-instruction?ref=badge_small)

</div>

## Installation

### [pipx](https://github.com/pypa/pipx)

```
pipx install installation-instruction
```


### pip

```
python -m pip install installation-instruction
```


### installation-instruction

*(Don't try at home.)*
```yaml
name: installation-instruction
type: object
properties:
  method:
    enum:
      - pipx
      - pip
----------------------------------
{% if method == "pip" %}
  python -m pip
{% else %}
  pipx
{% endif %}
  install installation-instruction
```


## CLI Usage

```
Usage: ibi [OPTIONS] COMMAND [ARGS]...

  Library and CLI for generating installation instructions from json schema
  and jinja templates.

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  install  Installs with config and parameters given.
  show     Shows installation instructions for your specified config file...
```

Options are dynamically created with the schema part of the config file.   

> [!TIP]
> Show help for a config file with: `ibi show CONFIG_FILE/FOLDER/GIT_REPO_URL --help`.


## Config

* The config is comprised of a single file `install.cfg`.
* The config has two parts delimited by `------` (6 or more `-`).
* Both parts should be developed in different files for language server support.


### Schema

* The first section of the config is a [json-schema](https://json-schema.org/).
* It can be written in [JSON](https://www.json.org/json-en.html) or to JSON capabilites restricted [YAML](https://yaml.org/).
* When creating a schema use the following schema draft version: https://json-schema.org/draft/2020-12/schema
* `title` are used for pretty print option names.
* `description` is used for the options help message.
* For adding a description and a pretty print name to enum values (for [web-installation-instruction](https://github.com/instructions-d-installation/web-installation-instruction)):
  1. Indent the schema with the key `schema`.
  2. Add `pretty` and `description` keys.
  3. Create lists like `key: Pretty Key`.
* `title` and `description` from within the schema overwrite `pretty` and `description` outside of the schema.

```yaml
schema:
  name: installation-instruction
  type: object
  properties:
    method:
      enum:
        - pipx
        - pip
pretty:
  pipx: Pipx
  pip: Pip
description:
  pipx: Installs python packages into virtual environments.
  pip: Standard python package manager.
```


### Template

* You can have as much whitespace and line breaks as you wish in and inbetween your commands.
* Commands must be seperated by `&&`! (`pip install installation-instruction && pip uninstall installation-instruction`.)
* If you wish to stop the render from within the template you can use the macro `raise`. (`{{ raise("no support!") }}`.) 


### MISC

Please have a look at the [examples](./examples/).


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

* [Adam McKellar](https://github.com/WyvernIXTL) ([dev@mckellar.eu](mailto:dev@mckellar.eu))
* [Kanushka Gupta](https://github.com/KanushkaGupta)
* [Timo Ege](https://github.com/TimoEg) ([timoege@online.de](mailto:timoege@online.de))


## Acknowledgments

This repository was set up using the [SSC Cookiecutter for Python Packages](https://github.com/ssciwr/cookiecutter-python-package).


## License Scan

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Finstructions-d-installation%2Finstallation-instruction.svg?type=large&issueType=license)](https://app.fossa.com/projects/git%2Bgithub.com%2Finstructions-d-installation%2Finstallation-instruction?ref=badge_large&issueType=license)
