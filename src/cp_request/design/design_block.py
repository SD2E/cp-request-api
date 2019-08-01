from cp_request.design.block_definition import BlockDefinition
from transform.transformer import RequestTransformer


class DesignBlock:
    """
    Represents a labeled {BlockDefinition}.

    Allows the definition of an experimental design that can be composed
    with other definitions to form a large design.
    """

    def __init__(self, *, label: str, definition: BlockDefinition):
        self.__label = label
        self.__definition = definition

    def __repr__(self):
        return "DesignBlock(label={}, definition={})".format(
            repr(self.__label), repr(self.__definition))

    def __str__(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, DesignBlock):
            return False
        return (self.__label == other.__label and
                self.__definition == self.__definition)

    def apply(self, visitor):
        visitor.visit_design_block(self)

    def transform(self, transformer: RequestTransformer):
        return transformer.transform_design_block(self)

    @property
    def label(self):
        return self.__label

    @property
    def definition(self):
        return self.__definition
