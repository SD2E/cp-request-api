from cp_request import NamedEntity
from cp_request.design.block_definition import BlockDefinition


class SubjectReference(BlockDefinition):
    def __init__(self, *, entity: NamedEntity):
        self.__entity = entity

    def __repr__(self):
        return "SubjectReference(entity={})".format(repr(self.__entity))

    def __str__(self):
        return self.__entity

    def __eq__(self, other):
        if not isinstance(other, SubjectReference):
            return False
        return self.__entity == other.__entity

    @property
    def entity(self):
        return self.__entity
