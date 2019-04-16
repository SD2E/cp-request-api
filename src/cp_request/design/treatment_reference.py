from cp_request.design.block_definition import BlockDefinition
from typing import Union


class TreatmentReference(BlockDefinition):
    def __init__(self, *, treatment_name):
        self.__treatment_name = treatment_name

    @staticmethod
    def create_from(*, treatment_name: str,
                    attribute: str = None,
                    value: Union[int, str] = None):
        if attribute:
            if value:
                return TreatmentAttributeValueReference(
                    treatment_name=treatment_name,
                    attribute=attribute,
                    value=value
                )
            return TreatmentAttributeReference(
                treatment_name=treatment_name,
                attribute=attribute
            )
        if value:
            return TreatmentValueReference(
                treatment_name=treatment_name,
                value=value
            )
        return TreatmentReference(treatment_name=treatment_name)

    def __repr__(self):
        return "TreatmentReference(treatment_name={})".format(
            repr(self.__treatment_name))

    def __str__(self):
        return self.__treatment_name

    def __eq__(self, other):
        if not isinstance(other, TreatmentReference):
            return False
        return self.__treatment_name == other.__treatment_name

    @property
    def treatment_name(self):
        return self.__treatment_name


class TreatmentAttributeReference(TreatmentReference):
    def __init__(self, *, treatment_name, attribute):
        super().__init__(treatment_name=treatment_name)
        self.__attribute = attribute

    def __repr__(self):
        return (
            "TreatmentAttributeReference(treatment_name={}, attribute={})"
        ).format(repr(self.treatment_name), repr(self.attribute))

    def __eq__(self, other):
        if not isinstance(other, TreatmentAttributeReference):
            return False
        if not super().__eq__(other):
            return False
        return self.attribute == other.attribute

    @property
    def attribute(self):
        return self.__attribute


class TreatmentValueReference(TreatmentReference):
    def __init__(self, *, treatment_name, value):
        super().__init__(treatment_name=treatment_name)
        self.__value = value

    def __repr__(self):
        return "TreatmentValueReference(treatment_name={}, value={})".format(
            repr(self.treatment_name), self.value)

    def __eq__(self, other):
        if not isinstance(other, TreatmentValueReference):
            return False
        if not super().__eq__(other):
            return False
        return self.value == other.value

    @property
    def value(self):
        return self.__value


class TreatmentAttributeValueReference(TreatmentAttributeReference):
    def __init__(self, *, treatment_name, attribute, value):
        super().__init__(treatment_name=treatment_name, attribute=attribute)
        self.__value = value

    def __repr__(self):
        return (
            "TreatmentAttributeValueReference(treatment_name={}, "
            "attribute={}, value={})"
        ).format(repr(self.treatment_name), repr(self.attribute), self.value)

    def __eq__(self, other):
        if not isinstance(other, TreatmentAttributeValueReference):
            return False
        if not super().__eq__(other):
            return False
        return self.value == other.value

    @property
    def value(self):
        return self.__value
