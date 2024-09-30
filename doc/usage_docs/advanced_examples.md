# Advanced Examples

```yaml
schema:
  $schema: https://json-schema.org/draft/2020-12/schema
  $id: https://github.com/instructions-d-installation/installation-instruction/doc/usage_docs/advanced_examples.md 
  title:  advanced example 
  description: This is a Schema to construct installation instructions for the advanced example.
  type: object
  properties:
    __os__:
      title: Operating System
      description: The operating system in which the package is installed.
      enum: 
        - windows
        - macoS
        - linux
    virtualenv:
      title: Use pip virtualenv
      description: Choose if you want to use a virtual environment to install the package.   
      type: boolean 
      default: false
      
  required:
    - __os__

pretty:
  windows: Windows
  macos: MacOS
  linux: Linux

```
```
------
```
```jinja
{% call command() %}
    echo

    {% if __os__ == "linux" %}
        "This is Linux!"
    {% elif __os__ == "windows" %}
        "This is Windows!"
    {% elif __os__ == "macos" %}
        "This is MacOS!"
    {% else %}
        {{ raise("This os is not supported!") }}
    {% endif %}
{% endcall %}
echo "Virtualenv is {{ "enabled" if virtualenv else "disabled" }}!"

```

This advanced example uses most functions of the package. In the following list the code is described starting from the top. 

* The schema starts with the `$schema`, `$id` , title and description keys.
* Afterwards the properties `__os__` and `virtualenv` are defined.
  * The property `__os__` is an enum type with the following choices:
      * windows
      * macos
      * linux  
      
       `__os__` is a special key with the feature of automatically setting the default value to the system it is currently running on (`["windows", "linux", "macos"]`).
  * The property `virtuealenv` is of boolean type with the default value false. Properties with boolean type are automatically registered as flags in the cli. 
* After the properties is a list of required options. In this list are all the properties listed which are not optional in the installation of the package. In this case it is `__os__`.
* Next is the list pretty for the pretty prints. This list just changes words in the help file to make it more readable. In this case windows would be turned to Windows.
* Next is the `------` which splits the file into the schema and jinja part. 
* The first statement of the jinja part `{% call command() %} ... {% endcall %}` removes all the linebreaks. In this case it removes  the linebrak between the echo line and the string choosen in the if-block. 
* The if block chooses a line based on the `__os__` property.
* The last line echos if the virtualenv property is enabled or disabled.
* For example the input:
  ```bash
  ibi show . ----os-- windows --virtualenv
  ```
  will have the following output: 
  ```bash
  echo "This is Windows!"
  echo "Virtualenv is activated!"`
  ```
