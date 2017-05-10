import store.env
import store.file


class Pconf(object):
    """Entry point class for the pconf module.

    Doesn't need to be instantiated. First set the hierarchy, by calling the
    desired source methods in the desired order. The source set first has the
    highest priority.

    After sources are set the values can be accessed by calling get()
    """
    __hierarchy = []

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

        for storeMethod in cls.__hierarchy:
            for key, value in storeMethod.get().iteritems():
                if key not in results:
                    results[key] = value

        return results

    @classmethod
    def file(cls, path, encoding=None, parser=None):
        """Set a file as a source.

        File are parsed as literal python dicts by default, this behaviour
        can be configured.

        Args:
            path: The path to the file to be parsed
            encoding: The encoding of the file.
                Defaults to 'raw'. Available built-in values: 'json'.
                Custom value can be used in conjunction with parser.
            parser: A parser function for a custom encoder.
                It is expected to return a dict containing the parsed values
                when called with the contents of the file as an argument.
        """
        cls.__hierarchy.append(store.file.File(path, encoding, parser))

    @classmethod
    def env(cls, separator=None, match=None, whitelist=None):
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
        """
        cls.__hierarchy.append(store.env.Env(separator, match, whitelist))

    @classmethod
    def argv(cls):
        raise NotImplementedError

    @classmethod
    def defaults(cls):
        raise NotImplementedError

    @classmethod
    def overrides(cls):
        raise NotImplementedError
