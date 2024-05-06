import math
import random
from fractions import Fraction
from typing import Tuple, Iterator, Union, Iterable, Protocol, runtime_checkable, Optional
from copy import copy, deepcopy


@runtime_checkable
class Multipliable(Protocol):
    def __mul__(self, other): ...


@runtime_checkable
class Divisible(Protocol):
    def __truediv__(self, other): ...


class Matrix:
    @staticmethod
    def identity(size: int) -> 'Matrix':
        """
        Create an identity matrix (1s on the main diagonal) of specified size.
        Args:
            size: size of square matrix

        Returns:
            Matrix
        """
        res = Matrix(size, size)
        for i in range(size):
            res[i, i] = 1
        return res

    @classmethod
    def from_array(cls, arr: list[list[Fraction]]) -> 'Matrix':
        res = Matrix(len(arr), len(arr[0]))
        res._data = deepcopy(arr)
        return res

    def __init__(self, height: int, width: int, default: Fraction = Fraction(0, 1)) -> None:
        self._height = height
        self._width = width
        self._data = [[default for _ in range(self.width)] for _ in range(self.height)]

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def is_square(self) -> bool:
        return self.height == self.width

    def __getitem__(self, tup: Tuple[Union[slice, int], Union[slice, int]]) -> 'Matrix':
        row, col = tup
        if isinstance(row, int) and isinstance(col, int):
            return Matrix(1, 1, self._data[row][col])

        if isinstance(row, int):
            row = slice(row, row + 1, 1)
        else:
            row = slice(
                row.start if row.start is not None else 0,
                row.stop if row.stop is not None else self.height,
                row.step if row.step is not None else 1
            )
        if isinstance(col, int):
            col = slice(col, col + 1, 1)
        else:
            col = slice(
                col.start if col.start is not None else 0,
                col.stop if col.stop is not None else self.width,
                col.step if col.step is not None else 1
            )
        num_rows = (row.stop - row.start) // row.step
        num_cols = (col.stop - col.start) // col.step
        res = Matrix(num_rows, num_cols)
        for res_i, cur_i in enumerate(range(row.start, row.stop, row.step)):
            for res_j, cur_j in enumerate(range(col.start, col.stop, col.step)):
                res._data[res_i][res_j] = self._data[cur_i][cur_j]
        return res

    def __setitem__(self, tup: Tuple[Union[slice, int], Union[slice, int]],
                    value: Union[int, float, Fraction, complex]) -> None:
        v: Fraction = Fraction(value, 1) if not isinstance(value, Fraction) else value
        row, col = tup
        if isinstance(row, int) and isinstance(col, int):
            self._data[row][col] = v
            return

        if isinstance(row, int):
            row = slice(row, row + 1, 1)
        else:
            row = slice(
                row.start if row.start is not None else 0,
                row.stop if row.stop is not None else self.height,
                row.step if row.step is not None else 1
            )
        if isinstance(col, int):
            col = slice(col, col + 1, 1)
        else:
            col = slice(
                col.start if col.start is not None else 0,
                col.stop if col.stop is not None else self.width,
                col.step if col.step is not None else 1
            )
        for res_i, cur_i in enumerate(range(row.start, row.stop, row.step)):
            for res_j, cur_j in enumerate(range(col.start, col.stop, col.step)):
                self._data[cur_i][cur_j] = v

    def __copy__(self) -> 'Matrix':
        return self[:, :]

    def __mul__(self, other: Union[int, float, Fraction, complex]) -> 'Matrix':
        if isinstance(other, Matrix):
            raise ValueError("For Matrix Multiplication use '@' operator instead of '*' operator")
        res = self.__copy__()
        for i in range(res.height):
            for j in range(res.width):
                res._data[i][j] *= other
        return res

    def __rmul__(self, other: Union[int, float, Fraction, complex]) -> 'Matrix':
        return self * other

    def __truediv__(self, value: Union[int, float, Fraction, complex]) -> 'Matrix':
        return self * (Fraction(1, value) if not isinstance(value, Fraction) else 1 / value)

    def __floordiv__(self, other: Union[int, float, Fraction, complex]) -> 'Matrix':
        return (self / other).__floor__()

    def __floor__(self) -> 'Matrix':
        res = self[:, :]
        for i in range(self.height):
            for j in range(res.width):
                res._data[i][j] = math.floor(res._data[i][j])
        return res

    def __ceil__(self):
        res = self[:, :]
        for i in range(self.height):
            for j in range(res.width):
                res._data[i][j] = math.ceil(res._data[i][j])
        return res

    def __add__(self, other: 'Matrix') -> 'Matrix':
        if not (self.width == other.width or self.height == other.height):
            raise ValueError('Matrix dimensions do not match')

        res = Matrix(self.width, self.height)
        for i in range(res.height):
            for j in range(res.width):
                res._data[i][j] = self._data[i][j] + other._data[i][j]
        return res

    def __sub__(self, other: 'Matrix') -> 'Matrix':
        return self + (-1 * other)

    def __pow__(self, power: int, modulo=None) -> 'Matrix':
        cur: Matrix = self[:, :]
        for _ in range(power - 1):
            cur @= self
        return cur

    def __matmul__(self, other: 'Matrix') -> 'Matrix':
        if not (self.width == other.height):
            raise ValueError(
                f"Can't perform Matrix multiplication on A={repr(self)} and B={repr(other)} as A.width != B.height")
        res = Matrix(self.height, other.width, 0)
        for i in range(self.height):
            for j in range(other.width):
                for k in range(self.width):
                    res._data[i][j] += self._data[i][k] * other._data[k][j]
        return res

    def __iter__(self) -> Iterator[Fraction]:
        for row in range(self.height):
            for col in range(self.width):
                yield self._data[row][col]

    def __neg__(self) -> 'Matrix':
        return -1 * self  # type:ignore

    def __repr__(self) -> str:
        return f'Matrix({self._width}, {self._height})'

    def __str__(self) -> str:
        rows = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(self._data[i][j])
            rows.append("[" + ", ".join(map(str, row)) + "]")
        return "[" + ", ".join(map(str, rows)) + "]"

    def __len__(self) -> int:
        return self.height * self.width

    def determinant(self) -> Union[float, 'Polynomial']:
        pass

    def transpose(self) -> 'Matrix':
        res = Matrix(self.width, self.height)
        for i in range(self.height):
            for j in range(self.width):
                res._data[j][i] = self._data[i][j]
        return res

    def vectorize(self) -> 'Vector':
        size = len(self)
        res = Vector(size)
        for i in range(self.height):
            for j in range(self.width):
                res[i * self.width + j] = self._data[i][j]
        return res

    def characteristic_polynomial(self) -> 'Polynomial':
        I = Matrix.identity(max(self.width, self.height))
        x = Polynomial([1, 0])
        return (x * I - self).determinant()  # type:ignore

    def eigen_values(self) -> list[Fraction]:
        return self.characteristic_polynomial().roots()  # type:ignore

    @classmethod
    def random(cls, height: int, width: int, a: int = 0, b: int = 100, seed: Optional[int] = None) -> 'Matrix':
        try:
            if seed is not None:
                prev_seed = random.getstate()
                random.seed(seed)

            res = Matrix(height, width)
            for i in range(height):
                for j in range(width):
                    res._data[i][j] = random.randint(a, b)
            return res
        finally:
            if seed is not None:
                random.setstate(prev_seed)


