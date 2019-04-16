import abc
import json
from typing import List
from cp_request import (
    NamedEntity, NamedEntityEncoder, NamedEntityDecoder,
    Unit, UnitEncoder, UnitDecoder,
    Value, ValueEncoder, ValueDecoder
)


class Treatment(abc.ABC):
    @abc.abstractmethod
    def __init__(self, *, name: str):
        self.__name = name

    @staticmethod
    def create_from(*,
                    name: str,
                    unit: Unit = None,
                    entity: NamedEntity = None,
                    attributes=None,
                    value: Value = None):  # should be List[AttributeEntity]
        if not name:
            raise CannotCreateTreatmentException(
                'Name must be provided to create a Treatment')
        if unit:
            return AttributeTreatment(name=name, unit=unit)
        if entity:
            if attributes:
                return EntityAttributeTreatment(name=name,
                                                entity=entity,
                                                attributes=attributes)
            return EntityTreatment(name=name, entity=entity)
        if value:
            return SimpleTreatment(name=name, value=value)
        raise CannotCreateTreatmentException(
            'No valid combinations of arguments provided')

    def is_bound(self):
        return False

    @property
    def name(self):
        return self.__name


class CannotCreateTreatmentException(Exception):
    def __init__(self, message):
        super().__init__(message)


class TreatmentEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, AttributeTreatment):
            return AttributeTreatmentEncoder().default(obj)
        if isinstance(obj, EntityAttributeTreatment):
            return EntityAttributeTreatmentEncoder().default(obj)
        if isinstance(obj, EntityTreatment):
            return EntityTreatmentEncoder().default(obj)
        if isinstance(obj, SimpleTreatment):
            return SimpleTreatmentEncoder().default(obj)
        return super().default(obj)


class TreatmentDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if 'treatment_type' not in d:
            return d
        if d['treatment_type'] == 'attribute_treatment':
            return AttributeTreatmentDecoder().object_hook(d)
        if d['treatment_type'] == 'entity_attribute_treatment':
            return EntityAttributeTreatmentDecoder().object_hook(d)
        if d['treatment_type'] == 'entity_treatment':
            return EntityTreatmentDecoder().object_hook(d)
        if d['treatment_type'] == 'simple_treatment':
            return SimpleTreatmentDecoder().object_hook(d)
        return d


class AttributeTreatment(Treatment):
    def __init__(self, *, name: str, unit: Unit):
        super().__init__(name=name)
        self.__unit = unit

    def __repr__(self):
        return "AttributeTreatment(name={}, unit={})".format(
            repr(self.name), repr(self.__unit))

    def __eq__(self, other):
        if not isinstance(other, AttributeTreatment):
            return False
        return self.name == other.name and self.unit == other.unit

    @property
    def unit(self):
        return self.__unit


class AttributeTreatmentEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, AttributeTreatment):
            rep = dict()
            rep['treatment_type'] = 'attribute_treatment'
            rep['name'] = obj.name
            rep['unit'] = UnitEncoder().default(obj.unit)
            return rep
        return super().default(obj)


class AttributeTreatmentDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if isinstance(d, AttributeTreatment):
            return d
        if 'treatment_type' not in d:
            return d
        if d['treatment_type'] != 'attribute_treatment':
            return d
        if 'name' not in d:
            return d
        if 'unit' not in d:
            return d
        return AttributeTreatment(
            name=d['name'], 
            unit=UnitDecoder().object_hook(d['unit'])
        )


class EntityAttributeTreatment(Treatment):
    def __init__(self, *, name: str,
                 entity: NamedEntity,
                 attributes: List[AttributeTreatment]):
        super().__init__(name=name)
        self.__entity = entity
        self.__attributes = attributes

    def __repr__(self):
        return "EntityAttributeTreatment(name={}, entity={}, attributes={})".format(
            repr(self.name), repr(self.entity), repr(self.attributes))

    def __eq__(self, other):
        if not isinstance(other, EntityAttributeTreatment):
            return False
        return (self.name == other.name
                and self.entity == other.entity
                and self.attributes == other.attributes)

    @property
    def entity(self):
        return self.__entity

    @property
    def attributes(self):
        return self.__attributes


class EntityAttributeTreatmentEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, EntityAttributeTreatment):
            rep = dict()
            rep['treatment_type'] = 'entity_attribute_treatment'
            rep['name'] = obj.name
            rep['entity'] = NamedEntityEncoder().default(obj.entity)
            rep['attributes'] = [
                AttributeTreatmentEncoder().default(attribute)
                for attribute in obj.attributes
            ]
            return rep
        return super().default(obj)


class EntityAttributeTreatmentDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if 'treatment_type' not in d:
            return d
        if d['treatment_type'] != 'entity_attribute_treatment':
            return d
        if 'name' not in d:
            return d
        if 'entity' not in d:
            return d
        if 'attributes' not in d:
            return d
        return EntityAttributeTreatment(
            name=d['name'],
            entity=NamedEntityDecoder().object_hook(d['entity']),
            attributes=[
                AttributeTreatmentDecoder().object_hook(attribute) for attribute in d['attributes']
            ]
        )


class EntityTreatment(Treatment):
    def __init__(self, *, name: str, entity: NamedEntity):
        super().__init__(name=name)
        self.__entity = entity

    def __repr__(self):
        return "EntityTreatment(name={}, entity={})".format(
            repr(self.name), repr(self.entity))

    def __eq__(self, other):
        if not isinstance(other, EntityTreatment):
            return False
        return self.name == other.name and self.entity == other.entity

    @property
    def entity(self):
        return self.__entity

    def is_bound(self):
        return True


class EntityTreatmentEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, EntityTreatment):
            rep = dict()
            rep['treatment_type'] = 'entity_treatment'
            rep['name'] = obj.name
            rep['entity'] = NamedEntityEncoder().default(obj.entity)
            return rep
        return super().default(obj)


class EntityTreatmentDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if 'treatment_type' not in d:
            return d
        if d['treatment_type'] != 'entity_treatment':
            return d
        if 'name' not in d:
            return d
        if 'entity' not in d:
            return d
        return EntityTreatment(
            name=d['name'],
            entity=NamedEntityDecoder().object_hook(d['entity'])
        )


class SimpleTreatment(Treatment):
    def __init__(self, *, name: str, value: Value):
        super().__init__(name=name)
        self.__value = value

    def __repr__(self):
        return "SimpleTreatment(name={}, value={})".format(
            repr(self.name), repr(self.value))

    def __eq__(self, other):
        if not isinstance(other, SimpleTreatment):
            return False
        return self.name == other.name and self.value == other.value

    @property
    def value(self):
        return self.__value

    def is_bound(self):
        return True


class SimpleTreatmentEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, SimpleTreatment):
            rep = dict()
            rep['treatment_type'] = 'simple_treatment'
            rep['name'] = obj.name
            rep['value'] = ValueEncoder().default(obj.value)
            return rep
        return super().default(obj)


class SimpleTreatmentDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if 'treatment_type' not in d:
            return d
        if d['treatment_type'] != 'simple_treatment':
            return d
        if 'name' not in d:
            return d
        if 'value' not in d:
            return d
        return SimpleTreatment(
            name=d['name'],
            value=ValueDecoder().object_hook(d['value'])
        )
