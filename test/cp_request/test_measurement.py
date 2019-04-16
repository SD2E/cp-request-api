import json
import pytest

from cp_request import (
    Control, ControlEncoder, ControlDecoder,
    Sample, SampleEncoder, SampleDecoder,
    Measurement, MeasurementEncoder, MeasurementDecoder,
    Unit, Value
)
from cp_request.design import (
    BlockReference, SubjectReference, TreatmentReference
)


class TestControl:
    def test_control(self):
        c1 = Control(
            name='positive_gfp',
            sample=Sample(
                subject=SubjectReference(
                    entity_name='MG1655_NAND_Circuit'),
                treatments=[
                    TreatmentReference.create_from(treatment_name='timepoint', value=Value(
                        value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))),
                    TreatmentReference.create_from(treatment_name='IPTG', attribute='concentration', value=Value(
                        value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))
                ]
            )
        )
        c2 = Control(
            name='positive_gfp',
            sample=Sample(
                subject=SubjectReference(
                    entity_name='MG1655_NAND_Circuit'),
                treatments=[
                    TreatmentReference.create_from(treatment_name='timepoint', value=Value(
                        value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))),
                    TreatmentReference.create_from(treatment_name='IPTG', attribute='concentration', value=Value(
                        value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))
                ]
            )
        )
        assert c1 == c1
        assert c1 == c2
        assert c1 != {}
        assert repr(
            c1) == "Control(name='positive_gfp', sample=Sample(subject=SubjectReference(entity='MG1655_NAND_Circuit'), treatments=[TreatmentValueReference(treatment_name='timepoint', value=Value(value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))), TreatmentAttributeValueReference(treatment_name='IPTG', attribute='concentration', value=Value(value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))]))"

    def test_control_serialization(self):
        c1 = Control(
            name='positive_gfp',
            sample=Sample(
                subject=SubjectReference(
                    entity_name='MG1655_NAND_Circuit'),
                treatments=[
                    TreatmentReference.create_from(treatment_name='timepoint', value=Value(
                        value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))),
                    TreatmentReference.create_from(treatment_name='IPTG', attribute='concentration', value=Value(
                        value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))
                ]
            )
        )
        c_json = json.dumps(c1, cls=ControlEncoder)
        c2 = json.loads(c_json, cls=ControlDecoder)
        assert c1 == c2

    def test_control_subject(self):
        c1 = Control(
            name='negative_gfp',
            sample=Sample(subject=SubjectReference(
                entity_name='MG1655_empty_landing_pads'))
        )
        c2 = Control(
            name='negative_gfp',
            sample=Sample(subject=SubjectReference(
                entity_name='MG1655_empty_landing_pads'))
        )
        assert c1 == c1
        assert c1 == c2
        assert c1 != {}
        assert repr(
            c1) == "Control(name='negative_gfp', sample=Sample(subject=SubjectReference(entity='MG1655_empty_landing_pads'), treatments=[]))"

    def test_control_subject_serialization(self):
        c1 = Control(
            name='negative_gfp',
            sample=Sample(subject=SubjectReference(
                entity_name='MG1655_empty_landing_pads'))
        )
        c_json = json.dumps(c1, cls=ControlEncoder)
        c2 = json.loads(c_json, cls=ControlDecoder)
        assert c1 == c2


