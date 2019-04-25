
import json
from cp_request.design import (
    DesignBlock, DesignBlockEncoder, DesignBlockDecoder
)
from cp_request import (
    Measurement, MeasurementEncoder, MeasurementDecoder,
    NamedEntity, NamedEntityEncoder, NamedEntityDecoder,
    Treatment, TreatmentEncoder, TreatmentDecoder,
    Version, VersionEncoder, VersionDecoder
)
from typing import List


class ExperimentalRequest:
    """
    Defines a structured experimental request
    """

    def __init__(self, *, cp_name: str,
                 reference_name: str,
                 reference_url: str,
                 version: Version,
                 derived_from=None,
                 subjects: List[NamedEntity] = list(),
                 treatments: List[Treatment] = list(),
                 designs: List[DesignBlock] = list(),
                 measurements: List[Measurement] = list()):
        self.challenge_problem = cp_name
        self.experiment_reference = reference_name
        self.experiment_reference_url = reference_url
        self.experiment_version = version
        self.derived_from = derived_from
        self.subjects = list(subjects)
        self.treatments = list(treatments)
        self.designs = list(designs)
        self.measurements = list(measurements)

    def __eq__(self, other):
        if not isinstance(other, ExperimentalRequest):
            return False
        return (
            self.challenge_problem == other.challenge_problem
            and self.experiment_reference == other.experiment_reference
            and self.experiment_reference_url == other.experiment_reference_url
            and self.experiment_version == other.experiment_version
            and self.derived_from == other.derived_from
            and self.subjects == other.subjects
            and self.treatments == other.treatments
            and self.designs == other.designs
            and self.measurements == other.measurements
        )

    def __repr__(self):
        return (
            "ExperimentalRequest(cp_name={}, "
            "reference_name={}, "
            "reference_url={}, "
            "version={}, "
            "derived_from={}, "
            "subjects={}, "
            "treatments={}, "
            "designs={}, "
            "measurements={})"
        ).format(
            repr(self.challenge_problem),
            repr(self.experiment_reference),
            repr(self.experiment_reference_url),
            repr(self.experiment_version),
            repr(self.derived_from),
            repr(self.subjects),
            repr(self.treatments),
            repr(self.designs),
            repr(self.measurements)
        )

    def apply(self, visitor):
        visitor.visit_experiment(self)


class ExperimentEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, ExperimentalRequest):
            rep = dict()
            rep['object_type'] = 'experimental_request'
            rep['challenge_problem'] = obj.challenge_problem
            rep['experiment_reference'] = obj.experiment_reference
            rep['experiment_reference_url'] = obj.experiment_reference_url
            rep['experiment_version'] = VersionEncoder().default(
                obj.experiment_version)
            if obj.derived_from:
                rep['derived_from'] = obj.derived_from
            rep['subjects'] = [NamedEntityEncoder().default(entity)
                               for entity in obj.subjects]
            rep['treatments'] = [TreatmentEncoder().default(treatment)
                                 for treatment in obj.treatments]
            rep['designs'] = [DesignBlockEncoder().default(design)
                              for design in obj.designs]
            rep['measurements'] = [MeasurementEncoder().default(measurement)
                                   for measurement in obj.measurements]
            return rep
        return super().default(obj)


class ExperimentDecoder(json.JSONDecoder):

    def __init__(self):
        super().__init__(object_hook=self.convert)

    def convert(self, d):
        if 'object_type' not in d:
            return d
        if d['object_type'] != 'experimental_request':
            return d
        if 'challenge_problem' not in d:
            return d
        if 'experiment_reference' not in d:
            return d
        if 'experiment_reference_url' not in d:
            return d
        if 'experiment_version' not in d:
            return d
        if 'subjects' not in d:
            return d
        if 'treatments' not in d:
            return d
        if 'designs' not in d:
            return d
        if 'measurements' not in d:
            return d
        derived_from = None
        if 'derived_from' in d:
            derived_from = d['derived_from']

        symbol_table = dict()
        subjects = [NamedEntityDecoder().object_hook(entity)
                    for entity in d['subjects']]
        for subject in subjects:
            symbol_table[subject.name] = subject
        treatments = [TreatmentDecoder().object_hook(treatment)
                      for treatment in d['treatments']]
        for treatment in treatments:
            symbol_table[treatment.name] = treatment

        return ExperimentalRequest(
            cp_name=d['challenge_problem'],
            reference_name=d['experiment_reference'],
            reference_url=d['experiment_reference_url'],
            version=VersionDecoder().object_hook(d['experiment_version']),
            derived_from=derived_from,
            subjects=subjects,
            treatments=treatments,
            designs=[
                DesignBlockDecoder(symbol_table).object_hook(design)
                for design in d['designs']
            ],
            measurements=[
                MeasurementDecoder(symbol_table).object_hook(measurement)
                for measurement in d['measurements']
            ]
        )
