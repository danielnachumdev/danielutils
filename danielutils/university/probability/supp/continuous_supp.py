from .supp import Supp
class ContinuousSupp(Supp):
    def intersect(self, other: "Supp") -> "Supp":
        pass


__all__=[
    "ContinuousSupp"
]