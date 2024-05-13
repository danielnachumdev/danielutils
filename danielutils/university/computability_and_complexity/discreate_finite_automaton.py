import random
from typing import Set, Callable, Sequence, Collection, Tuple, Dict, TypeVar, Generic

State = TypeVar('State')
Symbol = TypeVar('Symbol')
Alphabet = Collection[Symbol]
TransitionFunction = Callable[[State, Symbol], State]


class DiscreteFiniteAutomaton(Generic[State, Symbol]):
    def __init__(self, Q: Collection[State], sigma: Alphabet, delta: TransitionFunction, q0: State,
                 F: Collection[State]):
        """

        Args:
            Q: set of possible states
            sigma: the alphabet
            delta: the transition function
            q0: the initial state
            F: the accept states
        """
        self.Q: Set[State] = set(Q)
        self.sigma: Sequence[Symbol] = list(sigma)
        self.delta: TransitionFunction = delta
        self.q0: State = q0
        self.F: Set[State] = set(F)
        self._verify()

    def process(self, word: Sequence[Symbol]) -> State:
        cur = self.q0
        for letter in word:
            cur = self.delta(cur, letter)
        return cur

    def run(self, word: Sequence[Symbol]) -> bool:
        return self.process(word) in self.F

    def __call__(self, word: Sequence[Symbol]) -> bool:
        return self.run(word)

    def _verify(self) -> None:
        for letter in self.sigma:
            for state in self.Q:
                try:
                    res = self.delta(state, letter)
                except Exception as e:
                    raise ValueError(f'delta({state}, {letter}) raised an exception') from e
                if not res in self.Q:
                    raise ValueError(f'delta({state}, {letter}) = {state} which is not in F = {self.Q}')

    def random_word(self, k: int) -> Sequence[Symbol]:
        return tuple(random.choices(self.sigma, k=k))

    @staticmethod
    def delta_from_dict(dct: Dict[Tuple[State, Symbol], State]) -> TransitionFunction:
        return lambda state, letter: dct[(state, letter)]


DFA = DiscreteFiniteAutomaton

__all__ = [
    "State",
    "Symbol",
    "Alphabet",
    "TransitionFunction",
    "DiscreteFiniteAutomaton",
    "DFA"
]
