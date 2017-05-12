# pconf
Hierarchical python configuration with files, environment variables, command-line arguments. Inspired by [nconf](https://github.com/indexzero/nconf).

## Example

``` python
from pconf import Pconf
import json

"""
Setup pconf config source hierarchy as:
  1. Environment variables
  2. A JSON file located at 'path/to/config.json'
"""
Pconf.env()
Pconf.file('path/to/config.json', encoding='json')

# Get all the config values parsed from the sources
config = Pconf.get()

# Just print everything nicely
print json.dumps(config, sort_keys=True, indent=4)
```
Run the above script:
``` bash
python example.py
```
The output should be something like this:
```
{
    "HOSTNAME": "bb30700d22d8",
    "TERM": "xterm",
    "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
    "PWD": "/",
    "SHLVL": "1",
    "HOME": "/root",
    "no_proxy": "*.local, 169.254/16",
    "_": "/usr/bin/env",
    "example": {
        "another": "stuff",
        "key": "value"
    }
}
```

## Hierarchical configuration
Pconf is designed to be used with multiple sources of configuration values with the user being able define the priority of each of these as a hierarchy. The supported sources described below can be setup in any order without any hardcoded defaults. Priority meaning if a configuration key appears in multiple sources the value from the sources higher up in the hierarchy takes precedence. The order in which the sources are attached defines the priority in the hierarchy.

The available sources (more details about the below) in a sensible order:
1. **overrides** - Loads data passed to it
2. **argv** - Parses command line arguments to the process
3. **env** - Parses environment variables
4. **file** - Parses config files of various formats
5. **defaults** - Loads data passed to it

## Config sources

### Defaults, overrides
**Not yet implemented**
These two sources are essentially the same, pass a `dict` to when attaching and they will return that when queried.
``` python
Pconf.overrides({'key': 'override_value'})
Pconf.defaults({'key': 'default_value'})
```
Very simple, as the name suggests these are to allow the user to set defaults and override whatever value.

### Argv
**Not yet implemented**
Responsible for loading values parsed from command line arguments passed to the process.

Argv is expecting a parameters which are then passed to [argparse](https://docs.python.org/2/howto/argparse.html), see the documentation of the [add_argument()](https://docs.python.org/2/library/argparse.html#argparse.ArgumentParser.add_argument) for details.
``` python
Pconf.argv("-v", "--verbose", action="store_true")
Pconf.argv("-q", "--quiet", action="store_true")
```

### Env
Responsible for loading values parsesd from `os.environ` into the configuration hierarchy.
``` python
# Just load all the variables available for the process
Pconf.env()

# A separator can be specified for nested keys
Pconf.env(separator='__')
# This turns the 'log__file=/log' env variable into the `{'log': {'file': '/log'}}` dict

# Available variables can be whitelisted
Pconf.env(whitelist=['only', 'load', 'variables', 'listed', 'here'])

# A regular expression can be specified for matching keys also
# Keys matched by this expression are considered whitelisted
Pconf.env(match='^REGEX.*')

# Use all at once
Pconf.env(separator='__',
          match='whatever_matches_this_will_be_whitelisted',
          whitelist=['whatever', 'doesnt', 'match', 'but', 'is', 'whitelisted', 'gets', 'loaded', 'too'])
```

### File
Responsible for loading values parsed from a given file into the configuration hierarchy.

By default tries to parse file contents as literal python variables, use the `encoding` parameter to set the file format/encoding.
``` python
"""
`/path/to/literal` contents:
{'this': 'is_a_literal_python_dict'}
"""
Pconf.file('/path/to/literal')
```

#### Built-in encodings:
These are the built-in supported encodings, that can be passed as the `encoding` parameter to the function.
* json
``` python
"""
`/path/to/config.json` contents:
{
    "example": {
        "key": "value",
        "another": "stuff"
    }
}
"""
Pconf.file('/path/to/config.json', encoding='json')
```

#### Using custom file formats
To use custom encodings supply a parser along with an encoding that is not built-in. The parser is a function that expects the file contents as its argument and returns a dict containing the parsed contents.
``` python
def custom_parser(file_contents):
    return {'example': file_contents}

Pconf.file('/path/to/custom/file', encoding='example', parser=custom_parser)
```

## Getting the config values
Use the `get` method to get the processed config values. The method returns all the values as a python dictionary, with nested values and all. Values can be accessed as expected from a `dict`.

``` python
config = Pconf.get()

print config['key']
```

## Run Tests
Test are written using the standard python unittest framework.
First install the dev requirements:
```bash
pip install -r requirements-dev.txt
```
Run the tests from the repository root like so:
```bash
py.test
```

#### Author: [Andras Maroy](https://github.com/andrasmaroy)
#### License: MIT
