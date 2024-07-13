from typing import TypeVar, Collection, Callable, Set, List, Sequence, Tuple, Union, Literal

State = TypeVar('State')
Symbol = TypeVar('Symbol')
Alphabet = Collection[Symbol]
Direction = Union[Literal["L"], Literal["R"]]
TransitionFunction = Callable[[State, Symbol], Tuple[State, Symbol, Direction]]


class TuringMachine:
    def __init__(self, Q: Collection[State], Gamma: Alphabet, Sigma: Alphabet, delta: TransitionFunction, q0: State,
                 F_acc: Collection[State], F_rej: Collection[State]) -> None:
        self.Q: Set[State] = set(Q)
        self.Gamma: List[State] = list(Gamma)
        self.Sigma: List[State] = list(Sigma)
        self.delta: TransitionFunction = delta
        self.q0: State = q0
        self.F_acc: Set[State] = set(F_acc)
        self.F_rej: Set[State] = set(F_rej)
        self.tape: List[Symbol] = []
        self.head: int = 0

    def _should_stop(self, cur_state: State) -> bool:
        return cur_state in self.F_acc or cur_state in self.F_rej

    def process(self, word: Sequence[Symbol]) -> State:
        for letter in word:
            self.tape.append(letter)
        cur = self.q0
        while not self._should_stop(cur):
            state, symbol, direction = self.delta(cur, self.tape[self.head])
            cur = state
            self.tape[self.head] = symbol
            self.head += 1 if direction == "R" else -1

        return cur

    def run(self, word: Sequence[Symbol]) -> bool:
        return self.process(word) in self.F_acc

    def __call__(self, word: Sequence[Symbol]) -> bool:
        return self.run(word)


__all__ = [
    'TuringMachine'
]
