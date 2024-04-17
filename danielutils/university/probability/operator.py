from enum import Enum


class Operator(Enum):
    EQ = "EQ"
    NE = "NE"
    GT = "GT"
    GE = "GE"
    LT = "LT"
    LE = "LE"

    _INVERSE_MAP: dict['Operator', 'Operator'] = {
        EQ: NE,
        NE: EQ,
        GT: LE,
        LE: GT,
        GE: LT,
        LT: GE
    }

    @property
    def inverse(self) -> 'Operator':
        return Operator._INVERSE_MAP[self]


__all__ = [
    "Operator"
]
