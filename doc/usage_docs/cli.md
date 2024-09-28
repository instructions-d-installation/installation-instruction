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

`cat` prints the 

