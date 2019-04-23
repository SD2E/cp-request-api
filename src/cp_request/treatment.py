import abc
import json
from cp_request import (
    Attribute, AttributeEncoder, AttributeDecoder,
    NamedEntity, NamedEntityEncoder, NamedEntityDecoder
)


class Treatment(abc.ABC):
    @abc.abstractmethod
    def __init__(self, *, name: str):
        self.__name = name

    @staticmethod
    def create_from(*,
                    attribute: Attribute = None,
                    entity: NamedEntity = None):
        if attribute:
            return AttributeTreatment(attribute=attribute)
        elif entity:
            return EntityTreatment(entity=entity)
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
        if isinstance(obj, EntityTreatment):
            return EntityTreatmentEncoder().default(obj)
        return super().default(obj)


class TreatmentDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if 'treatment_type' not in d:
            return d
        if d['treatment_type'] == 'attribute_treatment':
            return AttributeTreatmentDecoder().object_hook(d)
        if d['treatment_type'] == 'entity_treatment':
            return EntityTreatmentDecoder().object_hook(d)
        return d


class AttributeTreatment(Treatment):
    def __init__(self, *, attribute: Attribute):
        super().__init__(name=attribute.name)
        self.__attribute = attribute

    def __repr__(self):
        return "AttributeTreatment(attribute={})".format(
            repr(self.__attribute))

    def __eq__(self, other):
        if not isinstance(other, AttributeTreatment):
            return False
        return self.attribute == other.attribute

    @property
    def attribute(self):
        return self.__attribute


class AttributeTreatmentEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, AttributeTreatment):
            rep = dict()
            rep['treatment_type'] = 'attribute_treatment'
            rep['attribute'] = AttributeEncoder().default(obj.attribute)
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
        if 'attribute' not in d:
            return d
        return AttributeTreatment(
            attribute=AttributeDecoder().object_hook(d['attribute'])
        )


class EntityTreatment(Treatment):
    def __init__(self, *, entity: NamedEntity):
        super().__init__(name=entity.name)
        self.__entity = entity

    def __repr__(self):
        return "EntityTreatment(entity={})".format(
            repr(self.entity))

    def __eq__(self, other):
        if not isinstance(other, EntityTreatment):
            return False
        return self.entity == other.entity

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
        if 'entity' not in d:
            return d
        return EntityTreatment(
            entity=NamedEntityDecoder().object_hook(d['entity'])
        )
