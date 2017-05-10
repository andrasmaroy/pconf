import store.env
import store.file


class Pconf(object):
    __hierarchy = []

    @classmethod
    def get(cls):
        results = {}

        for storeMethod in cls.__hierarchy:
            for key, value in storeMethod.get().iteritems():
                if key not in results:
                    results[key] = value

        return results

    @classmethod
    def file(cls, path, encoding=None, parser=None):
        cls.__hierarchy.append(store.file.File(path, encoding, parser))

    @classmethod
    def env(cls, separator=None, match=None, whitelist=None):
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
