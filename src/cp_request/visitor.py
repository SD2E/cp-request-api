import abc

from cp_request import (
    Attribute,
    Control,
    ExperimentalRequest,
    Measurement,
    NamedEntity,
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
    TreatmentValueReference,
    TupleBlock
)


class RequestVisitor(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        pass

    def visit_design_block(self, block: DesignBlock):
        return

    def visit_product_block(self, block: ProductBlock):
        return

    def visit_tuple_block(self, block: TupleBlock):
        return

    def visit_block_reference(self, reference: BlockReference):
        return

    def visit_sum_block(self, block: SumBlock):
        return

    def visit_subject_reference(self, reference: SubjectReference):
        return

    def visit_treatment_reference(self, reference: TreatmentReference):
        return

    def visit_treatment_value_reference(self,
                                        reference: TreatmentValueReference):
        return

    def visit_replicate_block(self, block: ReplicateBlock):
        return

    def visit_generate_block(self, block: GenerateBlock):
        return

    def visit_attribute(self, attribute: Attribute):
        return

    def visit_version(self, version: Version):
        return

    def visit_treatment(self, treatment: Treatment):
        return

    def visit_sample(self, sample: Sample):
        return

    def visit_control(self, control: Control):
        return

    def visit_measurement(self, measurement: Measurement):
        return

    def visit_unit(self, unit: Unit):
        return

    def visit_value(self, value: Value):
        return

    def visit_named_entity(self, entity: NamedEntity):
        return

    def visit_experiment(self, experiment: ExperimentalRequest):
        return
