import json
import pytest
from cp_request import (
    Attribute,
    Control,
    ExperimentalRequest, ExperimentEncoder, ExperimentDecoder,
    Measurement,
    NamedEntity,
    Sample,
    Treatment,
    Unit,
    Value,
    Version
)
from cp_request.design import (
    BlockReference,
    DesignBlock,
    GenerateBlock,
    ProductBlock,
    ReplicateBlock,
    SubjectReference,
    SumBlock,
    TreatmentReference,
    TupleBlock
)


class TestExperimentalRequest:

    def test_request(self):
        temperature_unit = Unit(
            reference='http://purl.obolibrary.org/obo/UO_0000027')
        hour_unit = Unit(reference='http://purl.obolibrary.org/obo/UO_0000032')
        micromolar_unit = Unit(
            reference='http://purl.obolibrary.org/obo/UO_0000064')
        microgram_per_milliliter_unit = Unit(
            reference='http://purl.obolibrary.org/obo/UO_0000274')
        nand_circuit = NamedEntity(
            name="MG1655_NAND_Circuit",
            reference="https://hub.sd2e.org/user/sd2e/design/MG1655_NAND_Circuit/1"
        )
        empty_landing_pads = NamedEntity(
            name="MG1655_empty_landing_pads",
            reference="https://hub.sd2e.org/user/sd2e/design/MG1655_empty_landing_pads/1"
        )
        temperature = Treatment.create_from(
            attribute=Attribute.create_from(
                name='temperature',
                value=Value(
                    value=37.0,
                    unit=temperature_unit
                )))
        timepoint = Treatment.create_from(
            attribute=Attribute.create_from(
                name='timepoint',
                unit=hour_unit)
        )
        media = Treatment.create_from(
            entity=NamedEntity(name="M9 Glucose CAA",
                               reference="https://hub.sd2e.org/user/sd2e/design/M9_glucose_CAA/1"))
        iptg = Treatment.create_from(
            entity=NamedEntity(
                name='IPTG',
                reference='https://hub.sd2e.org/user/sd2e/design/IPTG/1',
                attributes=[
                    Attribute.create_from(
                        name='concentration', unit=micromolar_unit)
                ])
        )
        l_arabinose = Treatment.create_from(
            entity=NamedEntity(
                name='L-arabinose',
                reference='https://hub.sd2e.org/user/sd2e/design/Larabinose/1',
                attributes=[
                    Attribute.create_from(
                        name='concentration', unit=micromolar_unit)
                ])
        )
        kan = Treatment.create_from(
            entity=NamedEntity(
                name='Kan',
                reference='https://hub.sd2e.org/user/sd2e/design/Kan/1',
                attributes=[
                    Attribute.create_from(
                        name='concentration', unit=microgram_per_milliliter_unit)
                ])
        )
        r1 = ExperimentalRequest(
            cp_name='NOVEL_CHASSIS',
            reference_name='NovelChassis-NAND-Ecoli-Titration',
            reference_url='https://docs.google.com/document/d/1oMC5VM3XcFn6zscxLKLUe4U-TXbBsz8H6OQwHal1h4g',
            version=Version(major=1, minor=0, patch=0),
            subjects=[nand_circuit, empty_landing_pads],
            treatments=[
                temperature,
                media,
                iptg,
                l_arabinose,
                kan
            ],
            designs=[
                DesignBlock(
                    label='strains',
                    definition=SumBlock(block_list=[
                        TupleBlock(block_list=[
                            SubjectReference(entity=nand_circuit),
                            TreatmentReference.create_from(treatment=kan)
                        ]),
                        SubjectReference(entity=empty_landing_pads)
                    ])
                ),
                DesignBlock(
                    label='temperature-media',
                    definition=TupleBlock(
                        block_list=[
                            TreatmentReference.create_from(
                                treatment=temperature),
                            TreatmentReference.create_from(treatment=media)
                        ])
                ),
                DesignBlock(
                    label='conditions',
                    definition=ProductBlock(block_list=[
                        GenerateBlock(
                            treatment=iptg,
                            values=[
                                Value(
                                    value=0,
                                    unit=micromolar_unit),
                                Value(
                                    value=0.25,
                                    unit=micromolar_unit),
                                Value(
                                    value=2.5,
                                    unit=micromolar_unit),
                                Value(
                                    value=25,
                                    unit=micromolar_unit),
                                Value(
                                    value=250,
                                    unit=micromolar_unit)
                            ]),
                        GenerateBlock(
                            treatment=l_arabinose,
                            values=[
                                Value(
                                    value=0,
                                    unit=micromolar_unit),
                                Value(
                                    value=5,
                                    unit=micromolar_unit),
                                Value(
                                    value=50,
                                    unit=micromolar_unit),
                                Value(
                                    value=500,
                                    unit=micromolar_unit),
                                Value(
                                    value=5000,
                                    unit=micromolar_unit),
                                Value(
                                    value=25000,
                                    unit=micromolar_unit)
                            ]),
                    ])
                ),
                DesignBlock(
                    label='experiment',
                    definition=ProductBlock(block_list=[
                        ReplicateBlock(
                            count=4,
                            block=ProductBlock(block_list=[
                                BlockReference(label='strains'),
                                BlockReference(label='temperature-media'),
                                BlockReference(label='conditions')
                            ])
                        ),
                        GenerateBlock(
                            treatment=TreatmentReference.create_from(
                                treatment=timepoint
                            ),
                            values=[
                                Value(
                                    value=5,
                                    unit=hour_unit),
                                Value(
                                    value=6.5,
                                    unit=hour_unit),
                                Value(
                                    value=8,
                                    unit=hour_unit),
                                Value(
                                    value=18,
                                    unit=hour_unit)
                            ]
                        ),
                    ])
                )
            ],
            measurements=[
                Measurement(
                    type='FLOW',
                    block=BlockReference(label='experiment'),
                    controls=[
                        Control(
                            name='positive_gfp',
                            sample=Sample(
                                subject=SubjectReference(
                                    entity=nand_circuit),
                                treatments=[
                                    TreatmentReference.create_from(
                                        treatment=timepoint, value=Value(
                                            value=18, unit=hour_unit)),
                                    TreatmentReference.create_from(
                                        treatment=iptg, value=Value(
                                            value=0, unit=micromolar_unit))
                                ]
                            )
                        ),
                        Control(
                            name='negative_gfp',
                            sample=Sample(subject=SubjectReference(
                                entity=empty_landing_pads))
                        )
                    ],
                    performers=['Ginkgo']
                )
            ]
        )
        r2 = ExperimentalRequest(
            cp_name='NOVEL_CHASSIS',
            reference_name='NovelChassis-NAND-Ecoli-Titration',
            reference_url='https://docs.google.com/document/d/1oMC5VM3XcFn6zscxLKLUe4U-TXbBsz8H6OQwHal1h4g',
            version=Version(major=1, minor=0, patch=0),
            subjects=[
                NamedEntity(
                    name="MG1655_NAND_Circuit",
                    reference="https://hub.sd2e.org/user/sd2e/design/MG1655_NAND_Circuit/1"
                ),
                NamedEntity(
                    name="MG1655_empty_landing_pads",
                    reference="https://hub.sd2e.org/user/sd2e/design/MG1655_empty_landing_pads/1"
                )
            ],
            treatments=[
                Treatment.create_from(
                    attribute=Attribute.create_from(
                        name='temperature',
                        value=Value(
                            value=37.0, unit=temperature_unit))),
                Treatment.create_from(
                    entity=NamedEntity(name="M9 Glucose CAA",
                                       reference="https://hub.sd2e.org/user/sd2e/design/M9_glucose_CAA/1")),
                Treatment.create_from(
                    entity=NamedEntity(
                        name='IPTG',
                        reference='https://hub.sd2e.org/user/sd2e/design/IPTG/1',
                        attributes=[
                            Attribute.create_from(
                                name='concentration', unit=micromolar_unit)
                        ])
                ),
                Treatment.create_from(
                    entity=NamedEntity(
                        name='L-arabinose',
                        reference='https://hub.sd2e.org/user/sd2e/design/Larabinose/1',
                        attributes=[
                            Attribute.create_from(
                                name='concentration', unit=micromolar_unit)
                        ])
                ),
                Treatment.create_from(
                    entity=NamedEntity(
                        name='Kan',
                        reference='https://hub.sd2e.org/user/sd2e/design/Kan/1',
                        attributes=[
                            Attribute.create_from(
                                name='concentration',
                                unit=microgram_per_milliliter_unit)
                        ])
                )
            ],
            designs=[
                DesignBlock(
                    label='strains',
                    definition=SumBlock(block_list=[
                        TupleBlock(block_list=[
                            SubjectReference(
                                entity=nand_circuit),
                            TreatmentReference.create_from(
                                treatment=kan)
                        ]),
                        SubjectReference(
                            entity=empty_landing_pads)
                    ])
                ),
                DesignBlock(
                    label='temperature-media',
                    definition=TupleBlock(block_list=[
                        TreatmentReference.create_from(
                            treatment=temperature),
                        TreatmentReference.create_from(treatment=media)
                    ])
                ),
                DesignBlock(
                    label='conditions',
                    definition=ProductBlock(block_list=[
                        GenerateBlock(
                            treatment=iptg,
                            values=[
                                Value(
                                    value=0,
                                    unit=micromolar_unit),
                                Value(
                                    value=0.25,
                                    unit=micromolar_unit),
                                Value(
                                    value=2.5,
                                    unit=micromolar_unit),
                                Value(
                                    value=25,
                                    unit=micromolar_unit),
                                Value(
                                    value=250,
                                    unit=micromolar_unit)
                            ]),
                        GenerateBlock(
                            treatment=l_arabinose,
                            values=[
                                Value(
                                    value=0,
                                    unit=micromolar_unit),
                                Value(
                                    value=5,
                                    unit=micromolar_unit),
                                Value(
                                    value=50,
                                    unit=micromolar_unit),
                                Value(
                                    value=500,
                                    unit=micromolar_unit),
                                Value(
                                    value=5000,
                                    unit=micromolar_unit),
                                Value(
                                    value=25000,
                                    unit=micromolar_unit)
                            ]),
                    ])
                ),
                DesignBlock(
                    label='experiment',
                    definition=ProductBlock(block_list=[
                        ReplicateBlock(
                            count=4,
                            block=ProductBlock(block_list=[
                                BlockReference(label='strains'),
                                BlockReference(label='temperature-media'),
                                BlockReference(label='conditions')
                            ])
                        ),
                        GenerateBlock(
                            treatment=timepoint,
                            values=[
                                Value(
                                    value=5,
                                    unit=hour_unit),
                                Value(
                                    value=6.5,
                                    unit=hour_unit),
                                Value(
                                    value=8,
                                    unit=hour_unit),
                                Value(
                                    value=18,
                                    unit=hour_unit)
                            ]
                        ),
                    ])
                )
            ],
            measurements=[
                Measurement(
                    type='FLOW',
                    block=BlockReference(label='experiment'),
                    controls=[
                        Control(
                            name='positive_gfp',
                            sample=Sample(
                                subject=SubjectReference(
                                    entity=nand_circuit),
                                treatments=[
                                    TreatmentReference.create_from(
                                        treatment=timepoint, value=Value(
                                            value=18, unit=hour_unit)),
                                    TreatmentReference.create_from(
                                        treatment=iptg, value=Value(
                                            value=0, unit=micromolar_unit))
                                ]
                            )
                        ),
                        Control(
                            name='negative_gfp',
                            sample=Sample(subject=SubjectReference(
                                entity=empty_landing_pads))
                        )
                    ],
                    performers=['Ginkgo']
                )
            ]
        )
        assert r1 == r1
        assert r1 == r2
        assert r1 != {}
        assert repr(r1) == "ExperimentalRequest(cp_name='NOVEL_CHASSIS', reference_name='NovelChassis-NAND-Ecoli-Titration', reference_url='https://docs.google.com/document/d/1oMC5VM3XcFn6zscxLKLUe4U-TXbBsz8H6OQwHal1h4g', version=Version(major=1, minor=0, patch=0), derived_from=None, subjects=[NamedEntity(name='MG1655_NAND_Circuit', reference='https://hub.sd2e.org/user/sd2e/design/MG1655_NAND_Circuit/1'), NamedEntity(name='MG1655_empty_landing_pads', reference='https://hub.sd2e.org/user/sd2e/design/MG1655_empty_landing_pads/1')], treatments=[AttributeTreatment(attribute=BoundAttribute(name='temperature', value=Value(value=37.0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000027')))), EntityTreatment(entity=NamedEntity(name='M9 Glucose CAA', reference='https://hub.sd2e.org/user/sd2e/design/M9_glucose_CAA/1')), EntityTreatment(entity=NamedEntity(name='IPTG', reference='https://hub.sd2e.org/user/sd2e/design/IPTG/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])), EntityTreatment(entity=NamedEntity(name='L-arabinose', reference='https://hub.sd2e.org/user/sd2e/design/Larabinose/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])), EntityTreatment(entity=NamedEntity(name='Kan', reference='https://hub.sd2e.org/user/sd2e/design/Kan/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000274'))]))], designs=[DesignBlock(label='strains', definition=SumBlock(block_list=[TupleBlock(block_list=[SubjectReference(entity=NamedEntity(name='MG1655_NAND_Circuit', reference='https://hub.sd2e.org/user/sd2e/design/MG1655_NAND_Circuit/1')), TreatmentReference(treatment=EntityTreatment(entity=NamedEntity(name='Kan', reference='https://hub.sd2e.org/user/sd2e/design/Kan/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000274'))])))]), SubjectReference(entity=NamedEntity(name='MG1655_empty_landing_pads', reference='https://hub.sd2e.org/user/sd2e/design/MG1655_empty_landing_pads/1'))])), DesignBlock(label='temperature-media', definition=TupleBlock(block_list=[TreatmentReference(treatment=AttributeTreatment(attribute=BoundAttribute(name='temperature', value=Value(value=37.0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000027'))))), TreatmentReference(treatment=EntityTreatment(entity=NamedEntity(name='M9 Glucose CAA', reference='https://hub.sd2e.org/user/sd2e/design/M9_glucose_CAA/1')))])), DesignBlock(label='conditions', definition=ProductBlock(block_list=[GenerateBlock(treatment=EntityTreatment(entity=NamedEntity(name='IPTG', reference='https://hub.sd2e.org/user/sd2e/design/IPTG/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])), values=[Value(value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=0.25, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=2.5, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=25, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=250, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))]), GenerateBlock(treatment=EntityTreatment(entity=NamedEntity(name='L-arabinose', reference='https://hub.sd2e.org/user/sd2e/design/Larabinose/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])), values=[Value(value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=5, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=50, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=500, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=5000, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')), Value(value=25000, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])])), DesignBlock(label='experiment', definition=ProductBlock(block_list=[ReplicateBlock(count=4, block=ProductBlock(block_list=[BlockReference(label='strains'), BlockReference(label='temperature-media'), BlockReference(label='conditions')])), GenerateBlock(treatment=TreatmentReference(treatment=AttributeTreatment(attribute=UnboundAttribute(name='timepoint', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032')))), values=[Value(value=5, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032')), Value(value=6.5, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032')), Value(value=8, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032')), Value(value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))])]))], measurements=[Measurement(type='FLOW', block=BlockReference(label='experiment'), controls=[Control(name='positive_gfp', sample=Sample(subject=SubjectReference(entity=NamedEntity(name='MG1655_NAND_Circuit', reference='https://hub.sd2e.org/user/sd2e/design/MG1655_NAND_Circuit/1')), treatments=[TreatmentValueReference(treatment=AttributeTreatment(attribute=UnboundAttribute(name='timepoint', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))), value=Value(value=18, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000032'))), TreatmentValueReference(treatment=EntityTreatment(entity=NamedEntity(name='IPTG', reference='https://hub.sd2e.org/user/sd2e/design/IPTG/1', attributes=[UnboundAttribute(name='concentration', unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064'))])), value=Value(value=0, unit=Unit(reference='http://purl.obolibrary.org/obo/UO_0000064')))])), Control(name='negative_gfp', sample=Sample(subject=SubjectReference(entity=NamedEntity(name='MG1655_empty_landing_pads', reference='https://hub.sd2e.org/user/sd2e/design/MG1655_empty_landing_pads/1')), treatments=[]))], performers=['Ginkgo'])])"

    def test_experiment_serialization(self):
        temperature_unit = Unit(
            reference='http://purl.obolibrary.org/obo/UO_0000027')
        hour_unit = Unit(reference='http://purl.obolibrary.org/obo/UO_0000032')
        micromolar_unit = Unit(
            reference='http://purl.obolibrary.org/obo/UO_0000064')
        microgram_per_milliliter_unit = Unit(
            reference='http://purl.obolibrary.org/obo/UO_0000274')
        nand_circuit = NamedEntity(
            name="MG1655_NAND_Circuit",
            reference="https://hub.sd2e.org/user/sd2e/design/MG1655_NAND_Circuit/1"
        )
        empty_landing_pads = NamedEntity(
            name="MG1655_empty_landing_pads",
            reference="https://hub.sd2e.org/user/sd2e/design/MG1655_empty_landing_pads/1"
        )
        temperature = Treatment.create_from(
            attribute=Attribute.create_from(
                name='temperature',
                value=Value(
                    value=37.0,
                    unit=temperature_unit
                )))
        timepoint = Treatment.create_from(
            attribute=Attribute.create_from(
                name='timepoint',
                unit=hour_unit)
        )
        media = Treatment.create_from(
            entity=NamedEntity(name="M9 Glucose CAA",
                               reference="https://hub.sd2e.org/user/sd2e/design/M9_glucose_CAA/1"))
        iptg = Treatment.create_from(
            entity=NamedEntity(
                name='IPTG',
                reference='https://hub.sd2e.org/user/sd2e/design/IPTG/1',
                attributes=[
                    Attribute.create_from(
                        name='concentration', unit=micromolar_unit)
                ])
        )
        l_arabinose = Treatment.create_from(
            entity=NamedEntity(
                name='L-arabinose',
                reference='https://hub.sd2e.org/user/sd2e/design/Larabinose/1',
                attributes=[
                    Attribute.create_from(
                        name='concentration', unit=micromolar_unit)
                ])
        )
        kan = Treatment.create_from(
            entity=NamedEntity(
                name='Kan',
                reference='https://hub.sd2e.org/user/sd2e/design/Kan/1',
                attributes=[
                    Attribute.create_from(
                        name='concentration', unit=microgram_per_milliliter_unit)
                ])
        )
        r1 = ExperimentalRequest(
            cp_name='NOVEL_CHASSIS',
            reference_name='NovelChassis-NAND-Ecoli-Titration',
            reference_url='https://docs.google.com/document/d/1oMC5VM3XcFn6zscxLKLUe4U-TXbBsz8H6OQwHal1h4g',
            version=Version(major=1, minor=0, patch=0),
            subjects=[
                NamedEntity(
                    name="MG1655_NAND_Circuit",
                    reference="https://hub.sd2e.org/user/sd2e/design/MG1655_NAND_Circuit/1"
                ),
                NamedEntity(
                    name="MG1655_empty_landing_pads",
                    reference="https://hub.sd2e.org/user/sd2e/design/MG1655_empty_landing_pads/1"
                )
            ],
            treatments=[
                Treatment.create_from(
                    attribute=Attribute.create_from(
                        name='temperature',
                        value=Value(
                            value=37.0, unit=temperature_unit))
                ),
                Treatment.create_from(
                    entity=NamedEntity(
                        name="M9 Glucose CAA",
                        reference="https://hub.sd2e.org/user/sd2e/design/M9_glucose_CAA/1")
                ),
                Treatment.create_from(
                    entity=NamedEntity(
                        name='IPTG',
                        reference='https://hub.sd2e.org/user/sd2e/design/IPTG/1',
                        attributes=[
                            Attribute.create_from(
                                name='concentration', unit=micromolar_unit)
                        ])
                ),
                Treatment.create_from(
                    entity=NamedEntity(
                        name='L-arabinose',
                        reference='https://hub.sd2e.org/user/sd2e/design/Larabinose/1',
                        attributes=[
                            Attribute.create_from(
                                name='concentration',
                                unit=micromolar_unit)
                        ])
                ),
                Treatment.create_from(
                    entity=NamedEntity(
                        name='Kan',
                        reference='https://hub.sd2e.org/user/sd2e/design/Kan/1',
                        attributes=[
                            Attribute.create_from(
                                name='concentration', unit=microgram_per_milliliter_unit)
                        ])
                )
            ],
            designs=[
                DesignBlock(
                    label='strains',
                    definition=SumBlock(block_list=[
                        TupleBlock(block_list=[
                            SubjectReference(entity=nand_circuit),
                            TreatmentReference.create_from(treatment=kan)
                        ]),
                        SubjectReference(entity=empty_landing_pads)
                    ])
                ),
                DesignBlock(
                    label='temperature-media',
                    definition=TupleBlock(block_list=[
                        TreatmentReference.create_from(
                            treatment=temperature),
                        TreatmentReference.create_from(treatment=media)
                    ])
                ),
                DesignBlock(
                    label='conditions',
                    definition=ProductBlock(block_list=[
                        GenerateBlock(
                            treatment=iptg,
                            values=[
                                Value(
                                    value=0,
                                    unit=micromolar_unit),
                                Value(
                                    value=0.25,
                                    unit=micromolar_unit),
                                Value(
                                    value=2.5,
                                    unit=micromolar_unit),
                                Value(
                                    value=25,
                                    unit=micromolar_unit),
                                Value(
                                    value=250,
                                    unit=micromolar_unit)
                            ]),
                        GenerateBlock(
                            treatment=l_arabinose,
                            values=[
                                Value(
                                    value=0,
                                    unit=micromolar_unit),
                                Value(
                                    value=5,
                                    unit=micromolar_unit),
                                Value(
                                    value=50,
                                    unit=micromolar_unit),
                                Value(
                                    value=500,
                                    unit=micromolar_unit),
                                Value(
                                    value=5000,
                                    unit=micromolar_unit),
                                Value(
                                    value=25000,
                                    unit=micromolar_unit)
                            ]),
                    ])
                ),
                DesignBlock(
                    label='experiment',
                    definition=ProductBlock(block_list=[
                        ReplicateBlock(
                            count=4,
                            block=ProductBlock(block_list=[
                                BlockReference(label='strains'),
                                BlockReference(label='temperature-media'),
                                BlockReference(label='conditions')
                            ])
                        ),
                        GenerateBlock(
                            treatment=timepoint,
                            values=[
                                Value(value=5, unit=hour_unit),
                                Value(value=6.5, unit=hour_unit),
                                Value(value=8, unit=hour_unit),
                                Value(value=18, unit=hour_unit)
                            ]
                        ),
                    ])
                )
            ],
            measurements=[
                Measurement(
                    type='FLOW',
                    block=BlockReference(label='experiment'),
                    controls=[
                        Control(
                            name='positive_gfp',
                            sample=Sample(
                                subject=nand_circuit,
                                treatments=[
                                    TreatmentReference.create_from(
                                        treatment=timepoint,
                                        value=Value(value=18, unit=hour_unit)),
                                    TreatmentReference.create_from(
                                        treatment=iptg,
                                        value=Value(value=0,
                                                    unit=micromolar_unit))
                                ]
                            )
                        ),
                        Control(
                            name='negative_gfp',
                            sample=Sample(subject=empty_landing_pads)
                        )
                    ],
                    performers=['Ginkgo']
                )
            ]
        )
        r_json = json.dumps(r1, cls=ExperimentEncoder)
        r2 = json.loads(r_json, cls=ExperimentDecoder)
        assert r1 == r2
