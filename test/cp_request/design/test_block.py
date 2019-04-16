import pytest

import json
from cp_request import (
    Unit,
    Value
)
from cp_request.design import (
    GenerateBlock, ProductBlock, ReplicateBlock, SumBlock, TupleBlock,
    BlockReference, SubjectReference, TreatmentReference,
    BlockDefinitionEncoder, BlockDefinitionDecoder,
    DesignBlock, DesignBlockEncoder, DesignBlockDecoder
)


class TestDefinitionBlock:

    def test_generate_block(self):
        b1 = GenerateBlock(
            treatment=TreatmentReference.create_from(
                treatment_name='IPTG',
                attribute='concentration'),
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
            treatment=TreatmentReference.create_from(
                treatment_name='IPTG',
                attribute='concentration'),
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
            b1) == "GenerateBlock(treatment=TreatmentAttributeReference(treatment_name='IPTG', attribute='concentration'), values=[Value(value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=0.25, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=2.5, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=25, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=250, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])"

    def test_generate_block_serialization(self):
        b1 = GenerateBlock(
            treatment=TreatmentReference.create_from(
                treatment_name='IPTG',
                attribute='concentration'),
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
        b2 = json.loads(b_json, cls=BlockDefinitionDecoder)
        assert b1 == b2

    def test_product_block(self):
        b1 = ProductBlock(block_list=[
            TreatmentReference.create_from(treatment_name='temperature'),
            TreatmentReference.create_from(treatment_name='timepoint')
        ])
        b2 = ProductBlock(block_list=[
            TreatmentReference.create_from(treatment_name='temperature'),
            TreatmentReference.create_from(treatment_name='timepoint')
        ])
        assert b1 == b1
        assert b1 == b2
        assert b1 != {}

        assert repr(
            b1) == "ProductBlock(block_list=[TreatmentReference(treatment_name='temperature'), TreatmentReference(treatment_name='timepoint')])"

    def test_product_block_serialization(self):
        b1 = ProductBlock(block_list=[
            TreatmentReference.create_from(treatment_name='temperature'),
            TreatmentReference.create_from(treatment_name='timepoint')
        ])

        b_json = json.dumps(b1, cls=BlockDefinitionEncoder)
        assert b_json == '{"block_type": "product_block", "block_list": [{"block_type": "treatment_reference", "treatment_name": "temperature"}, {"block_type": "treatment_reference", "treatment_name": "timepoint"}]}'
        b2 = json.loads(b_json, cls=BlockDefinitionDecoder)
        assert b1 == b2

    def test_replicate_block(self):
        b1 = ReplicateBlock(count=4, block=BlockReference(label='conditions'))
        b2 = ReplicateBlock(count=4, block=BlockReference(label='conditions'))

        assert b1 == b1
        assert b1 == b2
        assert b1 != {}

        assert repr(
            b1) == "ReplicateBlock(count=4, block=BlockReference(label='conditions'))"

    def test_replicate_block_serialization(self):
        b1 = ReplicateBlock(count=4, block=BlockReference(label='conditions'))
        b_json = json.dumps(b1, cls=BlockDefinitionEncoder)
        assert b_json == '{"block_type": "replicate_block", "count": 4, "block": {"block_type": "block_reference", "reference": "conditions"}}'
        b2 = json.loads(b_json, cls=BlockDefinitionDecoder)
        assert b1 == b2

    def test_sum_block(self):
        b1 = SumBlock(block_list=[
            BlockReference(label='strains'), BlockReference(label='conditions')
        ])
        b2 = SumBlock(block_list=[
            BlockReference(label='strains'), BlockReference(label='conditions')
        ])
        assert b1 == b1
        assert b1 == b2
        assert b1 != {}

        assert repr(
            b1) == "SumBlock(block_list=[BlockReference(label='strains'), BlockReference(label='conditions')])"

    def test_sum_block_serialization(self):
        b1 = SumBlock(block_list=[
            BlockReference(label='strains'), BlockReference(label='conditions')
        ])
        b_json = json.dumps(b1, cls=BlockDefinitionEncoder)
        assert b_json == '{"block_type": "sum_block", "block_list": [{"block_type": "block_reference", "reference": "strains"}, {"block_type": "block_reference", "reference": "conditions"}]}'
        b2 = json.loads(b_json, cls=BlockDefinitionDecoder)
        assert b1 == b2

    def test_tuple_block(self):
        b1 = TupleBlock(block_list=[
            BlockReference(label='strains'), BlockReference(label='conditions')
        ])
        b2 = TupleBlock(block_list=[
            BlockReference(label='strains'), BlockReference(label='conditions')
        ])
        assert b1 == b1
        assert b1 == b2
        assert b1 != {}

        assert repr(
            b1) == "TupleBlock(block_list=[BlockReference(label='strains'), BlockReference(label='conditions')])"

    def test_tuple_block_serialization(self):
        b1 = TupleBlock(block_list=[
            BlockReference(label='strains'), BlockReference(label='conditions')
        ])
        b_json = json.dumps(b1, cls=BlockDefinitionEncoder)
        assert b_json == '{"block_type": "tuple_block", "block_list": [{"block_type": "block_reference", "reference": "strains"}, {"block_type": "block_reference", "reference": "conditions"}]}'
        b2 = json.loads(b_json, cls=BlockDefinitionDecoder)
        assert b1 == b2


class TestReference:

    def test_block_reference(self):
        r1 = BlockReference(label='strains')
        r2 = BlockReference(label='strains')
        assert r1 == r1
        assert r1 == r2
        assert r1 != {}

        assert repr(r1) == "BlockReference(label='strains')"

    def test_block_reference_serialization(self):
        r1 = BlockReference(label='strains')
        r_json = json.dumps(r1, cls=BlockDefinitionEncoder)
        assert r_json == '{"block_type": "block_reference", "reference": "strains"}'
        r2 = json.loads(r_json, cls=BlockDefinitionDecoder)
        assert r1 == r2

    def test_treatment_reference(self):
        r1 = TreatmentReference.create_from(treatment_name='temperature')
        r2 = TreatmentReference.create_from(treatment_name='temperature')
        assert r1 == r1
        assert r1 == r2
        assert r1 != {}

        assert repr(r1) == "TreatmentReference(treatment_name='temperature')"

    def test_treatment_reference_serialization(self):
        r1 = TreatmentReference.create_from(treatment_name='temperature')
        r_json = json.dumps(r1, cls=BlockDefinitionEncoder)
        assert r_json == '{"block_type": "treatment_reference", "treatment_name": "temperature"}'
        r2 = json.loads(r_json, cls=BlockDefinitionDecoder)
        assert r1 == r2

    def test_treatment_attribute_reference(self):
        r1 = TreatmentReference.create_from(
            treatment_name='IPTG', attribute='concentration')
        r2 = TreatmentReference.create_from(
            treatment_name='IPTG', attribute='concentration')
        assert r1 == r1
        assert r1 == r2
        assert r1 != {}

        assert repr(
            r1) == "TreatmentAttributeReference(treatment_name='IPTG', attribute='concentration')"

    def test_treatment_attribute_reference_serialization(self):
        r1 = TreatmentReference.create_from(
            treatment_name='IPTG', attribute='concentration')
        r_json = json.dumps(r1, cls=BlockDefinitionEncoder)
        assert r_json == '{"block_type": "attribute_treatment_reference", "treatment_name": "IPTG", "attribute": "concentration"}'
        r2 = json.loads(r_json, cls=BlockDefinitionDecoder)
        assert r1 == r2

    def test_treatment_attribute_value_reference(self):
        r1 = TreatmentReference.create_from(
            treatment_name='IPTG',
            attribute='concentration',
            value=Value(
                value=0,
                unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))
        r2 = TreatmentReference.create_from(
            treatment_name='IPTG',
            attribute='concentration',
            value=Value(
                value=0,
                unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))
        assert r1 == r1
        assert r1 == r2
        assert r1 != {}

        assert repr(
            r1) == "TreatmentAttributeValueReference(treatment_name='IPTG', attribute='concentration', value=Value(value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))"

    def test_treatment_attribute_value_reference_serialization(self):
        r1 = TreatmentReference.create_from(
            treatment_name='IPTG',
            attribute='concentration',
            value=Value(
                value=0,
                unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))
        r_json = json.dumps(r1, cls=BlockDefinitionEncoder)
        r2 = json.loads(r_json, cls=BlockDefinitionDecoder)
        assert r1 == r2

    def test_subject_reference(self):
        r1 = SubjectReference(entity_name='Kan')
        r2 = SubjectReference(entity_name='Kan')
        assert r1 == r1
        assert r1 == r2
        assert r1 != {}

        assert repr(r1) == "SubjectReference(entity='Kan')"

    def test_subject_reference_serialization(self):
        r1 = SubjectReference(entity_name='Kan')
        r_json = json.dumps(r1, cls=BlockDefinitionEncoder)
        assert r_json == '{"block_type": "subject_reference", "reference": "Kan"}'
        r2 = json.loads(r_json, cls=BlockDefinitionDecoder)
        assert r1 == r2


class TestDesignBlock:
    def test_design_block(self):
        b1 = DesignBlock(
            label="test", definition=SubjectReference(entity_name="Kan"))
        b2 = DesignBlock(
            label="test", definition=SubjectReference(entity_name="Kan"))
        assert b1 == b1
        assert b1 == b2
        assert b1 != {}

        assert repr(
            b1) == "DesignBlock(label='test', definition=SubjectReference(entity='Kan'))"

    def test_design_block_serialization(self):
        b1 = DesignBlock(
            label="test", definition=SubjectReference(entity_name="Kan"))
        b_json = json.dumps(b1, cls=DesignBlockEncoder)
        assert b_json == '{"object_type": "design_block", "label": "test", "definition": {"block_type": "subject_reference", "reference": "Kan"}}'
        b2 = json.loads(b_json, cls=DesignBlockDecoder)
        assert b1 == b2
