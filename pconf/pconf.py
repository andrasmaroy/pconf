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
