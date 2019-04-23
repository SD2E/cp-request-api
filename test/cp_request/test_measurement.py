import json
import pytest

from cp_request import (
    Attribute,
    Control, ControlEncoder, ControlDecoder,
    NamedEntity,
    Sample, SampleEncoder, SampleDecoder,
    Treatment,
    Measurement, MeasurementEncoder, MeasurementDecoder,
    Unit, Value
)
from cp_request.design import (
    BlockReference, TreatmentReference
)


@pytest.fixture
def nand_circuit():
    return NamedEntity(
        name="MG1655_NAND_Circuit",
        reference="https://hub.sd2e.org/user/sd2e/design/MG1655_NAND_Circuit/1"
    )


@pytest.fixture
def iptg():
    micromolar_unit = Unit(
        reference='http://purl.obolibrary.org/obo/UO_0000064')
    return Treatment.create_from(
        entity=NamedEntity(
            name='IPTG',
            reference='https://hub.sd2e.org/user/sd2e/design/IPTG/1',
            attributes=[
                Attribute.create_from(
                    name='concentration', unit=micromolar_unit)
            ])
    )


@pytest.fixture
def empty_landing_pads():
    return NamedEntity(
        name="MG1655_empty_landing_pads",
        reference="https://hub.sd2e.org/user/sd2e/design/MG1655_empty_landing_pads/1"
    )


@pytest.fixture
def timepoint():
    hour_unit = Unit(reference='http://purl.obolibrary.org/obo/UO_0000032')
    return Treatment.create_from(
        attribute=Attribute.create_from(
            name='timepoint',
            unit=hour_unit)
    )


class DummyMeasurementDecoder(json.JSONDecoder):
    def __init__(self):
        self.__symbol_table = dict()
        self.__add_symbol(nand_circuit())
        self.__add_symbol(empty_landing_pads())
        self.__add_symbol(timepoint())
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        return MeasurementDecoder(self.__symbol_table).object_hook(d)

    def __add_symbol(self, obj):
        self.__symbol_table[obj.name] = obj


class DummySampleDecoder(json.JSONDecoder):
    def __init__(self):
        self.__symbol_table = dict()
        self.__add_symbol(nand_circuit())
        self.__add_symbol(empty_landing_pads())
        self.__add_symbol(timepoint())
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        return SampleDecoder(self.__symbol_table).object_hook(d)

    def __add_symbol(self, obj):
        self.__symbol_table[obj.name] = obj


class DummyControlDecoder(json.JSONDecoder):
    def __init__(self):
        self.__symbol_table = dict()
        self.__add_symbol(nand_circuit())
        self.__add_symbol(empty_landing_pads())
        self.__add_symbol(timepoint())
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        return ControlDecoder(self.__symbol_table).object_hook(d)

    def __add_symbol(self, obj):
        self.__symbol_table[obj.name] = obj


class TestControl:
    def test_control(self, nand_circuit, timepoint, iptg):
        c1 = Control(
            name='positive_gfp',
            sample=Sample(
                subject=nand_circuit,
                treatments=[
                    TreatmentReference.create_from(treatment=timepoint, value=Value(
                        value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))),
                    TreatmentReference.create_from(
                        treatment=iptg,
                        value=Value(
                            value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))
                ]
            )
        )
        c2 = Control(
            name='positive_gfp',
            sample=Sample(
                subject=nand_circuit,
                treatments=[
                    TreatmentReference.create_from(treatment=timepoint, value=Value(
                        value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))),
                    TreatmentReference.create_from(
                        treatment=iptg,
                        value=Value(
                            value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))
                ]
            )
        )
        assert c1 == c1
        assert c1 == c2
        assert c1 != {}
        assert repr(
            c1) == "Control(name='positive_gfp', sample=Sample(subject=NamedEntity(name='MG1655_NAND_Circuit', reference='https://hub.sd2e.org/user/sd2e/design/MG1655_NAND_Circuit/1'), treatments=[TreatmentValueReference(treatment=AttributeTreatment(attribute=UnboundAttribute(name='timepoint', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))), value=Value(value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))), TreatmentValueReference(treatment=EntityTreatment(entity=NamedEntity(name='IPTG', reference='https://hub.sd2e.org/user/sd2e/design/IPTG/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])), value=Value(value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))]))"

    def test_control_serialization(self, nand_circuit, timepoint, iptg):
        c1 = Control(
            name='positive_gfp',
            sample=Sample(
                subject=nand_circuit,
                treatments=[
                    TreatmentReference.create_from(
                        treatment=timepoint,
                        value=Value(
                            value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))),
                    TreatmentReference.create_from(
                        treatment=iptg,
                        value=Value(
                            value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))
                ]
            )
        )
        c_json = json.dumps(c1, cls=ControlEncoder)
        c2 = json.loads(c_json, cls=DummyControlDecoder)
        assert c1 == c2

    def test_control_subject(self, empty_landing_pads):
        c1 = Control(
            name='negative_gfp',
            sample=Sample(subject=empty_landing_pads)
        )
        c2 = Control(
            name='negative_gfp',
            sample=Sample(subject=empty_landing_pads)
        )
        assert c1 == c1
        assert c1 == c2
        assert c1 != {}
        assert repr(
            c1) == "Control(name='negative_gfp', sample=Sample(subject=NamedEntity(name='MG1655_empty_landing_pads', reference='https://hub.sd2e.org/user/sd2e/design/MG1655_empty_landing_pads/1'), treatments=[]))"

    def test_control_subject_serialization(self, empty_landing_pads):
        c1 = Control(
            name='negative_gfp',
            sample=Sample(subject=empty_landing_pads)
        )
        c_json = json.dumps(c1, cls=ControlEncoder)
        c2 = json.loads(c_json, cls=DummyControlDecoder)
        assert c1 == c2


