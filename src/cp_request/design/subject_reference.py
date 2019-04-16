from cp_request.design.block_definition import BlockDefinition


class SubjectReference(BlockDefinition):
    def __init__(self, *, entity_name):
        self.__entity_name = entity_name

    def __repr__(self):
        return "SubjectReference(entity={})".format(repr(self.__entity_name))

    def __str__(self):
        return self.__entity_name

    def __eq__(self, other):
        if not isinstance(other, SubjectReference):
            return False
        return self.__entity_name == other.__entity_name

    @property
    def entity_name(self):
        return self.__entity_name
