from cp_request.design.design_block import DesignBlock
from cp_request.design.block_definition import BlockDefinition


class BlockReference(BlockDefinition):
    """
    A {BlockDefinition} that is a reference to a design block.
    """

    def __init__(self, *, block: DesignBlock):
        self.__block = block

    def __repr__(self):
        return "BlockReference(block={})".format(repr(self.__block))

    def __str__(self):
        return self.__block

    def __eq__(self, other):
        if not isinstance(other, BlockReference):
            return False
        return self.__block == other.__block

    def apply(self, visitor):
        visitor.visit_block_reference(self)

    @property
    def block_label(self):
        return self.__block.label
