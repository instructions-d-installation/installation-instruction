# Architecture

## Format

The configuration file (`install.cfg`) is split into two parts. The first part is the schema part describing the possible options the end user might choose.
The second part is the template part, holding a template that is rendered and then executed line by line.
This split was chosen to have easy access to the option variable name, pretty print name, description and type.


### Schema

The schema part can be encoded with JSON or YAML. The library first tries to load the schema part with a safe yaml loader and when that fails with a json loader.

JSON Schema is a structured and well defined format. We use it to define options and flags.  
Flags are properties of type `boolean` and with the default `false`. Currently the cli will error, when the default is not set.  
Options can also be of type `number` or `string`.  

To define choice options (`["windows", "linux"]`) enum type is used.  
Though JSON Schema misses in itself the funcionality to save `title` and `description` for the enum values. 
This results in the need to save said data separately from the JSON Schema.
Said data is stored in the root keys `pretty` and `description`, while the schema is stored in `schema`.

This makes it necessary to detect, if the JSON Schema is in the root of the JSON/YAML or in the key `schema`.

The schema is validated and the end user input is checked before rendering the template. 


### Jinja Template

The template is given the parsed variables defined by the JSON Schema. This results in the variables having some type safety.

To support some common functionality, two macros are injected into the template before it is rendered (`raise` and `command`).
The template is rendered by a sandboxed renderer, as rendering a jinja template implies executing untrusted code.


### Composite Format

Havind a composite format configuration file has some adavantages and some disadvantages.

#### Advantages:
* One file holds the configuration.
* Structured and unstructured data can be held.
* Easy sharing.

#### Disadvantages:
* Missing IDE support.

The missing IDE support can be bypassed by developing the configuration in different files (`.yml` and `.json`).
The composite format could be build in the future by the cli from those separate files.

