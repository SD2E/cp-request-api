from cp_request.design.block_definition import BlockDefinition


class DesignBlock:
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

    @property
    def label(self):
        return self.__label

    @property
    def definition(self):
        return self.__definition
