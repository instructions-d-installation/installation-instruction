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

* The schema starts with the $schema, $id , title and description keys which are importent for the processing of the schema in the runtime.
* Afterwards the properties `__os__` and `virtualenv` are defined.
* The property `__os__` is an enum type with the following choices:
    * windows
    * macos
    * linux  
    
    As the name is `__os__` it also uses the feature of automatically setting the default value to the system it is currently running on.
* The property `virtuealenv` is a boolean type with the default value false. Properties with boolean type are automatically registered as flags in the cli. 
* After the properties is a list of required options. In this list are all the properties listed which are required to install a package. In this case it is `__os__`.
* Next is the list pretty for the pretty prints. This list just changes words in the help file to make it more readable. In this case windows would be turned to Windows.
* 
* 
* 
* 
* 
* 