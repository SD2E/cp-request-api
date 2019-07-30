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
    BlockReference,
    DesignBlock,
    GenerateBlock,
    ProductBlock,
    ReplicateBlock,
    SubjectReference,
    SumBlock,
    TupleBlock,
    TreatmentReference
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
    ref = "https://hub.sd2e.org/user/sd2e/design/MG1655_empty_landing_pads/1"
    return NamedEntity(
        name="MG1655_empty_landing_pads",
        reference=ref
    )


@pytest.fixture
def timepoint():
    hour_unit = Unit(
        reference='http://purl.obolibrary.org/obo/UO_0000032'
    )
    return Treatment.create_from(
        attribute=Attribute.create_from(
            name='timepoint',
            unit=hour_unit)
    )


@pytest.fixture()
def kan():
    microgram_per_milliliter_unit = Unit(
        reference='http://purl.obolibrary.org/obo/UO_0000274')
    return Treatment.create_from(
        entity=NamedEntity(
            name='Kan',
            reference='https://hub.sd2e.org/user/sd2e/design/Kan/1',
            attributes=[
                Attribute.create_from(
                    name='concentration', unit=microgram_per_milliliter_unit)
            ])
    )


@pytest.fixture
def temperature():
    temperature_unit = Unit(
        reference='http://purl.obolibrary.org/obo/UO_0000027')
    return Treatment.create_from(
        attribute=Attribute.create_from(
            name='temperature',
            value=Value(
                value=37.0,
                unit=temperature_unit
            )))


@pytest.fixture
def strain_block(nand_circuit, empty_landing_pads, kan):
    return DesignBlock(
        label='strains',
        definition=SumBlock(block_list=[
            TupleBlock(block_list=[
                SubjectReference(entity=nand_circuit),
                TreatmentReference(treatment=kan)
            ]),
            SubjectReference(entity=empty_landing_pads)
        ])
    )


@pytest.fixture
def temperature_block():
    temperature_unit = Unit(
        reference='http://purl.obolibrary.org/obo/UO_0000027')
    media = Treatment.create_from(
        entity=NamedEntity(
            name="M9 Glucose CAA",
            reference="https://hub.sd2e.org/user/sd2e/design/M9_glucose_CAA/1"
        ))
    temperature = Treatment.create_from(
        attribute=Attribute.create_from(
            name='temperature',
            value=Value(
                value=37.0,
                unit=temperature_unit
            )))
    return DesignBlock(
        label='temperature-media',
        definition=TupleBlock(block_list=[
            TreatmentReference(treatment=temperature),
            TreatmentReference(treatment=media)
        ])
    )


@pytest.fixture
def condition_block(iptg):
    micromolar_unit = Unit(
        reference='http://purl.obolibrary.org/obo/UO_0000064')
    l_arabinose = Treatment.create_from(
        entity=NamedEntity(
            name='L-arabinose',
            reference='https://hub.sd2e.org/user/sd2e/design/Larabinose/1',
            attributes=[
                Attribute.create_from(
                    name='concentration', unit=micromolar_unit)
            ])
    )
    return DesignBlock(
        label='conditions',
        definition=ProductBlock(block_list=[
            GenerateBlock(
                treatment=iptg,
                attribute_name='concentration',
                values=[
                    Value(
                        value=0,
                        unit=micromolar_unit),
                    Value(
                        value=0.25,
                        unit=micromolar_unit),
                    Value(
                        value=2.5,
                        unit=micromolar_unit),
                    Value(
                        value=25,
                        unit=micromolar_unit),
                    Value(
                        value=250,
                        unit=micromolar_unit)
                ]),
            GenerateBlock(
                treatment=l_arabinose,
                attribute_name='concentration',
                values=[
                    Value(
                        value=0,
                        unit=micromolar_unit),
                    Value(
                        value=5,
                        unit=micromolar_unit),
                    Value(
                        value=50,
                        unit=micromolar_unit),
                    Value(
                        value=500,
                        unit=micromolar_unit),
                    Value(
                        value=5000,
                        unit=micromolar_unit),
                    Value(
                        value=25000,
                        unit=micromolar_unit)
                ]),
        ])
    )


@pytest.fixture
def experiment_block(strain_block, temperature_block, condition_block, timepoint):
    hour_unit = Unit(reference='http://purl.obolibrary.org/obo/UO_0000032')
    return DesignBlock(
        label='experiment',
        definition=ProductBlock(block_list=[
            ReplicateBlock(
                count=4,
                block=ProductBlock(block_list=[
                    BlockReference(block=strain_block),
                    BlockReference(block=temperature_block),
                    BlockReference(block=condition_block)
                ])
            ),
            GenerateBlock(
                treatment=timepoint,
                attribute_name='timepoint',
                values=[
                    Value(
                        value=5,
                        unit=hour_unit),
                    Value(
                        value=6.5,
                        unit=hour_unit),
                    Value(
                        value=8,
                        unit=hour_unit),
                    Value(
                        value=18,
                        unit=hour_unit)
                ]
            ),
        ])
    )


