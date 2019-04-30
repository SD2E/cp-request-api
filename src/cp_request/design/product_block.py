from cp_request.design.block_definition import BlockDefinition
from typing import List


class ProductBlock(BlockDefinition):
    """
    Represents a design block formed by taking the product of a sequence of
    blocks.
    """

    def __init__(self, *, block_list: List[BlockDefinition]):
        self.__block_list = block_list

    def __repr__(self):
        return "ProductBlock(block_list={})".format(repr(self.__block_list))

    # TODO: define str method
    def __str__(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, ProductBlock):
            return False
        return self.__block_list == other.__block_list

    def apply(self, visitor):
        visitor.visit_product_block(self)

    @property
    def block_list(self):
        return self.__block_list
