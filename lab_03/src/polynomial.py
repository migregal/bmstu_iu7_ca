from __future__ import annotations
from math import prod


class Polynomial(object):
    terms: list[callable[float]:float]

    def __init__(self, terms: list[callable[float]:float]):
        self.terms = terms

    def __call__(self, arg: float) -> float:
        return sum([term(arg) for term in self.terms])


class NewtonPolynomial(Polynomial):

    @staticmethod
    def build(points: list[list[float]], arg: float, n: int) -> NewtonPolynomial:
        table = NewtonPolynomial._make_table(points, arg, n)

        return NewtonPolynomial(
            [lambda x:table[1][0]] +
            [NewtonPolynomial._term(table[i][0],  table[0][:i - 1])
             for i in range(2, len(table))]
        )

    @staticmethod
    def _term(va: float, vl: list[float]) -> callable:
        return lambda x: va * prod(map(lambda a: (x - a), vl))

    @staticmethod
    def _make_table(points: list[list[float]], arg: float, n: int) -> list[list[float]]:
        base = sorted(sorted(points, key=lambda p: abs(p[0] - arg))[:n+1])

        t = [[0.0 for i in range(len(base))] for j in range(n + 2)]

        for i in range(len(t[0])):
            t[0][i], t[1][i] = base[i][0], base[i][1]

        for i in range(2, len(t)):
            for j in range(len(base) - i + 1):
                t[i][j] = (t[i - 1][j] - t[i - 1][j + 1]) / \
                    (t[0][j] - t[0][j + i - 1])

        return t
