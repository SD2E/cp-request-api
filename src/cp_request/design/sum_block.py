from cp_request.design.block_definition import BlockDefinition
from typing import List


class SumBlock(BlockDefinition):
    def __init__(self, *, block_list: List[BlockDefinition]):
        self.__block_list = block_list

    def __repr__(self):
        return "SumBlock(block_list={})".format(repr(self.__block_list))

    def __str__(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, SumBlock):
            return False
        return self.__block_list == other.__block_list

    @property
    def block_list(self):
        return self.__block_list
