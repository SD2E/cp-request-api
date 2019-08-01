from cp_request.design.block_definition import BlockDefinition
from transform.transformer import RequestTransformer


class ReplicateBlock(BlockDefinition):
    """
    Represents a design block definition consisting of a sum of a given number
    of replicates of a block.
    """

    def __init__(self, *, count: int, block: BlockDefinition):
        self.__count = count
        self.__block = block

    def __repr__(self):
        return "ReplicateBlock(count={}, block={})".format(
            self.__count, repr(self.__block))

    # TODO: implement str method
    def __str__(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, ReplicateBlock):
            return False
        return self.count == other.count and self.block == other.block

    def apply(self, visitor):
        visitor.visit_replicate_block(self)

    def transform(self, transformer: RequestTransformer):
        return transformer.transform_replicate_block(self)

    @property
    def count(self):
        return self.__count

    @property
    def block(self):
        return self.__block
