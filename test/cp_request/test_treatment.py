import json
import pytest

from cp_request.treatment import (
    AttributeTreatment,
    Treatment, TreatmentEncoder, TreatmentDecoder
)
from cp_request import NamedEntity, Unit, Value


class TestTreatment:

    def test_attribute(self):
        t1 = Treatment.create_from(
            name='timepoint', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000027'))
        t2 = Treatment.create_from(
            name='timepoint', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000027'))
        assert t1 == t1
        assert t1 == t2
        assert t1 != {}

        assert repr(
            t1) == "AttributeTreatment(name='timepoint', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000027'))"

    def test_attribute_serialization(self):
        t1 = Treatment.create_from(
            name='timepoint', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000027'))
        t_json = json.dumps(t1, cls=TreatmentEncoder)
        t2 = json.loads(t_json, cls=TreatmentDecoder)
        assert t1 == t2

    def test_entity(self):
        t1 = Treatment.create_from(name='media',
                                   entity=NamedEntity(
                                       name='M9 Glucose CAA',
                                       reference='https://hub.sd2e.org/user/sd2e/design/M9_glucose_CAA/1'
                                   ))
        t2 = Treatment.create_from(name='media',
                                   entity=NamedEntity(
                                       name='M9 Glucose CAA',
                                       reference='https://hub.sd2e.org/user/sd2e/design/M9_glucose_CAA/1'
                                   ))
        assert t1 == t1
        assert t1 == t2
        assert t1 != {}

        assert repr(t1) == "EntityTreatment(name='media', entity=NamedEntity(name='M9 Glucose CAA', reference='https://hub.sd2e.org/user/sd2e/design/M9_glucose_CAA/1'))"

    def test_entity_serialization(self):
        t1 = Treatment.create_from(name='media',
                                   entity=NamedEntity(
                                       name='M9 Glucose CAA',
                                       reference='https://hub.sd2e.org/user/sd2e/design/M9_glucose_CAA/1'
                                   ))
        t_json = json.dumps(t1, cls=TreatmentEncoder)
        t2 = json.loads(t_json, cls=TreatmentDecoder)
        assert t1 == t2

    def test_entity_attribute(self):
        t1 = Treatment.create_from(
            name='IPTG',
            entity=NamedEntity(
                name='IPTG',
                reference='https://hub.sd2e.org/user/sd2e/design/IPTG/1'),
            attributes=[
                AttributeTreatment(
                    name='concentration',
                    unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')
                )
            ]
        )
        t2 = Treatment.create_from(
            name='IPTG',
            entity=NamedEntity(
                name='IPTG',
                reference='https://hub.sd2e.org/user/sd2e/design/IPTG/1'),
            attributes=[
                AttributeTreatment(
                    name='concentration',
                    unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')
                )
            ]
        )
        assert t1 == t1
        assert t1 == t2
        assert t1 != {}

        assert repr(
            t1) == "EntityAttributeTreatment(name='IPTG', entity=NamedEntity(name='IPTG', reference='https://hub.sd2e.org/user/sd2e/design/IPTG/1'), attributes=[AttributeTreatment(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])"

    def test_entity_attribute_serialization(self):
        t1 = Treatment.create_from(
            name='IPTG',
            entity=NamedEntity(
                name='IPTG',
                reference='https://hub.sd2e.org/user/sd2e/design/IPTG/1'),
            attributes=[
                AttributeTreatment(
                    name='concentration',
                    unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')
                )
            ]
        )
        t_json = json.dumps(t1, cls=TreatmentEncoder)
        t2 = json.loads(t_json, cls=TreatmentDecoder)
        assert t1 == t2

    def test_simple_treatment(self):
        t1 = Treatment.create_from(
            name='temperature',
            value=Value(
                value='',
                unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000027')
            )
        )
        t2 = Treatment.create_from(
            name='temperature',
            value=Value(
                value='',
                unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000027')
            )
        )
        assert t1 == t1
        assert t1 == t2
        assert t1 != {}

        assert repr(t1) == "SimpleTreatment(name='temperature', value=Value(value=, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000027')))"

    def test_simple_treatment_serialization(self):
        t1 = Treatment.create_from(
            name='temperature',
            value=Value(
                value='',
                unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000027')
            )
        )
        t_json = json.dumps(t1, cls=TreatmentEncoder)
        t2 = json.loads(t_json, cls=TreatmentDecoder)
        assert t1 == t2