import json
from cp_request import (
    ExperimentEncoder,
    ExperimentalRequest,
    NamedEntity,
    Version
)


def main():
    request = ExperimentalRequest(
        cp_name='PROTEIN_DESIGN',
        reference_name='',
        reference_url='',
        version=Version(major=1, minor=0, patch=0),
        subjects=[
            NamedEntity(
                name='NODS4 in PetconV4 B1A2',
                reference='27786'
            ),
            NamedEntity(
                name='Protein Design Ladder 1 PetconV4 B1A2',
                reference='27787'
            ),
            NamedEntity(
                name='NODS4 with Protein Design Ladder 1 in PetconV4 B1A2',
                reference='28349'
            ),
            NamedEntity(
                name='SDO -His -Trp -Ura',
                reference='https://hub.sd2e.org/user/sd2e/design/SDO0x200x2DHis0x200x2DTrp0x200x2DUra/1'
            ),
            NamedEntity(
                name='SDO + 2% Galactose -His -Trp -Ura',
                reference='https://hub.sd2e.org/user/sd2e/design/SDO0x200x2B0x2020x250x20Galactose0x200x2DHis0x200x2DTrp0x200x2DUra/1'
            ),
            NamedEntity(
                name='Chymotrypsin',
                reference='https://hub.sd2e.org/user/sd2e/design/Chymotrypsin/1'
            ),
            NamedEntity(
                name='Anti-c-myc-FITC',
                reference='22039'
            ),
            NamedEntity(
                name='TBS',
                reference='22035'
            ),
            NamedEntity(
                name='TBSF',
                reference='22036'
            ),
            NamedEntity(
                name='PBS',
                reference='22033'
            ),
            NamedEntity(
                name='PBSF',
                reference='22034'
            ),
            NamedEntity(
                name='Trypsin',
                reference='https://hub.sd2e.org/user/sd2e/design/Trypsin/1'
            ),
            NamedEntity(
                name='AMA1-best',
                reference='https://hub.sd2e.org/user/sd2e/design/UWBF_21171/1'
            ),
            NamedEntity(
                name='EBY100 + PETCONv3_baker',
                reference='https://hub.sd2e.org/user/sd2e/design/UWBF_21535/1'
            )
        ],
        treatments=[],
        designs=[],
        measurements=[]
    )
    with open('nc_titration_generated.json', 'w') as file:
        json.dump(request, file, cls=ExperimentEncoder, indent=2)


if __name__ == "__main__":
    main()
