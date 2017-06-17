pconf
=====

Hierarchical python configuration with files, environment variables,
command-line arguments.

See `GitHub <https://github.com/andrasmaroy/pconf>`__ for detailed documentation.

**License: MIT**

Example
-------

.. code:: python

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

Run the above script:

.. code:: bash

    pip install pconf
    python example.py

The output should be something like this:

::

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
