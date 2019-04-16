import json
import pytest
from cp_request import Unit
from cp_request.unit import UnitEncoder, UnitDecoder


class TestUnit:

    def test_methods(self):
        u1 = Unit(reference="http://purl.obolibrary.org/obo/UO_0000064")
        u2 = Unit(reference="http://purl.obolibrary.org/obo/UO_0000064")
        assert u1 == u2
        assert u1 != {}

        assert repr(
            u1) == "Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')"
        assert str(u1) == "http://purl.obolibrary.org/obo/UO_0000064"

    def test_serialization(self):
        u = Unit(reference="http://purl.obolibrary.org/obo/UO_0000064")
        u_json = json.dumps(u, cls=UnitEncoder)
        u2 = json.loads(u_json, cls=UnitDecoder)
        assert u == u2
