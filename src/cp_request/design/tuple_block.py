from cp_request.design.block_definition import BlockDefinition


class TupleBlock(BlockDefinition):
    def __init__(self, *, block_list):
        self.__block_list = block_list

    def __repr__(self):
        return "TupleBlock(block_list={})".format(self.__block_list)

    def __str__(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, TupleBlock):
            return False
        return self.__block_list == other.__block_list

    @property
    def block_list(self):
        return self.__block_list
