import json
import pytest

from cp_request import NamedEntity
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
