import json


class NamedEntity:
    def __init__(self, *, name, reference):
        self.__name = name
        self.__reference = reference

    def __repr__(self):
        return "NamedEntity(name={}, reference={})".format(
            repr(self.__name), repr(self.__reference))

    def __eq__(self, other):
        if not isinstance(other, NamedEntity):
            return False
        return self.__name == other.__name and self.__reference == other.__reference

    @property
    def name(self):
        return self.__name

    @property
    def reference(self):
        return self.__reference


class NamedEntityEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, NamedEntity):
            rep = dict()
            rep['object_type'] = 'named_entity'
            rep['name'] = obj.name
            rep['reference'] = obj.reference
            return rep
        return super().default(obj)


class NamedEntityDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if 'object_type' not in d:
            return d
        if d['object_type'] != 'named_entity':
            return d
        if 'name' not in d:
            return d
        if 'reference' not in d:
            return d

        return NamedEntity(
            name=d['name'],
            reference=d['reference']
        )
