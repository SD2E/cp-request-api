import json
import pytest
from cp_request import Version
from cp_request.version import VersionEncoder, VersionDecoder


class TestVersion:

    def test_methods(self):
        version = Version(major=1, minor=0, patch=2)
        version2 = Version(major=1, minor=0, patch=2)
        version3 = Version(major=3, minor=0, patch=2)
        assert repr(version) == "Version(major=1, minor=0, patch=2)"
        assert str(version) == "1.0.2"

        assert version == version2
        assert version != version3
        assert version.major == 1
        assert version.minor == 0
        assert version.patch == 2

    def test_serialization(self):
        v = Version(major=1, minor=0, patch=2)
        json_string = json.dumps(v, cls=VersionEncoder)
        assert json_string == '{"major": 1, "minor": 0, "patch": 2}'
        v_load = json.loads(json_string, cls=VersionDecoder)
        assert v_load == v

    def test_equals(self):
        v = Version(major=1, minor=0, patch=2)
        assert v != {}
