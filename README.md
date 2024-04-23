# Welcome to installation-instruction

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/None/badge/)](https://None.readthedocs.io/)
[![codecov](https://codecov.io/none/None/None/branch/main/graph/badge.svg)](https://codecov.io/none/None/None)

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

## Acknowledgments

This repository was set up using the [SSC Cookiecutter for Python Packages](https://github.com/ssciwr/cookiecutter-python-package).
