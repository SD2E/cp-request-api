import json


class Unit:
    def __init__(self, *, reference):
        self.__reference = reference

    def __repr__(self):
        return "Unit(reference={})".format(repr(self.__reference))

    def __str__(self):
        return self.__reference

    def __eq__(self, other):
        if not isinstance(other, Unit):
            return False

        return self.__reference == other.__reference

    @property
    def reference(self):
        return self.__reference


class UnitEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, Unit):
            rep = dict()
            rep['object_type'] = 'unit'
            rep['reference'] = obj.reference
            return rep
        return super().default(obj)


class UnitDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if 'object_type' not in d:
            return d
        if d['object_type'] != 'unit':
            return d
        if 'reference' not in d:
            return d
        return Unit(reference=d['reference'])
