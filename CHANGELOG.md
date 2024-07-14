# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

* Added `cat` command: Users can now see the source of an `install.cfg` file with `ibi cat`.


### Changed

* Switched to sandboxed rendering of template for security purposes.


## [0.4.0] - 2024-06-24

### Added

* Added git remote repositories and directories as potential sources for config files in the cli.
* `title` and `description` can be set from `pretty` and `description` keys at root.
* Added default key for os systems.


### Changed

* Moved `title` and `description` from `anyOf` to outside of schema. `anyOf` is now usable as intended for json schema.


### Removed

* Removed `title` and `description` support from `anyOf`.


## [0.3.0] - 2024-06-04

### Added

* Added schema validation when reading in config. (Before it was only validated when rendering the template.)
* Added parse function `parse_schema` to `InstallationInstruction` for 
    [web-installation-instruction](https://github.com/instructions-d-installation/web-installation-instruction)
    project.
* Added documentation for release procedure.


## [0.2.0] - 2024-05-30

### Added

* Added installation functionality.
* Added pretty print to show command.
* Added many colors for cli output.
* Added PyPi version badge.
* Added version flag.
* Added help shorthand.

### Changed

* Flags are now handled properly (requiered and default).
* Reworked config section in readme.
* Fixed wrong description of project in readme.
* Fixed wrong section title in readme.

### Removed


## [0.1.1] - 2024-05-21

### Changed

* Fixed scipy example.
* Other `UndefinedError` in template are now thrown.
* Fixed maximum supported `click` version.


## [0.1.0] - 2024-05-20

### Added

* Added cli for rendering installation instructions for end users.
* Added config section in readme.
* Added installation section in readme.
* Added examples.
* Added many tests.
* Added `raise` jinja macro.
* Generated project with template.
* Added badges.
* Added contributors.


[unreleased]: https://github.com/instructions-d-installation/installation-instruction/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/instructions-d-installation/installation-instruction/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/instructions-d-installation/installation-instruction/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/instructions-d-installation/installation-instruction/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/instructions-d-installation/installation-instruction/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/instructions-d-installation/installation-instruction/releases/tag/v0.1.0