class Vector(Matrix):
    def __init__(self, size: int, default: Fraction = Fraction(0, 1)) -> None:
        super().__init__(size, 1, default)

    @property
    def size(self) -> int:
        return self.height

    def __copy__(self):
        return self[:]

    def __getitem__(self, index: Union[slice, int]) -> 'Vector':  # type:ignore
        m = super().__getitem__((index, 0))
        if isinstance(index, int):
            return Vector(1, m._data[0][0])
        return m.vectorize()

    def __setitem__(self, index: int, value: float) -> None:  # type:ignore
        self._data[index][0] = value

    def __repr__(self) -> str:
        return f'Vector({self.size})'

    def __str__(self) -> str:
        vec = []
        for v in self:
            vec.append(v)
        return "[" + ", ".join(map(str, vec)) + "]"

    def __matmul__(self, other):
        raise ValueError("Can't perform Matrix Multiplication with a vector as the lhs")

    def __rmatmul__(self, other: 'Matrix') -> 'Vector':
        return other.__matmul__(self).vectorize()


class Polynomial:
    def __init__(self, coefficients: Iterable[float]) -> None:
        self._coefficients = list(coefficients)

    @property
    def coefficients(self) -> list[float]:
        return self._coefficients

    @property
    def degree(self) -> int:
        return len(self.coefficients) - 1

    def eval(self, x: float) -> float:
        res = 0.0
        for i, coeff in enumerate(self.coefficients):
            deg = self.degree - i
            res += coeff * x ** deg
        return res

    def __add__(self, other: Union[float, 'Polynomial']) -> 'Polynomial':
        res = self.__copy__()
        if isinstance(other, (float, int)):
            res.coefficients[-1] += other
            return res
        max_deg = min(self.degree, other.degree)
        for i in range(1, max_deg + 2):
            res.coefficients[-i] += other.coefficients[-i]
        return res

    def __sub__(self, other: Union[float, 'Polynomial']) -> 'Polynomial':
        return self + (-1 * other)

    def __copy__(self) -> 'Polynomial':
        return Polynomial(self.coefficients[:])

    def __mul__(self, other: Union[float, 'Polynomial']) -> Union[Matrix, Vector, 'Polynomial', float]:
        if isinstance(other, (float, int)):
            if other == 0:
                return 0.0
            res = self.__copy__()
            for i in range(self.degree + 1):
                res.coefficients[i] *= other
            return res

        if isinstance(other, Matrix):
            return other.__mul__(self)

        res = Polynomial([0 for _ in range(self.degree + other.degree + 1)])
        for deg in range(self.degree + 1):
            coeff = self.coefficients[deg]
            poly = Polynomial(other.coefficients + [0 for _ in range(self.degree - deg)])
            res += coeff * poly
        return res

    def __pow__(self, power: int, modulo=None) -> 'Polynomial':
        if power == 0:
            return 1
        cur = self.__copy__()
        for _ in range(power - 1):
            cur *= self
        return cur

    def __rmul__(self, other: Union[float, 'Polynomial']) -> 'Polynomial':
        return self.__mul__(other)

    def __getitem__(self, index: int) -> float:
        return self.coefficients[index]

    def roots(self, known_roots: list[int]) -> list[float]:
        cur = self.__copy__()
        for root in known_roots:
            cur /= Polynomial(1) - root

        pass

    def __call__(self, x: float) -> float:
        return self.eval(x)

    def __repr__(self) -> str:
        return f"Polynomial(deg={self.degree})"

    def __str__(self) -> str:
        parts = []
        for i, v in enumerate(self.coefficients):
            deg = self.degree - i
            if v == 0:
                continue
            if deg == 0:
                if v < 0:
                    parts.append(f"\b\b- {abs(v)}")
                else:
                    parts.append(f"{v}")
            elif deg == 1:
                if v == 1:
                    parts.append("x")
                elif v == -1:
                    parts.append("-x")
                elif v < 0:
                    parts.append(f"\b\b- {abs(v)}x")
                else:
                    parts.append(f"{v}x")
            else:
                if v == 1:
                    parts.append(f"x^{deg}")
                elif v == -1:
                    parts.append(f"(-x)^{deg}")
                elif v > 0:
                    parts.append(f"{v}x^{deg}")
                else:
                    parts.append(f"\b\b- {abs(v)}*x^{deg}")
        return " + ".join(parts)


__all__ = [
    "Matrix",
    "Vector",
    "Polynomial"
]
