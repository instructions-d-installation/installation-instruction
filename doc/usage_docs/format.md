# The Format

## Config

The config is comprised of a single file `install.cfg`.It has two parts delimited by `------` (6 or more `-`).
Both parts should be developed in different files for language server support. The language of the first part is [YAML] and for the second is [Jinja]. 


### Schema

The first section of the config is a [json-Schema].
It can be written in [JSON] or to JSON capabilites restricted [YAML].
The schema is restricted to the following draft version: <https://json-schema.org/draft/2020-12/schema>.

For functional usage the schema needs to include the following properties:

* `$id` is used as identifier for the exact python package.
* `title` are used for pretty print option names.
* `description` is used for the options help message.


Here are the exact steps to adding a description and a pretty print name to enum values (for [web-installation-instruction](https://github.com/instructions-d-installation/web-installation-instruction)):
  1. Indent the schema with the key `schema`.
  2. Add `pretty` and `description` keys.
  3. Create lists like `key: Pretty Key`.

`title` and `description` from within the schema overwrite `pretty` and `description` outside of the schema.

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


The schema is tested by the Draft202012Validator from the jsonschema python package. 

For the package to set the default os to the running system, give the property which specified the os the name `__os__`.

```yaml
__os__:
  - windows
  - linux
  - macos
```


### Jinja template

In the second part of the file a Jinja template is written. 
When installing the package, each rendered line is executed individually after each other.
```bash
echo "Hello"
echo "World!"
```
For a command with multible endparts wrapping with `{% call command() %}` and `{% endcall %}` essentially removes all line breaks for convenience.

```jinja
{% call command() %}
{% if greeting == "conda" %}
    hello
    {% if person == "world" %}
        World!
    {% else %}
        Nobody!
    {% endif %}
{% endif %}
{% endcall %}
```


If you wish to stop the render from within the template you can use the macro `raise`. (`{{ raise("no support!") }}`.) 

```jinja
{% if greeting == "conda" %}
    hello
    {% if person == "world" %}
        World!
    {% else %}
        {{ raise("World is not greeted!") }}
    {% endif %}
{% endif %}
```

[YAML]: https://yaml.org/
[JSON]: https://www.json.org/json-en.html
[Jinja]: https://jinja.palletsprojects.com/en/3.1.x/templates/
[json-Schema]: https://json-schema.org/
