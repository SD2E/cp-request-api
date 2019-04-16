from cp_request import Value
from cp_request.design import TreatmentReference
from cp_request.design.block_definition import BlockDefinition
from typing import List


class GenerateBlock(BlockDefinition):
    def __init__(self, *, treatment: TreatmentReference, values: List[Value]):
        self.__treatment = treatment
        self.__values = values

    def __repr__(self):
        return "GenerateBlock(treatment={}, values={})".format(
            repr(self.__treatment), repr(self.__values))

    def __str__(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, GenerateBlock):
            return False
        return (self.__treatment == other.__treatment and
                self.__values == other.__values)

    @property
    def treatment(self):
        return self.__treatment

    @property
    def values(self):
        return self.__values

