from math import sqrt
from rpis_lib.typing_fix import Self

from rpis_lib.consts import ECLIPSE
from rpis_lib.estimator import Estimator
from rpis_lib.utils import _check_norm, _check_t, _check_norm_t, _check_chi
from .enums import HypothesisType
from .results import CompareMeanResult, MeanResult, VariationResult, DifferenceResult
from .types import HypothesisPart


class MeanPart(HypothesisPart):
    def __init__(self, values: list[float], std: float | None):
        self.values = values
        self.std = std

    def __str__(self):
        v = [str(f) for f in self.values]
        return ", ".join(v[:ECLIPSE]) + " ... " + v[-1]

    def _get_result_type(self, other) -> HypothesisPart.CompareHypothesisResultConstructor:
        if isinstance(other, float) or isinstance(other, int):
            return MeanResult
        return CompareMeanResult

    def _calculate(self, other: float, _type: HypothesisType, alfa: float):
        n = len(self.values)
        ex = sum(self.values) / n

        if self.std is None:
            self.std = sqrt(Estimator.NEW(self.values))

        z = (ex - other) / (self.std / sqrt(n))
        return not _check_norm_t(z, n - 1, alfa, _type, n > 30 and self.std is not None)

    def _compare(self, other: Self, _type: HypothesisType, alfa: float):
        n1 = len(self.values)
        ex1 = sum(self.values) / n1

        n2 = len(other.values)
        ex2 = sum(other.values) / n2

        if self.std is None or other.std is None:
            s1 = Estimator.NEW(self.values)
            s2 = Estimator.NEW(other.values)
            sp = sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
            v = (ex1 - ex2) / (sp * sqrt(1 / n1 + 1 / n2))
            return not _check_t(v, n1 + n2 - 2, alfa, _type)
        else:
            s1 = self.std * self.std
            s2 = other.std * other.std
            v = (ex1 - ex2) / sqrt(s1 / n1 + s2 / n2)
            return not _check_norm(v, n1 + n2 - 2, alfa, _type)


class ProportionMeanPart(HypothesisPart):
    def __init__(self, n: int, p: int, std: float | None):
        self.p = p
        self.n = n
        self.std = std

    def __str__(self):
        return f"{self.p}/{self.n}"

    def _get_result_type(self, other) -> HypothesisPart.CompareHypothesisResultConstructor:
        if isinstance(other, float) or isinstance(other, int):
            return MeanResult
        return CompareMeanResult

    def _calculate(self, other: float, _type: HypothesisType, alfa: float):
        ex = self.p / self.n
        if self.std is None:
            std = sqrt(other * (1 - other) / self.n)
            z = (ex - other) / (std / sqrt(self.n))
            return not _check_norm_t(z, self.n - 1, alfa, _type, self.n > 30 and std is not None)
        else:
            z = (ex - other) / (self.std / sqrt(self.n))
            return not _check_norm_t(z, self.n - 1, alfa, _type, self.n > 30 and self.std is not None)

    def _compare(self, other: Self, _type: HypothesisType, alfa: float):
        ex1 = self.p / self.n
        ex2 = other.p / other.n

        if self.std is None or other.std is None:
            p = (self.p + other.p) / (self.n + other.n)
            sp = sqrt(p * (1 - p))
            v = (ex1 - ex2) / (sp * sqrt(1 / self.n + 1 / other.n))
            return not _check_t(v, self.n + other.n - 2, alfa, _type)
        else:
            s1 = self.std * self.std
            s2 = other.std * other.std
            v = (ex1 - ex2) / sqrt(s1 / self.n + s2 / other.n)
            return not _check_norm(v, self.n + other.n - 2, alfa, _type)


class VariationEstimatePart(HypothesisPart):
    def __init__(self, values: list[float]):
        self.values = values

    def __str__(self):
        v = [str(f) for f in self.values]
        return ", ".join(v[:ECLIPSE]) + " ... " + v[-1]

    def _get_result_type(self, other) -> HypothesisPart.CompareHypothesisResultConstructor:
        return VariationResult

    def _calculate(self, other: float, _type: HypothesisType, alfa: float):
        n = len(self.values)

        v = ((n - 1) * Estimator.NEW(self.values)) / other
        return not _check_chi(v, n - 1, alfa, _type)


class VariationPart(HypothesisPart):
    def __init__(self, n: int, var: float):
        self.n = n
        self.var = var

    def __str__(self):
        return f"n={self.n} v={self.var}"

    def _get_result_type(self, other) -> HypothesisPart.CompareHypothesisResultConstructor:
        return VariationResult

    def _calculate(self, other: float, _type: HypothesisType, alfa: float):
        v = ((self.n - 1) * self.var) / other
        return not _check_chi(v, self.n - 1, alfa, _type)


class DifferencePart(HypothesisPart):
    def __init__(self, values_a: list[float], values_b: list[float]):
        self.values_a = values_a
        self.values_b = values_b

    def __str__(self):
        a = [str(f) for f in self.values_a]
        b = [str(f) for f in self.values_b]
        return ", ".join(a[:ECLIPSE]) + " ... " + a[-1] + " - " + ", ".join(b[:ECLIPSE]) + " ... " + b[-1]

    def _get_result_type(self, other) -> HypothesisPart.CompareHypothesisResultConstructor:
        return DifferenceResult

    def _calculate(self, other: float, _type: HypothesisType, alfa: float):
        if len(self.values_a) != len(self.values_b):
            raise ValueError(f'Different number of values: {len(self.values_a)} != {len(self.values_b)}')

        n = len(self.values_a)
        values = [self.values_a[i] - self.values_b[i] for i in range(n)]
        ex = sum(values) / n

        v = (ex - other) / (sqrt(Estimator.NEW(values)) / sqrt(n))
        return not _check_t(v, n - 1, alfa, _type)
