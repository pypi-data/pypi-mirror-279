from math import sqrt
from typing import TypeVar

from scipy.stats import chi2, norm, t


class Estimator:

    @staticmethod
    def NEW(values: list[float]) -> float:
        """
        Unbiased variance estimator.
        :param values: values on with to estimate variance
        :return: estimated variance
        """
        n = len(values)
        ex = sum(values) / n
        s = sum((x - ex) ** 2 for x in values)
        return 1 / (n - 1) * s

    @staticmethod
    def mean(values: list[float], alfa: float, std: float | None = None) -> tuple[float, float]:
        """
        Estimates confidence interval for mean of a normal distribution.
        :param values: values on with to estimate mean
        :param std: standard deviation
        :param alfa: factor of which we allow error
        :return: estimated confidence interval for mean
        """
        n = len(values)
        ex = sum(values) / n

        if std is None:
            std = sqrt(Estimator.NEW(values))
            if n <= 30:
                v = t.ppf(1 - alfa / 2, n - 1) * std / sqrt(n)
                return ex - v, ex + v

        return ex - norm.ppf(1 - alfa / 2) * std / sqrt(n), ex + norm.ppf(1 - alfa / 2) * std / sqrt(n)

    @staticmethod
    def variation(values: list[float], alfa: float) -> tuple[float, float]:
        """
        Estimates confidence interval for variance.
        :param values: values on with to estimate variance
        :param alfa: factor of which we allow error
        :return: confidence interval estimator for variance.
        """
        n = len(values)
        s2 = Estimator.NEW(values)
        return (n - 1) * s2 / chi2.ppf(1 - alfa / 2, n - 1), (n - 1) * s2 / chi2.ppf(alfa / 2, n - 1)

    T = TypeVar("T")

    @staticmethod
    def proportion(values: list[T], value: T, alfa: float) -> tuple[float, float]:
        """
        Estimates confidence interval for probability of given value.
        :param values: values on with to estimate proportion
        :param value: value for with we estimate
        :param alfa: factor of which we allow error
        :return: estimated confidence interval for proportion
        """
        n = len(values)
        p = sum(1 for ele in values if ele == value) / n
        return p - norm.ppf(1 - alfa / 2) * sqrt(p * (1 - p) / n), p + norm.ppf(1 - alfa / 2) * sqrt(p * (1 - p) / n)
