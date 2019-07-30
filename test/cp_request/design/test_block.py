import pytest

import json
from cp_request import (
    Unit,
    Value, NamedEntity, Attribute, Treatment
)
from cp_request.design import (
    GenerateBlock, ProductBlock, ReplicateBlock, SumBlock,
    BlockReference, SubjectReference, TreatmentReference,
    BlockDefinitionEncoder, BlockDefinitionDecoder,
    DesignBlock, DesignBlockEncoder, DesignBlockDecoder
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
def timepoint():
    hour_unit = Unit(reference='http://purl.obolibrary.org/obo/UO_0000032')
    return Treatment.create_from(
        attribute=Attribute.create_from(
            name='timepoint',
            unit=hour_unit)
    )


@pytest.fixture
def nand_circuit():
    return NamedEntity(
        name="MG1655_NAND_Circuit",
        reference="https://hub.sd2e.org/user/sd2e/design/MG1655_NAND_Circuit/1"
    )


@pytest.fixture
def empty_landing_pads():
    return NamedEntity(
        name="MG1655_empty_landing_pads",
        reference="https://hub.sd2e.org/user/sd2e/design/MG1655_empty_landing_pads/1"
    )


@pytest.fixture
def strain_block(nand_circuit, empty_landing_pads, kan):
    return DesignBlock(
        label='strains',
        definition=SumBlock(block_list=[
            ProductBlock(block_list=[
                SubjectReference(entity=nand_circuit),
                TreatmentReference(treatment=kan)
            ]),
            SubjectReference(entity=empty_landing_pads)
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


class DummyDefinitionDecoder(json.JSONDecoder):
    def __init__(self):
        self.__symbol_table = dict()
        self.__add_symbol(iptg())
        self.__add_symbol(kan())
        self.__add_symbol(temperature())
        self.__add_symbol(timepoint())
        self.__add_symbol(condition_block(iptg()))
        self.__add_symbol(
            strain_block(nand_circuit(), empty_landing_pads(), kan()))
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        return BlockDefinitionDecoder(self.__symbol_table).object_hook(d)

    def __add_symbol(self, obj):
        if isinstance(obj, DesignBlock):
            self.__symbol_table[obj.label] = obj
        else:
            self.__symbol_table[obj.name] = obj


class DummyDesignDecoder(json.JSONDecoder):
    def __init__(self):
        self.__symbol_table = dict()
        self.__add_symbol(iptg())
        self.__add_symbol(kan())
        self.__add_symbol(temperature())
        self.__add_symbol(timepoint())
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        return DesignBlockDecoder(self.__symbol_table).object_hook(d)

    def __add_symbol(self, obj):
        self.__symbol_table[obj.name] = obj


class TestDefinitionBlock:

    def test_generate_block(self, iptg):
        b1 = GenerateBlock(
            treatment=iptg,
            attribute_name='concentration',
            values=[
                Value(value=0, unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000064')),
                Value(value=0.25, unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000064')),
                Value(value=2.5, unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000064')),
                Value(value=25, unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000064')),
                Value(value=250, unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000064'))
            ])
        b2 = GenerateBlock(
            treatment=iptg,
            attribute_name='concentration',
            values=[
                Value(value=0, unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000064')),
                Value(value=0.25, unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000064')),
                Value(value=2.5, unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000064')),
                Value(value=25, unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000064')),
                Value(value=250, unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000064'))
            ])
        assert b1 == b1
        assert b1 == b2
        assert b1 != {}

        assert repr(
            b1) == "GenerateBlock(treatment=EntityTreatment(entity=NamedEntity(name='IPTG', reference='https://hub.sd2e.org/user/sd2e/design/IPTG/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])), attribute_name='concentration', values=[Value(value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=0.25, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=2.5, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=25, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=250, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])"

    def test_generate_block_serialization(self, iptg):
        b1 = GenerateBlock(
            treatment=iptg,
            attribute_name='concentration',
            values=[
                Value(value=0, unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000064')),
                Value(value=0.25, unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000064')),
                Value(value=2.5, unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000064')),
                Value(value=25, unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000064')),
                Value(value=250, unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000064'))
            ])
        b_json = json.dumps(b1, cls=BlockDefinitionEncoder)
        b2 = json.loads(b_json, cls=DummyDefinitionDecoder)
        assert b1 == b2

    def test_product_block(self, temperature, timepoint):
        b1 = ProductBlock(block_list=[
            TreatmentReference(treatment=temperature),
            TreatmentReference(treatment=timepoint)
        ])
        b2 = ProductBlock(block_list=[
            TreatmentReference(treatment=temperature),
            TreatmentReference(treatment=timepoint)
        ])
        assert b1 == b1
        assert b1 == b2
        assert b1 != {}

        assert repr(
            b1) == "ProductBlock(block_list=[TreatmentReference(treatment=AttributeTreatment(attribute=BoundAttribute(name='temperature', value=Value(value=37.0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000027'))))), TreatmentReference(treatment=AttributeTreatment(attribute=UnboundAttribute(name='timepoint', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))))])"

    def test_product_block_serialization(self, temperature, timepoint):
        b1 = ProductBlock(block_list=[
            TreatmentReference(treatment=temperature),
            TreatmentReference(treatment=timepoint)
        ])

        b_json = json.dumps(b1, cls=BlockDefinitionEncoder)
        assert b_json == '{"block_type": "product_block", "block_list": [{"block_type": "treatment_reference", "reference": "temperature"}, {"block_type": "treatment_reference", "reference": "timepoint"}]}'
        b2 = json.loads(b_json, cls=DummyDefinitionDecoder)
        assert b1 == b2

    def test_replicate_block(self, condition_block):
        b1 = ReplicateBlock(count=4,
                            block=BlockReference(block=condition_block))
        b2 = ReplicateBlock(count=4,
                            block=BlockReference(block=condition_block))

        assert b1 == b1
        assert b1 == b2
        assert b1 != {}

        assert repr(
            b1) == "ReplicateBlock(count=4, block=BlockReference(block=DesignBlock(label='conditions', definition=ProductBlock(block_list=[GenerateBlock(treatment=EntityTreatment(entity=NamedEntity(name='IPTG', reference='https://hub.sd2e.org/user/sd2e/design/IPTG/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])), attribute_name='concentration', values=[Value(value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=0.25, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=2.5, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=25, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=250, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))]), GenerateBlock(treatment=EntityTreatment(entity=NamedEntity(name='L-arabinose', reference='https://hub.sd2e.org/user/sd2e/design/Larabinose/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])), attribute_name='concentration', values=[Value(value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=5, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=50, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=500, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=5000, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=25000, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])]))))"

    def test_replicate_block_serialization(self, condition_block):
        b1 = ReplicateBlock(count=4,
                            block=BlockReference(block=condition_block))
        b_json = json.dumps(b1, cls=BlockDefinitionEncoder)
        assert b_json == '{"block_type": "replicate_block", "count": 4, "block": {"block_type": "block_reference", "reference": "conditions"}}'
        b2 = json.loads(b_json, cls=DummyDefinitionDecoder)
        assert b1 == b2

    def test_sum_block(self, condition_block, strain_block):
        b1 = SumBlock(block_list=[
            BlockReference(block=strain_block),
            BlockReference(block=condition_block)
        ])
        b2 = SumBlock(block_list=[
            BlockReference(block=strain_block),
            BlockReference(block=condition_block)
        ])
        assert b1 == b1
        assert b1 == b2
        assert b1 != {}

        assert repr(
            b1) == "SumBlock(block_list=[BlockReference(block=DesignBlock(label='strains', definition=SumBlock(block_list=[ProductBlock(block_list=[SubjectReference(entity=NamedEntity(name='MG1655_NAND_Circuit', reference='https://hub.sd2e.org/user/sd2e/design/MG1655_NAND_Circuit/1')), TreatmentReference(treatment=EntityTreatment(entity=NamedEntity(name='Kan', reference='https://hub.sd2e.org/user/sd2e/design/Kan/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000274'))])))]), SubjectReference(entity=NamedEntity(name='MG1655_empty_landing_pads', reference='https://hub.sd2e.org/user/sd2e/design/MG1655_empty_landing_pads/1'))]))), BlockReference(block=DesignBlock(label='conditions', definition=ProductBlock(block_list=[GenerateBlock(treatment=EntityTreatment(entity=NamedEntity(name='IPTG', reference='https://hub.sd2e.org/user/sd2e/design/IPTG/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])), attribute_name='concentration', values=[Value(value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=0.25, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=2.5, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=25, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=250, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))]), GenerateBlock(treatment=EntityTreatment(entity=NamedEntity(name='L-arabinose', reference='https://hub.sd2e.org/user/sd2e/design/Larabinose/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])), attribute_name='concentration', values=[Value(value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=5, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=50, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=500, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=5000, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=25000, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])])))])"

    def test_sum_block_serialization(self, condition_block, strain_block):
        b1 = SumBlock(block_list=[
            BlockReference(block=strain_block),
            BlockReference(block=condition_block)
        ])
        b_json = json.dumps(b1, cls=BlockDefinitionEncoder)
        assert b_json == '{"block_type": "sum_block", "block_list": [{"block_type": "block_reference", "reference": "strains"}, {"block_type": "block_reference", "reference": "conditions"}]}'
        b2 = json.loads(b_json, cls=DummyDefinitionDecoder)
        assert b1 == b2

    def test_tuple_block(self, condition_block, strain_block):
        b1 = ProductBlock(block_list=[
            BlockReference(block=strain_block),
            BlockReference(block=condition_block)
        ])
        b2 = ProductBlock(block_list=[
            BlockReference(block=strain_block),
            BlockReference(block=condition_block)
        ])
        assert b1 == b1
        assert b1 == b2
        assert b1 != {}

        assert repr(
            b1) == "ProductBlock(block_list=[BlockReference(block=DesignBlock(label='strains', definition=SumBlock(block_list=[ProductBlock(block_list=[SubjectReference(entity=NamedEntity(name='MG1655_NAND_Circuit', reference='https://hub.sd2e.org/user/sd2e/design/MG1655_NAND_Circuit/1')), TreatmentReference(treatment=EntityTreatment(entity=NamedEntity(name='Kan', reference='https://hub.sd2e.org/user/sd2e/design/Kan/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000274'))])))]), SubjectReference(entity=NamedEntity(name='MG1655_empty_landing_pads', reference='https://hub.sd2e.org/user/sd2e/design/MG1655_empty_landing_pads/1'))]))), BlockReference(block=DesignBlock(label='conditions', definition=ProductBlock(block_list=[GenerateBlock(treatment=EntityTreatment(entity=NamedEntity(name='IPTG', reference='https://hub.sd2e.org/user/sd2e/design/IPTG/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])), attribute_name='concentration', values=[Value(value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=0.25, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=2.5, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=25, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=250, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))]), GenerateBlock(treatment=EntityTreatment(entity=NamedEntity(name='L-arabinose', reference='https://hub.sd2e.org/user/sd2e/design/Larabinose/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])), attribute_name='concentration', values=[Value(value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=5, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=50, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=500, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=5000, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=25000, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])])))])"

    def test_tuple_block_serialization(self, condition_block, strain_block):
        b1 = ProductBlock(block_list=[
            BlockReference(block=strain_block),
            BlockReference(block=condition_block)
        ])
        b_json = json.dumps(b1, cls=BlockDefinitionEncoder)
        b2 = json.loads(b_json, cls=DummyDefinitionDecoder)
        assert b1 == b2


class TestReference:

    def test_block_reference(self, strain_block):
        r1 = BlockReference(block=strain_block)
        r2 = BlockReference(block=strain_block)
        assert r1 == r1
        assert r1 == r2
        assert r1 != {}

        assert repr(r1) == "BlockReference(block=DesignBlock(label='strains', definition=SumBlock(block_list=[ProductBlock(block_list=[SubjectReference(entity=NamedEntity(name='MG1655_NAND_Circuit', reference='https://hub.sd2e.org/user/sd2e/design/MG1655_NAND_Circuit/1')), TreatmentReference(treatment=EntityTreatment(entity=NamedEntity(name='Kan', reference='https://hub.sd2e.org/user/sd2e/design/Kan/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000274'))])))]), SubjectReference(entity=NamedEntity(name='MG1655_empty_landing_pads', reference='https://hub.sd2e.org/user/sd2e/design/MG1655_empty_landing_pads/1'))])))"

    def test_block_reference_serialization(self, strain_block):
        r1 = BlockReference(block=strain_block)
        r_json = json.dumps(r1, cls=BlockDefinitionEncoder)
        assert r_json == '{"block_type": "block_reference", "reference": "strains"}'
        r2 = json.loads(r_json, cls=DummyDefinitionDecoder)
        assert r1 == r2

    def test_treatment_reference(self, temperature):
        r1 = TreatmentReference(treatment=temperature)
        r2 = TreatmentReference(treatment=temperature)
        assert r1 == r1
        assert r1 == r2
        assert r1 != {}

        assert repr(r1) == "TreatmentReference(treatment=AttributeTreatment(attribute=BoundAttribute(name='temperature', value=Value(value=37.0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000027')))))"

    def test_treatment_reference_serialization(self, temperature):
        r1 = TreatmentReference(treatment=temperature)
        r_json = json.dumps(r1, cls=BlockDefinitionEncoder)
        assert r_json == '{"block_type": "treatment_reference", "reference": "temperature"}'
        r2 = json.loads(r_json, cls=DummyDefinitionDecoder)
        assert r1 == r2

    def test_treatment_attribute_reference(self, iptg):
        r1 = TreatmentReference(treatment=iptg)
        r2 = TreatmentReference(treatment=iptg)
        assert r1 == r1
        assert r1 == r2
        assert r1 != {}

        assert repr(
            r1) == "TreatmentReference(treatment=EntityTreatment(entity=NamedEntity(name='IPTG', reference='https://hub.sd2e.org/user/sd2e/design/IPTG/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])))"

    def test_treatment_attribute_reference_serialization(self, iptg):
        r1 = TreatmentReference(treatment=iptg)
        r_json = json.dumps(r1, cls=BlockDefinitionEncoder)
        r2 = json.loads(r_json, cls=DummyDefinitionDecoder)
        assert r1 == r2

    def test_treatment_attribute_value_reference(self, iptg):
        r1 = TreatmentReference.create_from(
            treatment=iptg,
            value=Value(
                value=0,
                unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000064')))
        r2 = TreatmentReference.create_from(
            treatment=iptg,
            value=Value(
                value=0,
                unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000064')))
        assert r1 == r1
        assert r1 == r2
        assert r1 != {}

        assert repr(
            r1) == "TreatmentValueReference(treatment=EntityTreatment(entity=NamedEntity(name='IPTG', reference='https://hub.sd2e.org/user/sd2e/design/IPTG/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])), value=Value(value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))"

    def test_treatment_attribute_value_reference_serialization(self, iptg):
        r1 = TreatmentReference.create_from(
            treatment=iptg,
            value=Value(
                value=0,
                unit=Unit(
                    reference='http://purl.obolibrary.org/obo/UO_0000064')))
        r_json = json.dumps(r1, cls=BlockDefinitionEncoder)
        r2 = json.loads(r_json, cls=DummyDefinitionDecoder)
        assert r1 == r2

    def test_subject_reference(self, kan):
        r1 = TreatmentReference(treatment=kan)
        r2 = TreatmentReference(treatment=kan)
        assert r1 == r1
        assert r1 == r2
        assert r1 != {}

        assert repr(
            r1) == "TreatmentReference(treatment=EntityTreatment(entity=NamedEntity(name='Kan', reference='https://hub.sd2e.org/user/sd2e/design/Kan/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000274'))])))"

    def test_subject_reference_serialization(self, kan):
        r1 = TreatmentReference(treatment=kan)
        r_json = json.dumps(r1, cls=BlockDefinitionEncoder)
        r2 = json.loads(r_json, cls=DummyDefinitionDecoder)
        assert r1 == r2


class TestDesignBlock:
    def test_design_block(self, kan):
        b1 = DesignBlock(
            label="test", definition=TreatmentReference(treatment=kan))
        b2 = DesignBlock(
            label="test", definition=TreatmentReference(treatment=kan))
        assert b1 == b1
        assert b1 == b2
        assert b1 != {}

        assert repr(
            b1) == "DesignBlock(label='test', definition=TreatmentReference(treatment=EntityTreatment(entity=NamedEntity(name='Kan', reference='https://hub.sd2e.org/user/sd2e/design/Kan/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000274'))]))))"

    def test_design_block_serialization(self, kan):
        b1 = DesignBlock(
            label="test", definition=TreatmentReference(treatment=kan))
        b_json = json.dumps(b1, cls=DesignBlockEncoder)
        assert b_json == '{"object_type": "design_block", "label": "test", "definition": {"block_type": "treatment_reference", "reference": "Kan"}}'
        b2 = json.loads(b_json, cls=DummyDesignDecoder)
        assert b1 == b2
