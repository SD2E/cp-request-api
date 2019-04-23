import json
import pytest

from cp_request import Attribute, NamedEntity, Unit, Value
from cp_request.named_entity import NamedEntityEncoder, NamedEntityDecoder


class TestNamedEntity:

    def test_entity(self):
        e1 = NamedEntity(name="one", reference="http://one.one")
        e2 = NamedEntity(name="one", reference="http://one.one")
        assert e1 == e2
        assert e1 != {}

        assert repr(e1) == "NamedEntity(name='one', reference='http://one.one')"
        assert str(e1) == "NamedEntity(name='one', reference='http://one.one')"

    def test_serialization(self):
        e1 = NamedEntity(name="one", reference="http://one.one")
        e_json = json.dumps(e1, cls=NamedEntityEncoder)
        e2 = json.loads(e_json, cls=NamedEntityDecoder)
        assert e1 == e2

    def test_entity_attributes(self):
        e1 = NamedEntity(name="one",
                         reference="http://one.one",
                         attributes=[
                             Attribute.create_from(
                                 name='concentration',
                                 value=Value(value=0.25, unit=Unit(
                                     reference='http://purl.obolibrary.org/obo/UO_0000064')))
                         ])
