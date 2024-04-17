from enum import Enum
from .conditional_variables import ConditionalVariable
from .conditional_variables.discrete import Bernoulli, Geometric, Uniform, Binomial, Poisson


class DiscreteDistribution(Enum):
    Ber = Bernoulli
    Geo = Geometric
    Unif = Uniform
    Bin = Binomial
    Pois = Poisson

    def __call__(self, *args, **kwargs) -> ConditionalVariable:
        return self.value(*args, **kwargs)


class ContinuousDistribution(Enum):
    Unif = None
    Exp = None
    Normal = None


class Distribution:
    Discrete = DiscreteDistribution
    Continuous = ContinuousDistribution
    #     def __getattr__(self, item):
    #         if item in map(lambda x: x.name, list(self.value)):
    #             print("foo")
    #         return super().__getattr__(item)

__all__ = [
    'DiscreteDistribution',
    'ContinuousDistribution',
    'Distribution'
]
