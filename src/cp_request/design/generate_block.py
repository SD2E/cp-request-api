from cp_request import Value
from cp_request.design import TreatmentReference
from cp_request.design.block_definition import BlockDefinition
from typing import List


class GenerateBlock(BlockDefinition):
    """
    A design block definition by assigning a list of values to a treatment.

    Equivalent to a {SumBlock} that includes each assignment of values to the
    attribute(s) of the treatment.
    """

    def __init__(self, *,
                 treatment: TreatmentReference,
                 attribute_name: str,
                 values: List[Value]):
        self.__treatment = treatment
        self.__attribute_name = attribute_name
        self.__values = values

    def __repr__(self):
        return "GenerateBlock(treatment={}, attribute_name={}, values={})".format(
            repr(self.__treatment), repr(self.__attribute_name), repr(self.__values))

    # TODO: implement str method
    def __str__(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, GenerateBlock):
            return False
        return (self.__treatment == other.__treatment and
                self.__attribute_name == other.__attribute_name and
                self.__values == other.__values)

    def apply(self, visitor):
        visitor.visit_generate_block(self)

    @property
    def treatment(self):
        return self.__treatment

    @property
    def attribute_name(self):
        return self.__attribute_name

    @property
    def values(self):
        return self.__values