class DummyMeasurementDecoder(json.JSONDecoder):
    def __init__(self):
        self.__symbol_table = dict()
        self.__add_symbol(nand_circuit())
        self.__add_symbol(empty_landing_pads())
        self.__add_symbol(timepoint())
        self.__add_symbol(
            experiment_block(
                strain_block(
                    nand_circuit(),
                    empty_landing_pads(), kan()
                ),
                temperature_block(),
                condition_block(iptg()),
                timepoint()))
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        return MeasurementDecoder(self.__symbol_table).object_hook(d)

    def __add_symbol(self, obj):
        if isinstance(obj, DesignBlock):
            self.__symbol_table[obj.label] = obj
        else:
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
                    TreatmentReference.create_from(
                        treatment=timepoint,
                        value=Value(
                            value=18,
                            unit=Unit(
                                reference='http://purl.obolibrary.org/obo/UO_0000032'
                            )
                        )
                    ),
                    TreatmentReference.create_from(
                        treatment=iptg,
                        value=Value(
                            value=0,
                            unit=Unit(
                                reference='http://purl.obolibrary.org/obo/UO_0000064'
                            )
                        )
                    )
                ]
            )
        )
        c2 = Control(
            name='positive_gfp',
            sample=Sample(
                subject=nand_circuit,
                treatments=[
                    TreatmentReference.create_from(
                        treatment=timepoint,
                        value=Value(
                            value=18,
                            unit=Unit(
                                reference='http://purl.obolibrary.org/obo/UO_0000032'
                            )
                        )
                    ),
                    TreatmentReference.create_from(
                        treatment=iptg,
                        value=Value(
                            value=0,
                            unit=Unit(
                                reference='http://purl.obolibrary.org/obo/UO_0000064'
                            )
                        )
                    )
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
                            value=18,
                            unit=Unit(
                                reference='http://purl.obolibrary.org/obo/UO_0000032'
                            )
                        )
                    ),
                    TreatmentReference.create_from(
                        treatment=iptg,
                        value=Value(
                            value=0, unit=Unit(
                                reference='http://purl.obolibrary.org/obo/UO_0000064'
                            )
                        )
                    )
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
                TreatmentReference.create_from(
                    treatment=timepoint,
                    value=Value(
                        value=18,
                        unit=Unit(
                            reference='http://purl.obolibrary.org/obo/UO_0000032'
                        )
                    )
                ),
                TreatmentReference.create_from(
                    treatment=iptg,
                    value=Value(
                        value=0,
                        unit=Unit(
                            reference='http://purl.obolibrary.org/obo/UO_0000064'
                        )
                    )
                )
            ]
        )
        s2 = Sample(
            subject=nand_circuit,
            treatments=[
                TreatmentReference.create_from(
                    treatment=timepoint,
                    value=Value(
                        value=18,
                        unit=Unit(
                            reference='http://purl.obolibrary.org/obo/UO_0000032'
                        )
                    )
                ),
                TreatmentReference.create_from(
                    treatment=iptg,
                    value=Value(
                        value=0,
                        unit=Unit(
                            reference='http://purl.obolibrary.org/obo/UO_0000064'
                        )
                    )
                )
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
                TreatmentReference.create_from(
                    treatment=timepoint,
                    value=Value(
                        value=18,
                        unit=Unit(
                            reference='http://purl.obolibrary.org/obo/UO_0000032'
                        )
                    )
                ),
                TreatmentReference.create_from(
                    treatment=iptg,
                    value=Value(
                        value=0,
                        unit=Unit(
                            reference='http://purl.obolibrary.org/obo/UO_0000064'
                        )
                    )
                )
            ]
        )
        s_json = json.dumps(s1, cls=SampleEncoder)
        s2 = json.loads(s_json, cls=DummySampleDecoder)
        assert s1 == s2


