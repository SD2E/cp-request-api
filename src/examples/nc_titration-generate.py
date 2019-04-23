import json
from cp_request import (
    Attribute,
    Control,
    ExperimentEncoder,
    ExperimentalRequest,
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


def main():
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
        entity=NamedEntity(
            name="M9 Glucose CAA",
            reference="https://hub.sd2e.org/user/sd2e/design/M9_glucose_CAA/1"
        ))
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
    request = ExperimentalRequest(
        cp_name='NOVEL_CHASSIS',
        reference_name='NovelChassis-NAND-Ecoli-Titration',
        reference_url='https://docs.google.com/document/d/1oMC5VM3XcFn6zscxLKLUe4U-TXbBsz8H6OQwHal1h4g',
        version=Version(major=1, minor=0, patch=0),
        subjects=[nand_circuit, empty_landing_pads],
        treatments=[iptg, kan, l_arabinose, media, temperature, timepoint],
        designs=[
            DesignBlock(
                label='strains',
                definition=SumBlock(block_list=[
                    TupleBlock(block_list=[
                        SubjectReference(entity=nand_circuit),
                        TreatmentReference(treatment=kan)
                    ]),
                    SubjectReference(entity=empty_landing_pads)
                ])
            ),
            DesignBlock(
                label='temperature-media',
                definition=TupleBlock(block_list=[
                    TreatmentReference(treatment=temperature),
                    TreatmentReference(treatment=media)
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
                            subject=nand_circuit,
                            treatments=[
                                TreatmentReference.create_from(
                                    treatment=timepoint,
                                    value=Value(
                                        value=18,
                                        unit=hour_unit)),
                                TreatmentReference.create_from(
                                    treatment=iptg,
                                    value=Value(
                                        value=0,
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
            ),
            Measurement(
                type='PLATE_READER',
                block=BlockReference(label='experiment'),
                performers=['Ginkgo']
            ),
            Measurement(
                type='RNA_SEQ',
                block=BlockReference(label='experiment'),
                performers=['Ginkgo']
            ),
            Measurement(
                type='PROTEOMICS',
                block=BlockReference(label='experiment'),
                performers=['Ginkgo']
            ),
        ]
    )
    with open('nc_titration_generated.json', 'w') as file:
        json.dump(request, file, cls=ExperimentEncoder, indent=2)


if __name__ == "__main__":
    main()
