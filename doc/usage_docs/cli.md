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

* `cat` prints the the entire `install.cfg` as output into the terminal.

* `install` takes the user input parmeters and installs the package with the user specifications.

* `show` takes the user input parmeters and prints the installation commands into the terminal without executing them.

* `default` is used to safe default settings specified by the user.

  * `add` safes and changes custom default settings of a user to a json file. 

  * `list` prints all the custom settings of a package in the terminal.

  * `remove` removes deletes a project from the json file.


## Examples

### Looking at Pytorch Installation

```
# ibi show https://github.com/instructions-d-installation/webpage-example -h
Usage: ibi show https://github.com/instructions-d-installation/webpage-example
           [OPTIONS]

Options:
  --build [stable|preview]        Use the latest or the tested version.
                                  [default: stable]
  ----os-- [linux|macos|windows]  The operating system you use.  [default:
                                  windows; required]
  --package [conda|pip]           The package manager you use.  [default: pip]
  --compute-platform [cu118|cu121|ro60|cpu]
                                  Should your gpu or your cpu handle the task?
                                  [default: cu118]
  -h, --help                      Show this message and exit.
```

```
# ibi show https://github.com/instructions-d-installation/webpage-example --package conda --compute-platform cu121
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c nvidia -c pytorch
```
