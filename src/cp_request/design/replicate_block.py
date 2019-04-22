from cp_request.design.block_definition import BlockDefinition


class ReplicateBlock(BlockDefinition):
    def __init__(self, *, count: int, block: BlockDefinition):
        self.__count = count
        self.__block = block

    def __repr__(self):
        return "ReplicateBlock(count={}, block={})".format(
            self.__count, repr(self.__block))

    def __str__(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, ReplicateBlock):
            return False
        return self.count == other.count and self.block == other.block

    @property
    def count(self):
        return self.__count

    @property
    def block(self):
        return self.__block
