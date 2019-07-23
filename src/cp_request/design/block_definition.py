import abc


class BlockDefinition:
    """
    An abstract super class for definitions of design blocks.

    Allows deserialization to check for instances of this class rather than
    each of the subclasses.
    """
    @abc.abstractmethod
    def __init__(self):
        pass
