import json
from cp_request.design import (
    BlockReference,
    DesignBlock,
    GenerateBlock,
    ProductBlock,
    ReplicateBlock,
    SubjectReference,
    SumBlock,
    TreatmentReference,
    TreatmentAttributeReference,
    TreatmentAttributeValueReference,
    TreatmentValueReference,
    TupleBlock
)
from cp_request.design.block_definition import BlockDefinition
from cp_request import (
    ValueEncoder, ValueDecoder
)


class BlockReferenceEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, BlockReference):
            rep = dict()
            rep['block_type'] = 'block_reference'
            rep['reference'] = obj.block_label
            return rep
        return super().default(obj)


class BlockReferenceDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if 'block_type' not in d:
            return d
        if d['block_type'] != 'block_reference':
            return d
        if 'reference' not in d:
            return d

        return BlockReference(label=d['reference'])


class DesignBlockEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, DesignBlock):
            rep = dict()
            rep['object_type'] = 'design_block'
            rep['label'] = obj.label
            rep['definition'] = BlockDefinitionEncoder().default(
                obj.definition)
            return rep
        return super().default(obj)


class DesignBlockDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if 'object_type' not in d:
            return d
        if d['object_type'] != 'design_block':
            return d
        if 'label' not in d:
            return d
        if 'definition' not in d:
            return d
        return DesignBlock(
            label=d['label'],
            definition=BlockDefinitionDecoder().object_hook(d['definition'])
        )


class GenerateBlockEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, GenerateBlock):
            rep = dict()
            rep['block_type'] = 'generate_block'
            rep['treatment'] = TreatmentReferenceEncoder().default(
                obj.treatment)
            rep['values'] = [
                ValueEncoder().default(value) for value in obj.values
            ]
            return rep
        return super().default(obj)


class GenerateBlockDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if 'block_type' not in d:
            return d
        if d['block_type'] != 'generate_block':
            return d
        return GenerateBlock(
            treatment=TreatmentReferenceDecoder(
            ).object_hook(d['treatment']),
            values=[
                ValueDecoder().object_hook(value) for value in d['values']
            ])


class ProductBlockEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, ProductBlock):
            rep = dict()
            rep['block_type'] = 'product_block'
            rep['block_list'] = [
                BlockDefinitionEncoder().default(block)
                for block in obj.block_list
            ]
            return rep
        return super().default(obj)


class ProductBlockDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if 'block_type' not in d:
            return d
        if d['block_type'] != 'product_block':
            return d
        if 'block_list' not in d:
            return d

        return ProductBlock(block_list=[
            BlockDefinitionDecoder().object_hook(block)
            for block in d['block_list']
        ])


class ReplicateBlockEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, ReplicateBlock):
            rep = dict()
            rep['block_type'] = 'replicate_block'
            rep['count'] = obj.count
            rep['block'] = BlockDefinitionEncoder().default(obj.block)
            return rep
        return super().default(obj)


class ReplicateBlockDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if 'block_type' not in d:
            return d
        if d['block_type'] != 'replicate_block':
            return d
        if 'count' not in d:
            return d
        if 'block' not in d:
            return d
        return ReplicateBlock(
            count=d['count'],
            block=BlockDefinitionDecoder().object_hook(d['block'])
        )


class SubjectReferenceEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, SubjectReference):
            rep = dict()
            rep['block_type'] = 'subject_reference'
            rep['reference'] = obj.entity_name
            return rep
        return super().default(obj)


class SubjectReferenceDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if 'block_type' not in d:
            return d
        if d['block_type'] != 'subject_reference':
            return d
        if 'reference' not in d:
            return d
        return SubjectReference(entity_name=d['reference'])


class SumBlockEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, SumBlock):
            rep = dict()
            rep['block_type'] = 'sum_block'
            rep['block_list'] = [
                BlockDefinitionEncoder().default(block)
                for block in obj.block_list
            ]
            return rep
        return super().default(obj)


class SumBlockDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if 'block_type' not in d:
            return d
        if d['block_type'] != 'sum_block':
            return d
        if 'block_list' not in d:
            return d
        return SumBlock(
            block_list=[
                BlockDefinitionDecoder().object_hook(block)
                for block in d['block_list']
            ])


class TreatmentReferenceEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, TreatmentReference):
            rep = dict()
            rep['block_type'] = 'treatment_reference'
            rep['treatment_name'] = obj.treatment_name
            if isinstance(obj, TreatmentAttributeReference):
                rep['block_type'] = 'attribute_treatment_reference'
                rep['attribute'] = obj.attribute
                if isinstance(obj, TreatmentAttributeValueReference):
                    rep['block_type'] = 'attribute_value_treatment_reference'
                    rep['value'] = ValueEncoder().default(obj.value)
            elif isinstance(obj, TreatmentValueReference):
                rep['block_type'] = 'value_treatment_reference'
                rep['value'] = ValueEncoder().default(obj.value)
            return rep
        return super().default(obj)


class TreatmentReferenceDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if isinstance(d, TreatmentReference):
            return d
        if 'block_type' not in d:
            return d
        if 'treatment_name' not in d:
            return d
        if d['block_type'] == 'attribute_treatment_reference':
            if 'attribute' not in d:
                return d
            return TreatmentAttributeReference(
                treatment_name=d['treatment_name'],
                attribute=d['attribute']
            )
        if d['block_type'] == 'attribute_value_treatment_reference':
            if 'attribute' not in d:
                return d
            if 'value' not in d:
                return d
            return TreatmentAttributeValueReference(
                treatment_name=d['treatment_name'],
                attribute=d['attribute'],
                value=ValueDecoder().object_hook(d['value'])
            )
        if d['block_type'] == 'value_treatment_reference':
            if 'value' not in d:
                return d
            return TreatmentValueReference(
                treatment_name=d['treatment_name'],
                value=ValueDecoder().object_hook(d['value'])
            )
        return TreatmentReference(treatment_name=d['treatment_name'])


class TupleBlockEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, TupleBlock):
            rep = dict()
            rep['block_type'] = 'tuple_block'
            rep['block_list'] = [
                BlockDefinitionEncoder().default(block)
                for block in obj.block_list
            ]
            return rep
        return super().default(obj)


class TupleBlockDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if 'block_type' not in d:
            return d
        if d['block_type'] != 'tuple_block':
            return d
        if 'block_list' not in d:
            return d

        return TupleBlock(block_list=[
            BlockDefinitionDecoder().object_hook(block)
            for block in d['block_list']
        ])


class BlockDefinitionEncoder(json.JSONEncoder):

    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, BlockReference):
            return BlockReferenceEncoder().default(obj)
        if isinstance(obj, GenerateBlock):
            return GenerateBlockEncoder().default(obj)
        if isinstance(obj, ProductBlock):
            return ProductBlockEncoder().default(obj)
        if isinstance(obj, ReplicateBlock):
            return ReplicateBlockEncoder().default(obj)
        if isinstance(obj, SubjectReference):
            return SubjectReferenceEncoder().default(obj)
        if isinstance(obj, SumBlock):
            return SumBlockEncoder().default(obj)
        if isinstance(obj, TreatmentReference):
            return TreatmentReferenceEncoder().default(obj)
        if isinstance(obj, TupleBlock):
            return TupleBlockEncoder().default(obj)
        return super().default(obj)


class BlockDefinitionDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if isinstance(d, BlockDefinition):
            return d
        if 'block_type' not in d:
            return d
        if d['block_type'] == 'block_reference':
            return BlockReferenceDecoder().object_hook(d)
        if d['block_type'] == 'generate_block':
            return GenerateBlockDecoder().object_hook(d)
        if d['block_type'] == 'product_block':
            return ProductBlockDecoder().object_hook(d)
        if d['block_type'] == 'replicate_block':
            return ReplicateBlockDecoder().object_hook(d)
        if d['block_type'] == 'subject_reference':
            return SubjectReferenceDecoder().object_hook(d)
        if d['block_type'] == 'sum_block':
            return SumBlockDecoder().object_hook(d)
        if d['block_type'] == 'tuple_block':
            return TupleBlockDecoder().object_hook(d)

        if 'treatment_name' in d:
            return TreatmentReferenceDecoder().object_hook(d)

        return d
