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
    TreatmentReference
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

    strain_block = DesignBlock(
        label='strains',
        definition=SumBlock(block_list=[
            ProductBlock(block_list=[
                SubjectReference(entity=nand_circuit),
                TreatmentReference(treatment=kan)
            ]),
            SubjectReference(entity=empty_landing_pads)
        ])
    )
    temperature_block = DesignBlock(
        label='temperature-media',
        definition=ProductBlock(block_list=[
            TreatmentReference(treatment=temperature),
            TreatmentReference(treatment=media)
        ])
    )
    condition_block = DesignBlock(
        label='conditions',
        definition=ProductBlock(block_list=[
            GenerateBlock(
                treatment=iptg,
                attribute_name='concentration',
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
                attribute_name='concentration',
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
    )
    experiment_block = DesignBlock(
        label='experiment',
        definition=ProductBlock(block_list=[
            ReplicateBlock(
                count=4,
                block=ProductBlock(block_list=[
                    BlockReference(block=strain_block),
                    BlockReference(block=temperature_block),
                    BlockReference(block=condition_block)
                ])
            ),
            GenerateBlock(
                treatment=timepoint,
                attribute_name='timepoint',
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

    flow_measurement = Measurement(
        type='FLOW',
        block=BlockReference(block=experiment_block),
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
    )
    plate_reader_measurement = Measurement(
        type='PLATE_READER',
        block=BlockReference(block=experiment_block),
        performers=['Ginkgo']
    )
    rnaseq_measurement = Measurement(
        type='RNA_SEQ',
        block=BlockReference(block=experiment_block),
        performers=['Ginkgo']
    )
    proteomic_measurement = Measurement(
        type='PROTEOMICS',
        block=BlockReference(block=experiment_block),
        performers=['Ginkgo']
    )

    request = ExperimentalRequest(
        cp_name='NOVEL_CHASSIS',
        reference_name='NovelChassis-NAND-Ecoli-Titration',
        reference_url='https://docs.google.com/document/d/1oMC5VM3XcFn6zscxLKLUe4U-TXbBsz8H6OQwHal1h4g',
        version=Version(major=1, minor=0, patch=0),
        subjects=[
            nand_circuit,
            empty_landing_pads
        ],
        treatments=[
            iptg,
            kan,
            l_arabinose,
            media,
            temperature,
            timepoint
        ],
        designs=[
            strain_block,
            temperature_block,
            condition_block,
            experiment_block
        ],
        measurements=[
            flow_measurement,
            plate_reader_measurement,
            rnaseq_measurement,
            proteomic_measurement
        ]
    )

    with open('nc_titration_generated.json', 'w') as file:
        json.dump(request, file, cls=ExperimentEncoder, indent=2)


if __name__ == "__main__":
    main()
