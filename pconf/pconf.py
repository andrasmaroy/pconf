from .store import argv
from .store import env
from .store import file
from .store import memory

from deepmerge import Merger


class Pconf(object):
    """Entry point class for the pconf module.

    Doesn't need to be instantiated. First set the hierarchy, by calling the
    desired source methods in the desired order. The source set first has the
    highest priority.

    After sources are set the values can be accessed by calling get()
    """

    __hierarchy = []

    merger = Merger([(dict, ["merge"])], ["override"], ["override"])

    @classmethod
    def get(cls):
        """Get values gathered from the previously set hierarchy.

        Respects the order in which sources are set, the first source set
        has the highest priority, overrides values with the same key that
        exist in sources with lower priority.

        Returns:
            dict: The dictionary containing values gathered from all set sources.
        """
        results = {}

        hierarchy = cls.__hierarchy[::-1]

        for storeMethod in hierarchy:
            cls.merger.merge(results, storeMethod.get())

        return results

    @classmethod
    def defaults(cls, data):
        """Set passed values as a source

        Stores the passed dict in memory, use to manually set default values
        in the hierarchy, by setting this in the end.

        Args:
            data: the dict to store
        """
        cls.__hierarchy.append(memory.Memory(data))

    @classmethod
    def overrides(cls, data):
        """Set passed values as a source

        Stores the passed dict in memory, use to manually override any values
        in the hierarchy, by setting this in the front.

        Args:
            data: the dict to store
        """
        cls.__hierarchy.append(memory.Memory(data))

    @classmethod
    def argv(cls, name, short_name=None, type=None, help=None):
        """Set command line arguments as a source

        Parses the command line arguments described by the parameters.

        Args:
            name: the long name of the argument (foo)
            short_name: the optional short name of the argument (f)
            type: the optional type of the argument, defaults to bool
            help: the optional help text for the argument
        """
        cls.__hierarchy.append(argv.Argv(name, short_name, type, help))

    @classmethod
    def env(
        cls,
        separator=None,
        match=None,
        whitelist=None,
        parse_values=None,
        to_lower=None,
        convert_underscores=None,
        docker_secrets=None,
    ):
        """Set environment variables as a source.

        By default all environment variables available to the process are used.
        This can be narrowed by the args.

        Args:
            separator: Keys are split along this character, the resulting
                splits are considered nested values.
            match: Regular expression for key matching. Keys matching the
                expression are considered whitelisted.
            whitelist: Only use environment variables that are listed in this
                list.
            parse_values: Try to parse all variable for well-known types.
            to_lower: Convert all variable names to lower case.
            convert_underscores: Convert all underscores in the name to dashes,
                this takes place after separation via the separator option.
            docker_secrets: A list of names with _FILE postfix, which will have
                their postfix removed and the content of the file pointed by
                their original value.
        """
        cls.__hierarchy.append(
            env.Env(
                separator,
                match,
                whitelist,
                parse_values,
                to_lower,
                convert_underscores,
                docker_secrets,
            )
        )

    @classmethod
    def file(cls, path, encoding=None, parser=None):
        """Set a file as a source.

        File are parsed as literal python dicts by default, this behaviour
        can be configured.

        Args:
            path: The path to the file to be parsed
            encoding: The encoding of the file.
                Defaults to 'raw'. Available built-in values: 'ini', 'json', 'yaml'.
                Custom value can be used in conjunction with parser.
            parser: A parser function for a custom encoder.
                It is expected to return a dict containing the parsed values
                when called with the contents of the file as an argument.
        """
        cls.__hierarchy.append(file.File(path, encoding, parser))

    @classmethod
    def clear(cls):
        """Purge everything from the current hierarchy.

        In case of the need for multiple configurations this can be used to
        reset everything to a blank slate and start over.
        """
        del cls.__hierarchy[:]  # instead of clear() to maintain 2.7 compatibility
