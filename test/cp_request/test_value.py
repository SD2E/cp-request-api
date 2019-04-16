import json
import pytest

from cp_request import Unit, Value, ValueEncoder, ValueDecoder


class TestValue:

    def test_value(self):
        v1 = Value(value=37, unit=Unit(
            reference='http://purl.obolibrary.org/obo/UO_0000027'))
        v2 = Value(value=37, unit=Unit(
            reference='http://purl.obolibrary.org/obo/UO_0000027'))
        assert v1 == v1
        assert v1 == v2
        assert v1 != {}
        assert repr(v1) == "Value(value=37, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000027'))"

    def test_value_serialization(self):
        v1 = Value(value=37, unit=Unit(
            reference='http://purl.obolibrary.org/obo/UO_0000027'))
        v_json = json.dumps(v1, cls=ValueEncoder)
        v2 = json.loads(v_json, cls=ValueDecoder)
        assert v1 == v2