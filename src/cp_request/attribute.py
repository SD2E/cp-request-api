import abc
import json
from cp_request import (
    Unit, UnitEncoder, UnitDecoder,
    Value, ValueEncoder, ValueDecoder
)


class Attribute:
    """
    Abstract base class representing an attribute.
    """

    @abc.abstractmethod
    def __init__(self, name: str):
        self.__name = name

    @staticmethod
    def create_from(*,
                    name: str,
                    unit: Unit = None,
                    value: Value = None):
        if not name:
            raise CannotCreateAttributeException(
                'Name must be provided to create an Attribute')
        if unit:
            return UnboundAttribute(name=name, unit=unit)
        if value:
            return BoundAttribute(name=name, value=value)

    def __eq__(self, other):
        if not isinstance(other, Attribute):
            return False
        return self.name == other.name

    def apply(self, visitor):
        visitor.visit_attribute(self)

    @property
    def name(self):
        return self.__name

    def is_bound(self):
        """
        Indicates whether this {Attribute} is bound to a {Value}.
        """
        return False


class CannotCreateAttributeException(Exception):
    def __init__(self, message):
        super().__init__(message)


class BoundAttribute(Attribute):
    def __init__(self, name: str, value: Value):
        super().__init__(name=name)
        self.__value = value

    def __repr__(self):
        return "BoundAttribute(name={}, value={})".format(
            repr(self.name), repr(self.__value)
        )

    def __eq__(self, other):
        if not isinstance(other, BoundAttribute):
            return False
        if not super().__eq__(other):
            return False
        return self.value == other.value

    @property
    def value(self):
        return self.__value

    def is_bound(self):
        return True


class UnboundAttribute(Attribute):
    def __init__(self, name: str, unit: Unit):
        super().__init__(name=name)
        self.__unit = unit

    def __repr__(self):
        return "UnboundAttribute(name={}, unit={})".format(
            repr(self.name), repr(self.__unit)
        )

    def __eq__(self, other):
        if not isinstance(other, UnboundAttribute):
            return False
        if not super().__eq__(other):
            return False
        return self.unit == other.unit

    @property
    def unit(self):
        return self.__unit


class AttributeEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, BoundAttribute):
            return BoundAttributeEncoder().default(obj)
        if isinstance(obj, UnboundAttribute):
            return UnboundAttributeEncoder().default(obj)
        return super().default(obj)


class AttributeDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if 'attribute_type' not in d:
            return d
        if d['attribute_type'] == 'bound_attribute':
            return BoundAttributeDecoder().object_hook(d)
        if d['attribute_type'] == 'unbound_attribute':
            return UnboundAttributeDecoder().object_hook(d)
        return d


class BoundAttributeEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, Attribute):
            rep = dict()
            rep['attribute_type'] = 'bound_attribute'
            rep['name'] = obj.name
            rep['value'] = ValueEncoder().default(obj.value)
            return rep
        return super().default(obj)


class BoundAttributeDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, dictionary):
        if isinstance(dictionary, BoundAttribute):
            return dictionary
        if 'attribute_type' not in dictionary:
            return dictionary
        if dictionary['attribute_type'] != 'bound_attribute':
            return dictionary
        if 'name' not in dictionary:
            return dictionary
        if 'value' not in dictionary:
            return dictionary
        return BoundAttribute(
            name=dictionary['name'],
            value=ValueDecoder().object_hook(dictionary['value'])
        )


class UnboundAttributeEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, Attribute):
            rep = dict()
            rep['attribute_type'] = 'unbound_attribute'
            rep['name'] = obj.name
            rep['unit'] = UnitEncoder().default(obj.unit)
            return rep
        return super().default(obj)


class UnboundAttributeDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, dictionary):
        if isinstance(dictionary, UnboundAttribute):
            return dictionary
        if 'attribute_type' not in dictionary:
            return dictionary
        if dictionary['attribute_type'] != 'unbound_attribute':
            return dictionary
        if 'name' not in dictionary:
            return dictionary
        if 'unit' not in dictionary:
            return dictionary
        return UnboundAttribute(
            name=dictionary['name'],
            unit=UnitDecoder().object_hook(dictionary['unit'])
        )
