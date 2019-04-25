import json
from cp_request import (
    ExperimentEncoder,
    ExperimentalRequest,
    NamedEntity,
    Treatment,
    Version
)


def main():
    base_library = NamedEntity(
        name='NODS4 in PetconV4 B1A2',
        reference='https://hub.sd2e.org/user/sd2e/design/NODS40x20in0x20PetconV40x20B1A2/1'
    )
    ladder = NamedEntity(
        name='Protein Design Ladder 1 PetconV4 B1A2',
        reference='https://hub.sd2e.org/user/sd2e/design/Protein0x20Design0x20Ladder0x2010x20PetconV40x20B1A2/1'
    )
    library = NamedEntity(
        name='NODS4 with Protein Design Ladder 1 in PetconV4 B1A2',
        reference='https://hub.sd2e.org/user/sd2e/design/NODS40x20with0x20Protein0x20Design0x20Ladder0x2010x20in0x20PetconV40x20B1A2/1'
    )

    request = ExperimentalRequest(
        cp_name='PROTEIN_DESIGN',
        reference_name='',
        reference_url='',
        version=Version(major=1, minor=0, patch=0),
        subjects=[base_library, ladder, library],
        treatments=[
            Treatment.create_from(
                entity=NamedEntity(
                    name='SDO -His -Trp -Ura',
                    reference='https://hub.sd2e.org/user/sd2e/design/SDO0x200x2DHis0x200x2DTrp0x200x2DUra/1'
                )
            ),
            Treatment.create_from(
                entity=NamedEntity(
                    name='SDO + 2% Galactose -His -Trp -Ura',
                    reference='https://hub.sd2e.org/user/sd2e/design/SDO0x200x2B0x2020x250x20Galactose0x200x2DHis0x200x2DTrp0x200x2DUra/1'
                )
            ),
            Treatment.create_from(
                entity=NamedEntity(
                    name='Chymotrypsin',
                    reference='https://hub.sd2e.org/user/sd2e/design/Chymotrypsin/1'
                )
            ),
            Treatment.create_from(
                entity=NamedEntity(
                    name='Anti-c-myc-FITC',
                    reference='https://hub.sd2e.org/user/sd2e/design/Anti0x2Dc0x2Dmyc0x2DFITC/1'
                )
            ),
            Treatment.create_from(
                entity=NamedEntity(
                    name='TBS',
                    reference='https://hub.sd2e.org/user/sd2e/design/Tris0x20Buffered0x20Saline/1'
                )
            ),
            Treatment.create_from(
                entity=NamedEntity(
                    name='TBSF',
                    reference='https://hub.sd2e.org/user/sd2e/design/Tris0x20Buffered0x20Saline0x200x2B0x2010x250x20BSA/1'
                )
            ),
            Treatment.create_from(
                entity=NamedEntity(
                    name='PBS',
                    reference='https://hub.sd2e.org/user/sd2e/design/pbs/1'
                )
            ),
            Treatment.create_from(
                entity=NamedEntity(
                    name='PBSF',
                    reference='https://hub.sd2e.org/user/sd2e/design/Phosphate0x20Buffered0x20Saline0x200x2B0x2010x250x20BSA/1'
                )
            ),
            Treatment.create_from(
                entity=NamedEntity(
                    name='Trypsin',
                    reference='https://hub.sd2e.org/user/sd2e/design/Trypsin/1'
                )
            ),
            Treatment.create_from(
                entity=NamedEntity(
                    name='AMA1-best',
                    reference='https://hub.sd2e.org/user/sd2e/design/UWBF_21171/1'
                )
            ),
            Treatment.create_from(
                entity=NamedEntity(
                    name='EBY100 + PETCONv3_baker',
                    reference='https://hub.sd2e.org/user/sd2e/design/UWBF_21535/1'
                ))],
        designs=[],
        measurements=[]
    )
    with open('nc_titration_generated.json', 'w') as file:
        json.dump(request, file, cls=ExperimentEncoder, indent=2)


if __name__ == "__main__":
    main()
