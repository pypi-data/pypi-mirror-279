from math import sqrt
from typing import TypeVar

from scipy.stats import chi2, norm, t

from classes.range import Range
from classes.alfa_wrapper import AlfaWrapper


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
    def mean(values: list[float], std: float | None = None) -> AlfaWrapper:
        """
        Estimates confidence interval for mean of a normal distribution.
        :param values: values on with to estimate mean
        :param std: standard deviation
        :return: estimated confidence interval for mean
        """
        n = len(values)
        ex = sum(values) / n

        if std is None:
            std = sqrt(Estimator.NEW(values))
            if n <= 30:
                def res(alfa: float):
                    v = t.ppf(1 - alfa / 2, n - 1) * std / sqrt(n)
                    return Range(ex - v, ex + v)

                return AlfaWrapper(res)

        def res(alfa: float):
            return Range(ex - norm.ppf(1 - alfa / 2) * std / sqrt(n),
                         ex + norm.ppf(1 - alfa / 2) * std / sqrt(n))

        return AlfaWrapper(res)

    @staticmethod
    def variation(values: list[float]) -> AlfaWrapper:
        """
        Estimates confidence interval for variance.
        :param values: values on with to estimate variance
        :return: confidence interval estimator for variance.
        """
        n = len(values)
        s2 = Estimator.NEW(values)

        def res(alfa: float):
            return Range((n - 1) * s2 / chi2.ppf(1 - alfa / 2, n - 1),
                         (n - 1) * s2 / chi2.ppf(alfa / 2, n - 1))

        return AlfaWrapper(res)

    T = TypeVar("T")

    @staticmethod
    def proportion(values: list[T], value: T) -> AlfaWrapper:
        """
        Estimates confidence interval for probability of given value.
        :param values: values on with to estimate proportion
        :param value: value for with we estimate
        :return: estimated confidence interval for proportion
        """
        n = len(values)
        p = sum(1 for ele in values if ele == value) / n

        def res(alfa: float):
            return Range(p - norm.ppf(1 - alfa / 2) * sqrt(p * (1 - p) / n),
                         p + norm.ppf(1 - alfa / 2) * sqrt(p * (1 - p) / n))

        return AlfaWrapper(res)
