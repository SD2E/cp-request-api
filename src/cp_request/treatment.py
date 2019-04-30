"""
Package for classes representing treatments.
"""

import abc
import json
from cp_request import (
    Attribute, AttributeEncoder, AttributeDecoder,
    NamedEntity, NamedEntityEncoder, NamedEntityDecoder
)


class Treatment(abc.ABC):
    """
    Abstract base class for treatments.
    """

    @abc.abstractmethod
    def __init__(self, *, name: str):
        self.__name = name

    @staticmethod
    def create_from(*,
                    attribute: Attribute = None,
                    entity: NamedEntity = None):
        """
        Creates a Treatment object based on the parameters.
        If an attribute is provided, creates an {AttributeTreatment}.
        Or, if an entity is provided, creates an {EntityTreatment}.
        """
        if attribute:
            return AttributeTreatment(attribute=attribute)
        elif entity:
            return EntityTreatment(entity=entity)
        raise CannotCreateTreatmentException(
            'No valid combinations of arguments provided')

    def apply(self, visitor):
        visitor.visit_treatment(self)

    def is_bound(self):
        """
        Indicates that all {Attribute} instances of this {Treatment}
        are bound to a {Value}.
        """
        return False

    @property
    def name(self):
        return self.__name


class CannotCreateTreatmentException(Exception):
    def __init__(self, message):
        super().__init__(message)


class TreatmentEncoder(json.JSONEncoder):
    """
    A JSONEncoder to serialize an instance of {Treatment}.
    """

    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, AttributeTreatment):
            return AttributeTreatmentEncoder().default(obj)
        if isinstance(obj, EntityTreatment):
            return EntityTreatmentEncoder().default(obj)
        return super().default(obj)


class TreatmentDecoder(json.JSONDecoder):
    """
    A JSONDecoder to deserialize an instance of {Treatment}.
    """

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
    """
    Represents an {Treatment} object defined by an {Attribute}.

    Examples are temperature, or time points.
    """

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

    def is_bound(self):
        return self.__attribute.is_bound()


class AttributeTreatmentEncoder(json.JSONEncoder):
    """
    A JSONEncoder for the {AttributeTreatment} class.
    """
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, AttributeTreatment):
            rep = dict()
            rep['treatment_type'] = 'attribute_treatment'
            rep['attribute'] = AttributeEncoder().default(obj.attribute)
            return rep
        return super().default(obj)


class AttributeTreatmentDecoder(json.JSONDecoder):
    """
    A JSONDecoder for the {AttributeTreatment} class.

    Note: the convert method is the object_hook.
    """

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
    """
    Defines a {Treatment} that is defined by a {NamedEntity}.
    """

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
        return self.entity.is_bound()


class EntityTreatmentEncoder(json.JSONEncoder):
    """
    A JSONEncoder for the {EntityTreatment} class.
    """

    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, EntityTreatment):
            rep = dict()
            rep['treatment_type'] = 'entity_treatment'
            rep['entity'] = NamedEntityEncoder().default(obj.entity)
            return rep
        return super().default(obj)


class EntityTreatmentDecoder(json.JSONDecoder):
    """
    A JSONDecoder for the {EntityTreatment} class.

    Note: the convert method is the object_hook.
    """

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