class TestSample:
    def test_sample(self):
        s1 = Sample(
            subject=SubjectReference(entity_name='MG1655_NAND_Circuit'),
            treatments=[
                TreatmentReference.create_from(
                    treatment_name='timepoint',
                    value=Value(
                        value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))),
                TreatmentReference.create_from(
                    treatment_name='IPTG', attribute='concentration',
                    value=Value(
                        value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))
            ]
        )
        s2 = Sample(
            subject=SubjectReference(entity_name='MG1655_NAND_Circuit'),
            treatments=[
                TreatmentReference.create_from(treatment_name='timepoint', value=Value(
                    value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))),
                TreatmentReference.create_from(treatment_name='IPTG', attribute='concentration', value=Value(
                    value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))
            ]
        )
        assert s1 == s1
        assert s1 == s2
        assert s1 != {}
        assert repr(
            s1) == "Sample(subject=SubjectReference(entity='MG1655_NAND_Circuit'), treatments=[TreatmentValueReference(treatment_name='timepoint', value=Value(value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))), TreatmentAttributeValueReference(treatment_name='IPTG', attribute='concentration', value=Value(value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))])"

    def test_sample_serialization(self):
        s1 = Sample(
            subject=SubjectReference(entity_name='MG1655_NAND_Circuit'),
            treatments=[
                TreatmentReference.create_from(treatment_name='timepoint', value=Value(
                    value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))),
                TreatmentReference.create_from(treatment_name='IPTG', attribute='concentration', value=Value(
                    value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))
            ]
        )
        s_json = json.dumps(s1, cls=SampleEncoder)
        s2 = json.loads(s_json, cls=SampleDecoder)
        assert s1 == s2


class TestMeasurement:
    def test_measurement(self):
        m1 = Measurement(
            type='FLOW',
            block=BlockReference(label='experiment'),
            controls=[
                Control(
                    name='positive_gfp',
                    sample=Sample(
                        subject=SubjectReference(
                            entity_name='MG1655_NAND_Circuit'),
                        treatments=[
                            TreatmentReference.create_from(treatment_name='timepoint', value=Value(
                                value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))),
                            TreatmentReference.create_from(treatment_name='IPTG', attribute='concentration', value=Value(
                                value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))
                        ]
                    )
                ),
                Control(
                    name='negative_gfp',
                    sample=Sample(subject=SubjectReference(
                        entity_name='MG1655_empty_landing_pads'))
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
                        subject=SubjectReference(
                            entity_name='MG1655_NAND_Circuit'),
                        treatments=[
                            TreatmentReference.create_from(treatment_name='timepoint', value=Value(
                                value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))),
                            TreatmentReference.create_from(treatment_name='IPTG', attribute='concentration', value=Value(
                                value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))
                        ]
                    )
                ),
                Control(
                    name='negative_gfp',
                    sample=Sample(subject=SubjectReference(
                        entity_name='MG1655_empty_landing_pads'))
                )
            ],
            performers=['Ginkgo']
        )
        assert m1 == m1
        assert m1 == m2
        assert m1 != {}
        assert repr(m1) == "Measurement(type='FLOW', block=BlockReference(label='experiment'), controls=[Control(name='positive_gfp', sample=Sample(subject=SubjectReference(entity='MG1655_NAND_Circuit'), treatments=[TreatmentValueReference(treatment_name='timepoint', value=Value(value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))), TreatmentAttributeValueReference(treatment_name='IPTG', attribute='concentration', value=Value(value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))])), Control(name='negative_gfp', sample=Sample(subject=SubjectReference(entity='MG1655_empty_landing_pads'), treatments=[]))], performers=['Ginkgo'])"

    def test_measurement_serialization(self):
        m1 = Measurement(
            type='FLOW',
            block=BlockReference(label='experiment'),
            controls=[
                Control(
                    name='positive_gfp',
                    sample=Sample(
                        subject=SubjectReference(
                            entity_name='MG1655_NAND_Circuit'),
                        treatments=[
                            TreatmentReference.create_from(treatment_name='timepoint', value=Value(
                                value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))),
                            TreatmentReference.create_from(treatment_name='IPTG', attribute='concentration', value=Value(
                                value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))
                        ]
                    )
                ),
                Control(
                    name='negative_gfp',
                    sample=Sample(subject=SubjectReference(
                        entity_name='MG1655_empty_landing_pads'))
                )
            ],
            performers=['Ginkgo']
        )
        m_json = json.dumps(m1, cls=MeasurementEncoder)
        m2 = json.loads(m_json, cls=MeasurementDecoder)
        assert m1 == m2
