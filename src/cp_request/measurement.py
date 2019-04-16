import json
from cp_request.design import (
    BlockReference, SubjectReference, TreatmentReference,
    BlockDefinitionEncoder, BlockDefinitionDecoder
)
from typing import List


class Sample:
    def __init__(self, *, subject: SubjectReference, treatments: List[TreatmentReference] = list()):
        self.__subject = subject
        self.__treatments = list(treatments)

    def __repr__(self):
        return "Sample(subject={}, treatments={})".format(
            repr(self.subject), repr(self.treatments))

    def __eq__(self, other):
        if not isinstance(other, Sample):
            return False
        return self.subject == other.subject and self.treatments == self.treatments

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
            rep['subject'] = BlockDefinitionEncoder().default(obj.subject)
            if obj.treatments:
                rep['treatments'] = [BlockDefinitionEncoder().default(ref)
                                     for ref in obj.treatments]
            return rep
        return super().default(obj)


class SampleDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if 'object_type' not in d:
            return d
        if d['object_type'] != 'sample':
            return d
        if 'subject' not in d:
            return d
        treatments = list()
        if 'treatments' in d:
            treatments = [
                BlockDefinitionDecoder().object_hook(treatment)
                for treatment in d['treatments']
            ]
        return Sample(
            subject=BlockDefinitionDecoder().object_hook(d['subject']),
            treatments=treatments
        )


class Control:
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
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if 'object_type' not in d:
            return d
        if d['object_type'] != 'control':
            return d
        if 'name' not in d:
            return d
        if 'sample' not in d:
            return d
        return Control(name=d['name'], sample=SampleDecoder().object_hook(d['sample']))


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
            repr(self.type), repr(self.block), repr(self.controls), repr(self.performers))

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
    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if 'object_type' not in d:
            return d
        if d['object_type'] != 'measurement':
            return d
        if 'type' not in d:
            return d
        if 'block' not in d:
            return d
        if 'performers' not in d:
            return d
        controls = list()
        if 'controls' in d:
            controls = [
                ControlDecoder().object_hook(control)
                for control in d['controls']
            ]
        return Measurement(
            type=d['type'],
            block=BlockDefinitionDecoder().object_hook(d['block']),
            controls=controls,
            performers=d['performers']
        )
