# Example: Hello World

Create a file and call it `install.cfg`. Copy the following into it:

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://github.com/instructions-d-installation/installation-instruction/doc/usage_docs/hello_world.md
name: hello-world
type: object
properties:
  say_hello:
    type: boolean
    default: false
------
echo "{{ "Hello " if say_hello }}World!"

```

Executing it with the [cli] results in:  

```
# ibi install --verbose ./install.cfg --say-hello
"Hello World!"
Installation successful.
```


## Lets go over it:

Everything before the separator `------` *(6 or more `-`)* is a [JSON Schema]. Everything past it is a [Jinja template].
* The schema specifies the options the user has under the `properties` key.  
* `say_hello` is a flag *(an boolean option)*, which is by default false.  
* `{{ "Hello " if say_hello }` is jinja syntax, which pastes `Hello ` if `say_hello` is true.  
* `ibi install` then parses your input (`--say-hello` sets `say_hello` to true), renders the Jinja template with the parsed options and executes every rendered line as a command (`echo "Hello World!"`).


[cli]: https://installation-instruction.readthedocs.io/en/latest/usage_docs/cli.html
[JSON Schema]: https://json-schema.org/learn/getting-started-step-by-step
[Jinja Template]: https://jinja.palletsprojects.com/en/3.0.x/templates/
