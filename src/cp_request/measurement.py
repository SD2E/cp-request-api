import json
from cp_request import NamedEntity, Treatment
from cp_request.design import (
    BlockReference,
    BlockDefinitionEncoder,
    BlockDefinitionDecoder
)
from typing import List


# TODO: ensure that entity and treatments are bound
class Sample:
    """
    An entity with treatments.
    """

    def __init__(self, *,
                 subject: NamedEntity,
                 treatments: List[Treatment] = list()):
        self.__subject = subject
        self.__treatments = list(treatments)

    def __repr__(self):
        return "Sample(subject={}, treatments={})".format(
            repr(self.subject), repr(self.treatments))

    def __eq__(self, other):
        if not isinstance(other, Sample):
            return False
        return (self.subject == other.subject
                and self.treatments == self.treatments)

    def apply(self, visitor):
        visitor.visit_sample(self)

    @property
    def subject(self):
        return self.__subject

    @property
    def treatments(self):
        return self.__treatments


class SampleEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, Sample):
            rep = dict()
            rep['object_type'] = 'sample'
            rep['subject'] = obj.subject.name
            if obj.treatments:
                rep['treatments'] = [BlockDefinitionEncoder().default(ref)
                                     for ref in obj.treatments]
            return rep
        return super().default(obj)


class SampleDecoder(json.JSONDecoder):
    def __init__(self, symbol_table):
        self.__symbol_table = symbol_table
        super().__init__(object_hook=self.convert)

    def convert(self, dictionary):
        if 'object_type' not in dictionary:
            return dictionary
        if dictionary['object_type'] != 'sample':
            return dictionary
        if 'subject' not in dictionary:
            return dictionary
        subject = self.__symbol_table[dictionary['subject']]
        treatments = list()
        if 'treatments' in dictionary:
            treatments = [
                BlockDefinitionDecoder(
                    self.__symbol_table).object_hook(treatment)
                for treatment in dictionary['treatments']
            ]
        return Sample(
            subject=subject,
            treatments=treatments
        )


class Control:
    """
    A {Sample} that represents a measurement control.
    """

    def __init__(self, *, name: str, sample: Sample):
        self.__name = name
        self.__sample = sample

    def __repr__(self):
        return "Control(name={}, sample={})".format(
            repr(self.name), repr(self.sample)
        )

    def __eq__(self, other):
        if not isinstance(other, Control):
            return False
        return self.name == other.name and self.sample == other.sample

    def apply(self, visitor):
        visitor.visit_control(self)

    @property
    def name(self):
        return self.__name

    @property
    def sample(self):
        return self.__sample


class ControlEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, Control):
            rep = dict()
            rep['object_type'] = 'control'
            rep['name'] = obj.name
            rep['sample'] = SampleEncoder().default(obj.sample)
            return rep
        return super().default(obj)


class ControlDecoder(json.JSONDecoder):
    def __init__(self, symbol_table):
        self.__symbol_table = symbol_table
        super().__init__(object_hook=self.convert)

    def convert(self, dictionary):
        if 'object_type' not in dictionary:
            return dictionary
        if dictionary['object_type'] != 'control':
            return dictionary
        if 'name' not in dictionary:
            return dictionary
        if 'sample' not in dictionary:
            return dictionary
        return Control(
            name=dictionary['name'],
            sample=SampleDecoder(
                self.__symbol_table).object_hook(dictionary['sample']))


class Measurement:
    def __init__(self, *,
                 type: str,
                 block: BlockReference,
                 controls: List[Control] = list(),
                 performers: List[str]):
        self.__type = type
        self.__block = block
        self.__controls = list(controls)
        self.__performers = performers

    def __eq__(self, other):
        if not isinstance(other, Measurement):
            return False
        return (self.type == other.type
                and self.block == other.block
                and self.controls == other.controls
                and self.performers == other.performers)

    def __repr__(self):
        return "Measurement(type={}, block={}, controls={}, performers={})".format(
            repr(self.type),
            repr(self.block),
            repr(self.controls),
            repr(self.performers))

    def apply(self, visitor):
        visitor.visit_measurement(self)

    @property
    def type(self):
        return self.__type

    @property
    def block(self):
        return self.__block

    @property
    def controls(self):
        return self.__controls

    @property
    def performers(self):
        return self.__performers


class MeasurementEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, Measurement):
            rep = dict()
            rep['object_type'] = 'measurement'
            rep['type'] = obj.type
            rep['block'] = BlockDefinitionEncoder().default(obj.block)
            if obj.controls:
                rep['controls'] = [
                    ControlEncoder().default(control)
                    for control in obj.controls
                ]
            rep['performers'] = obj.performers
            return rep
        return super().default(obj)


class MeasurementDecoder(json.JSONDecoder):
    def __init__(self, symbol_table):
        self.__symbol_table = symbol_table
        super().__init__(object_hook=self.convert)

    def convert(self, dictionary):
        if 'object_type' not in dictionary:
            return dictionary
        if dictionary['object_type'] != 'measurement':
            return dictionary
        if 'type' not in dictionary:
            return dictionary
        if 'block' not in dictionary:
            return dictionary
        if 'performers' not in dictionary:
            return dictionary
        controls = list()
        if 'controls' in dictionary:
            controls = [
                ControlDecoder(self.__symbol_table).object_hook(control)
                for control in dictionary['controls']
            ]
        return Measurement(
            type=dictionary['type'],
            block=BlockDefinitionDecoder(
                self.__symbol_table).object_hook(dictionary['block']),
            controls=controls,
            performers=dictionary['performers']
        )