class TestMeasurement:
    def test_measurement(self, nand_circuit, iptg, timepoint, empty_landing_pads, experiment_block):
        m1 = Measurement(
            type='FLOW',
            block=BlockReference(block=experiment_block),
            controls=[
                Control(
                    name='positive_gfp',
                    sample=Sample(
                        subject=nand_circuit,
                        treatments=[
                            TreatmentReference.create_from(
                                treatment=timepoint,
                                value=Value(
                                    value=18,
                                    unit=Unit(
                                        reference='http://purl.obolibrary.org/obo/UO_0000032'
                                    )
                                )
                            ),
                            TreatmentReference.create_from(
                                treatment=iptg,
                                value=Value(
                                    value=0,
                                    unit=Unit(
                                        reference='http://purl.obolibrary.org/obo/UO_0000064'
                                    )
                                )
                            )
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
            block=BlockReference(block=experiment_block),
            controls=[
                Control(
                    name='positive_gfp',
                    sample=Sample(
                        subject=nand_circuit,
                        treatments=[
                            TreatmentReference.create_from(
                                treatment=timepoint,
                                value=Value(
                                    value=18,
                                    unit=Unit(
                                        reference='http://purl.obolibrary.org/obo/UO_0000032'
                                    )
                                )
                            ),
                            TreatmentReference.create_from(
                                treatment=iptg,
                                value=Value(
                                    value=0,
                                    unit=Unit(
                                        reference='http://purl.obolibrary.org/obo/UO_0000064'
                                    )
                                )
                            )
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
        # TODO: figure out why this fails
        assert repr(m1) == "Measurement(type='FLOW', block=BlockReference(block=DesignBlock(label='experiment', definition=ProductBlock(block_list=[ReplicateBlock(count=4, block=ProductBlock(block_list=[BlockReference(block=DesignBlock(label='strains', definition=SumBlock(block_list=[TupleBlock(block_list=[SubjectReference(entity=NamedEntity(name='MG1655_NAND_Circuit', reference='https://hub.sd2e.org/user/sd2e/design/MG1655_NAND_Circuit/1')), TreatmentReference(treatment=EntityTreatment(entity=NamedEntity(name='Kan', reference='https://hub.sd2e.org/user/sd2e/design/Kan/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000274'))])))]), SubjectReference(entity=NamedEntity(name='MG1655_empty_landing_pads', reference='https://hub.sd2e.org/user/sd2e/design/MG1655_empty_landing_pads/1'))]))), BlockReference(block=DesignBlock(label='temperature-media', definition=TupleBlock(block_list=[TreatmentReference(treatment=AttributeTreatment(attribute=BoundAttribute(name='temperature', value=Value(value=37.0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000027'))))), TreatmentReference(treatment=EntityTreatment(entity=NamedEntity(name='M9 Glucose CAA', reference='https://hub.sd2e.org/user/sd2e/design/M9_glucose_CAA/1')))]))), BlockReference(block=DesignBlock(label='conditions', definition=ProductBlock(block_list=[GenerateBlock(treatment=EntityTreatment(entity=NamedEntity(name='IPTG', reference='https://hub.sd2e.org/user/sd2e/design/IPTG/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])), attribute_name='concentration', values=[Value(value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=0.25, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=2.5, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=25, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=250, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))]), GenerateBlock(treatment=EntityTreatment(entity=NamedEntity(name='L-arabinose', reference='https://hub.sd2e.org/user/sd2e/design/Larabinose/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])), attribute_name='concentration', values=[Value(value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=5, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=50, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=500, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=5000, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=25000, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])])))])), GenerateBlock(treatment=AttributeTreatment(attribute=UnboundAttribute(name='timepoint', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))), attribute_name='timepoint', values=[Value(value=5, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032')), Value(value=6.5, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032')), Value(value=8, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032')), Value(value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))])]))), controls=[Control(name='positive_gfp', sample=Sample(subject=NamedEntity(name='MG1655_NAND_Circuit', reference='https://hub.sd2e.org/user/sd2e/design/MG1655_NAND_Circuit/1'), treatments=[TreatmentValueReference(treatment=AttributeTreatment(attribute=UnboundAttribute(name='timepoint', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))), value=Value(value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))), TreatmentValueReference(treatment=EntityTreatment(entity=NamedEntity(name='IPTG', reference='https://hub.sd2e.org/user/sd2e/design/IPTG/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])), value=Value(value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))])), Control(name='negative_gfp', sample=Sample(subject=NamedEntity(name='MG1655_empty_landing_pads', reference='https://hub.sd2e.org/user/sd2e/design/MG1655_empty_landing_pads/1'), treatments=[]))], performers=['Ginkgo'])"

    def test_measurement_serialization(self, nand_circuit, timepoint, iptg, empty_landing_pads, experiment_block):
        m1 = Measurement(
            type='FLOW',
            block=BlockReference(block=experiment_block),
            controls=[
                Control(
                    name='positive_gfp',
                    sample=Sample(
                        subject=nand_circuit,
                        treatments=[
                            TreatmentReference.create_from(
                                treatment=timepoint,
                                value=Value(
                                    value=18,
                                    unit=Unit(
                                        reference='http://purl.obolibrary.org/obo/UO_0000032'
                                    )
                                )
                            ),
                            TreatmentReference.create_from(
                                treatment=iptg,
                                value=Value(
                                    value=0,
                                    unit=Unit(
                                        reference='http://purl.obolibrary.org/obo/UO_0000064'
                                    )
                                )
                            )
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
