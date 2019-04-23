import json
import pytest

from cp_request import (
    Attribute, AttributeEncoder, AttributeDecoder,
    Unit,
    Value
)


class TestAttribute:

    def test_bound_attribute(self):
        a1 = Attribute.create_from(
            name='temperature',
            value=Value(
                value=37.2,
                unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000027')
            )
        )
        a2 = Attribute.create_from(
            name='temperature',
            value=Value(
                value=37.2,
                unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000027')
            )
        )
        assert a1 == a1
        assert a1 == a2
        assert a1 != {}

        assert repr(
            a1) == "BoundAttribute(name='temperature', value=Value(value=37.2, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000027')))"

    def test_bound_attribute_serialization(self):
        a1 = Attribute.create_from(
            name='temperature',
            value=Value(
                value='',
                unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000027')
            )
        )
        a_json = json.dumps(a1, cls=AttributeEncoder)
        a2 = json.loads(a_json, cls=AttributeDecoder)
        assert a1 == a2

    def test_unbound_attribute(self):
        t1 = Attribute.create_from(
            name='timepoint', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000027'))
        t2 = Attribute.create_from(
            name='timepoint', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000027'))
        assert t1 == t1
        assert t1 == t2
        assert t1 != {}

        assert repr(
            t1) == "UnboundAttribute(name='timepoint', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000027'))"

    def test_unbound_attribute_serialization(self):
        t1 = Attribute.create_from(
            name='timepoint', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000027'))
        t_json = json.dumps(t1, cls=AttributeEncoder)
        t2 = json.loads(t_json, cls=AttributeDecoder)
        assert t1 == t2