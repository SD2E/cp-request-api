from cp_request.design.block_definition import BlockDefinition


class BlockReference(BlockDefinition):
    """
    A {BlockDefinition} that is a reference to a design block.
    """

    def __init__(self, *, label: str):
        self.__block_label = label

    def __repr__(self):
        return "BlockReference(label={})".format(repr(self.__block_label))

    def __str__(self):
        return self.__block_label

    def __eq__(self, other):
        if not isinstance(other, BlockReference):
            return False
        return self.__block_label == other.__block_label

    def apply(self, visitor):
        visitor.visit_block_reference(self)

    @property
    def block_label(self):
        return self.__block_label
