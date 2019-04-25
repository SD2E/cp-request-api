from cp_request import Treatment, Value
from cp_request.design.block_definition import BlockDefinition
from typing import Union


class TreatmentReference(BlockDefinition):
    def __init__(self, *, treatment: Treatment):
        self.__treatment = treatment

    @staticmethod
    def create_from(*, treatment: Treatment,
                    value: Union[int, float] = None):
        if value:
            return TreatmentValueReference(
                treatment=treatment,
                value=value
            )
        return TreatmentReference(treatment=treatment)

    def __repr__(self):
        return "TreatmentReference(treatment={})".format(
            repr(self.__treatment))

    def __str__(self):
        return self.__treatment

    def __eq__(self, other):
        if not isinstance(other, TreatmentReference):
            return False
        return self.__treatment == other.__treatment

    def apply(self, visitor):
        visitor.visit_treatment_reference(self)

    @property
    def treatment(self):
        return self.__treatment

    @property
    def treatment_name(self):
        return self.treatment.name


class TreatmentValueReference(TreatmentReference):
    def __init__(self, *, treatment: Treatment, value: Value):
        super().__init__(treatment=treatment)
        self.__value = value

    def __repr__(self):
        return "TreatmentValueReference(treatment={}, value={})".format(
            repr(self.treatment), repr(self.value))

    def __eq__(self, other):
        if not isinstance(other, TreatmentValueReference):
            return False
        if not super().__eq__(other):
            return False
        return self.value == other.value

    def apply(self, visitor):
        visitor.visit_treatment_value_reference(self)

    @property
    def value(self):
        return self.__value
