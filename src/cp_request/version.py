import json


class Version:
    def __init__(self, *, major: int, minor: int, patch: int):
        self.__major = int(major)
        self.__minor = int(minor)
        self.__patch = int(patch)

    def __repr__(self):
        return "Version(major={}, minor={}, patch={})".format(
            self.__major, self.__minor, self.__patch)

    def __str__(self):
        return "{}.{}.{}".format(self.__major, self.__minor, self.__patch)

    def __eq__(self, other):
        if not isinstance(other, Version):
            return False

        return (self.__major == other.major and
                self.__minor == other.minor and
                self.__patch == other.patch)

    @property
    def major(self):
        return self.__major

    @property
    def minor(self):
        return self.__minor

    @property
    def patch(self):
        return self.__patch


class VersionEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, Version):
            rep = dict()
            rep['major'] = obj.major
            rep['minor'] = obj.minor
            rep['patch'] = obj.patch
            return rep
        return super().default(obj)


class VersionDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if 'major' not in d:
            return d
        if 'minor' not in d:
            return d
        if 'patch' not in d:
            return d

        return Version(
            major=d['major'],
            minor=d['minor'],
            patch=d['patch']
        )