class TestSample:
    def test_sample(self, nand_circuit, timepoint, iptg):
        s1 = Sample(
            subject=nand_circuit,
            treatments=[
                TreatmentReference.create_from(treatment=timepoint, value=Value(
                    value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))),
                TreatmentReference.create_from(
                    treatment=iptg,
                    value=Value(
                        value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))
            ]
        )
        s2 = Sample(
            subject=nand_circuit,
            treatments=[
                TreatmentReference.create_from(treatment=timepoint, value=Value(
                    value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))),
                TreatmentReference.create_from(
                    treatment=iptg,
                    value=Value(
                        value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))
            ]
        )
        assert s1 == s1
        assert s1 == s2
        assert s1 != {}
        assert repr(
            s1) == "Sample(subject=NamedEntity(name='MG1655_NAND_Circuit', reference='https://hub.sd2e.org/user/sd2e/design/MG1655_NAND_Circuit/1'), treatments=[TreatmentValueReference(treatment=AttributeTreatment(attribute=UnboundAttribute(name='timepoint', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))), value=Value(value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))), TreatmentValueReference(treatment=EntityTreatment(entity=NamedEntity(name='IPTG', reference='https://hub.sd2e.org/user/sd2e/design/IPTG/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])), value=Value(value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))])"

    def test_sample_serialization(self, nand_circuit, timepoint, iptg):
        s1 = Sample(
            subject=nand_circuit,
            treatments=[
                TreatmentReference.create_from(treatment=timepoint, value=Value(
                    value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))),
                TreatmentReference.create_from(
                    treatment=iptg,
                    value=Value(
                        value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))
            ]
        )
        s_json = json.dumps(s1, cls=SampleEncoder)
        s2 = json.loads(s_json, cls=DummySampleDecoder)
        assert s1 == s2


class TestMeasurement:
    def test_measurement(self, nand_circuit, iptg, timepoint, empty_landing_pads):
        m1 = Measurement(
            type='FLOW',
            block=BlockReference(label='experiment'),
            controls=[
                Control(
                    name='positive_gfp',
                    sample=Sample(
                        subject=nand_circuit,
                        treatments=[
                            TreatmentReference.create_from(treatment=timepoint, value=Value(
                                value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))),
                            TreatmentReference.create_from(
                                treatment=iptg,
                                value=Value(
                                    value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))
                        ]
                    )
                ),
                Control(
                    name='negative_gfp',
                    sample=Sample(subject=empty_landing_pads)
                )
            ],
            performers=['Ginkgo']
        )
        m2 = Measurement(
            type='FLOW',
            block=BlockReference(label='experiment'),
            controls=[
                Control(
                    name='positive_gfp',
                    sample=Sample(
                        subject=nand_circuit,
                        treatments=[
                            TreatmentReference.create_from(treatment=timepoint, value=Value(
                                value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))),
                            TreatmentReference.create_from(
                                treatment=iptg,
                                value=Value(
                                    value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))
                        ]
                    )
                ),
                Control(
                    name='negative_gfp',
                    sample=Sample(subject=empty_landing_pads)
                )
            ],
            performers=['Ginkgo']
        )
        assert m1 == m1
        assert m1 == m2
        assert m1 != {}
        assert repr(m1) == "Measurement(type='FLOW', block=BlockReference(label='experiment'), controls=[Control(name='positive_gfp', sample=Sample(subject=NamedEntity(name='MG1655_NAND_Circuit', reference='https://hub.sd2e.org/user/sd2e/design/MG1655_NAND_Circuit/1'), treatments=[TreatmentValueReference(treatment=AttributeTreatment(attribute=UnboundAttribute(name='timepoint', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))), value=Value(value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))), TreatmentValueReference(treatment=EntityTreatment(entity=NamedEntity(name='IPTG', reference='https://hub.sd2e.org/user/sd2e/design/IPTG/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])), value=Value(value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))])), Control(name='negative_gfp', sample=Sample(subject=NamedEntity(name='MG1655_empty_landing_pads', reference='https://hub.sd2e.org/user/sd2e/design/MG1655_empty_landing_pads/1'), treatments=[]))], performers=['Ginkgo'])"

    def test_measurement_serialization(self, nand_circuit, timepoint, iptg, empty_landing_pads):
        m1 = Measurement(
            type='FLOW',
            block=BlockReference(label='experiment'),
            controls=[
                Control(
                    name='positive_gfp',
                    sample=Sample(
                        subject=nand_circuit,
                        treatments=[
                            TreatmentReference.create_from(treatment=timepoint, value=Value(
                                value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))),
                            TreatmentReference.create_from(
                                treatment=iptg,
                                value=Value(
                                    value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))
                        ]
                    )
                ),
                Control(
                    name='negative_gfp',
                    sample=Sample(subject=empty_landing_pads)
                )
            ],
            performers=['Ginkgo']
        )
        m_json = json.dumps(m1, cls=MeasurementEncoder)
        m2 = json.loads(m_json, cls=DummyMeasurementDecoder)
        assert m1 == m2
