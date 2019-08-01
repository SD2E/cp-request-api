from cp_request import (
    Attribute,
    Control,
    ExperimentalRequest,
    Measurement,
    NamedEntity,
    RequestVisitor,
    Sample,
    Treatment,
    Unit,
    Value,
    Version
)

from cp_request.design import (
    DesignBlock,
    BlockReference,
    GenerateBlock,
    ProductBlock,
    ReplicateBlock,
    SumBlock,
    SubjectReference,
    TreatmentReference,
    TreatmentValueReference
)

from transform import RequestTransformer


class NormalizeTransformer(RequestTransformer):
    """
    Visitor that creates a normalized request object so that all design blocks
    are fully enumerated.
    """

    def __init__(self):
        pass

    def transform_design_block(self, block: DesignBlock):
        # normalize block.definition and create new design block
        return

    def transform_product_block(self, block: ProductBlock):
        return

    def transform_block_reference(self, reference: BlockReference):
        return

    def transform_sum_block(self, block: SumBlock):
        return

    def transform_subject_reference(self, reference: SubjectReference):
        return

    def transform_treatment_reference(self, reference: TreatmentReference):
        return

    def transform_treatment_value_reference(self,
                                            reference: TreatmentValueReference):
        return

    def transform_replicate_block(self, block: ReplicateBlock):
        return

    def transform_generate_block(self, block: GenerateBlock):
        """
        Creates the equivalent SumBlock, and adds it to the normalized request.
        """
        treatment_list = list()
        # using block.treatment
        # iterate over block.values and instantiate attribute
        sum_block = SumBlock(block_list=treatment_list)

    def transform_attribute(self, attribute: Attribute):
        return

    def transform_version(self, version: Version):
        return

    def transform_treatment(self, treatment: Treatment):
        return

    def transform_sample(self, sample: Sample):
        return

    def transform_control(self, control: Control):
        return

    def transform_measurement(self, measurement: Measurement):
        return

    def transform_unit(self, unit: Unit):
        return

    def transform_value(self, value: Value):
        return

    def transform_named_entity(self, entity: NamedEntity):
        return

    def transform_experiment(self, experiment: ExperimentalRequest):
        return
