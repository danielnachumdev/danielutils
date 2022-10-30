class Polynomial:
    def __init__(self, prefixes: list[int], powers: list[int]):
        self.prefixes = prefixes
        self.powers = powers

    def __len__(self) -> int:
        return len(self.prefixes)

    def __call__(self, value):
        res = 0
        for i in range(len(self)):
            res += self.prefixes[i]*(value**self.powers[i])
        return res
