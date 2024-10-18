# CLI Usage

```
Usage: ibi [OPTIONS] COMMAND [ARGS]...

  Library and CLI for generating installation instructions from json schema
  and jinja templates.

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  cat      Shows source of installation instructions config file.
  install  Installs with config and parameters given.
  show     Shows installation instructions for your specified config file...

```


## `ibi`

The cli name is `ibi`. All its subcommands take as first argument a path to a config file (`install.cfg`), a path to a folder with such config file or
an url to a git repository with a config file in its root.


### `cat`

`cat` prints the the entire `install.cfg` as output into the terminal.

### `install`

`install` takes the user input parmeters and installs the package with the user specifications.

### `show`

`show` takes the user input parmeters and prints the installation commands into the terminal without executing them.

### `default`

`default` is used to safe default settings specified by the user.

#### `add`

`add` safes and changes custom default settings of a user to a json file. 

#### `list`

`list` prints all the custom settings of a package in the terminal.

#### `remove`

`remove` removes deletes a project from the json file.

