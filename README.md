# pconf

[![Build Status](https://img.shields.io/travis/andrasmaroy/pconf.svg?style=flat)](https://travis-ci.org/andrasmaroy/pconf)
[![Code Coverage](https://img.shields.io/codecov/c/github/andrasmaroy/pconf.svg?style=flat)](https://codecov.io/gh/andrasmaroy/pconf)
[![PyPi Version](https://img.shields.io/pypi/v/pconf.svg?style=flat)](https://pypi.python.org/pypi/pconf)
[![License](https://img.shields.io/pypi/l/pconf.svg?style=flat)](https://pypi.python.org/pypi/pconf)
[![Py Versions](https://img.shields.io/pypi/pyversions/pconf.svg?style=flat)](https://pypi.python.org/pypi/pconf)
[![Known Vulnerabilities](https://snyk.io/test/github/andrasmaroy/pconf/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/andrasmaroy/pconf?targetFile=requirements.txt)

Hierarchical python configuration with files, environment variables, command-line arguments.

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
Pconf is designed to be used with multiple sources of configuration values with the user being able define the priority of each of these as a hierarchy. The supported sources described below can be setup in any order without any hardcoded defaults. Priority meaning if a configuration key appears in multiple sources the value from the sources higher up in the hierarchy takes precedence. The order in which the sources are attached defines the priority in the hierarchy, source attached first take precedence.

The available sources (more details about the below) in a sensible order:
1. **overrides** - Loads data passed to it
2. **argv** - Parses command line arguments to the process
3. **env** - Parses environment variables
4. **file** - Parses config files of various formats
5. **defaults** - Loads data passed to it

## Config sources

### Defaults, overrides
These two sources are essentially the same, pass a `dict` to when attaching and they will return that when queried.
``` python
Pconf.overrides({'key': 'override_value'})
Pconf.defaults({'key': 'default_value'})
```
Very simple, as the name suggests these are to allow the user to set defaults and override whatever value.

### Argv
Responsible for loading values parsed from command line arguments passed to the process. Parameters passed to the process, but not described to be parsed as below are ignored.

Parsed arguments can be defined with the following parameters:
* `name`: the long name of the argument
* `short_name`: the *optional* short name of the argument
* `type`: the *optional* type of the argument
* `help`: the *optional* help text for the argument

``` python
Pconf.argv('--test_argument')
Pconf.argv('--privileged', type=bool)
Pconf.argv('--threads', short_name='-c', type=int)
Pconf.argv('--verbose', short_name='-v', type=bool, help='Run in verbose mode')
```
These could be used like:
``` bash
python example.py --test_argument=hello_world -v --threads 4
```
#### Lists as arguments
Lists can be passed in two ways as arguments
* literal list
```python
Pconf.argv('--list', type=list)
```
```bash
python example.py --list="['item1', 'item2']"
{'list': ['item1', 'item2']}
```
* repeated arguments:
```python
Pconf.argv('--list', type='repeated_list')
```
```bash
python example.py --list=item1 --list=item2
{'list': ['item1', 'item2']}
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

# The contents of the variables can be parsed as well-known types, in case parsing fails the variable remains as a string
Pconf.env(parse_values=True)

# The variable names can be converted to lowercase to match other variable names.
Pconf.env(to_lower=True)

# Convert all underscores in the name to dashes, this takes place after separation via the separator option.
Pconf.env(convert_underscores=True)

# Use all at once
Pconf.env(separator='__',
          match='whatever_matches_this_will_be_whitelisted',
          whitelist=['whatever', 'doesnt', 'match', 'but', 'is', 'whitelisted', 'gets', 'loaded', 'too'],
          parse_values=True,
          to_lower=True,
          convert_underscores=True)
```

### File
Responsible for loading values parsed from a given file into the configuration hierarchy. If the file does not exist the result will be empty and no error is thrown.

By default tries to parse file contents as literal python variables, use the `encoding` parameter to set the file format/encoding.
``` python
"""
`/path/to/literal` contents:
{'this': 'is_a_literal_python_dict'}
"""
Pconf.file('/path/to/literal')
```

#### Built-in encodings:
These are the built-in supported encodings, that can be passed as the `encoding` parameter to the function. All the example files below result in the same data structure after parsing.
* ini
    ``` python
    """
    `/path/to/config.ini` contents:
    [example]
    key: value
    another=stuff
    """
    Pconf.file('/path/to/config.ini', encoding='ini')
    ```
    Ini files have to have sections, though the special `DEFAULT` section won't be included as a section header only its contents.
    Also ini files are quite restrictive, only basic types are supported, and most are parsed as strings. If support for more complex types is required AND it has to come from ini files, then look at custom file formats below.
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
* yaml
    ``` python
    """
    `/path/to/config.yaml` contents:
    ---
    example:
      key: value
      another: stuff
    """
    Pconf.file('/path/to/config.yaml', encoding='yaml')
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
pip install -r requirements.txt
pip install -r requirements-dev.txt
```
Run the tests from the repository root like so:
```bash
py.test
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/andrasmaroy/pconf/tags). 

## Authors

* [Andras Maroy](https://github.com/andrasmaroy)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Inspired by [nconf](https://github.com/indexzero/nconf)
