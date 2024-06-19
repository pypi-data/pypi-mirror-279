from scipy.stats import chi2

from classes.alfa_wrapper import AlfaWrapper
from rpis_lib import poisson_lambda

from .classes.parts import (DifferencePart, MeanPart, ProportionMeanPart,
                            VariationEstimatePart, VariationPart)
from .classes.results import IsPoissonResult, IsUniformResult
from .classes.types import HypothesisPart, HypothesisResult


class Hypothesis:
    @staticmethod
    def is_uniform(values: list[float]) -> AlfaWrapper:
        """
        Checks if the given values are uniformly distributed.
        :param values: values to check
        :return: True if values are uniformly distributed, False otherwise
        """
        n = len(values)
        ex = sum(values) / n
        v = sum([((ele - ex) ** 2) for ele in values]) / ex

        def res(alfa):
            ok = v > chi2.ppf(1 - alfa, n - 1)
            return IsUniformResult(not ok)

        return AlfaWrapper(res)

    @staticmethod
    def is_poisson(values: list[float], lam: float) -> AlfaWrapper:
        """
        Checks if the given values are poisson distributed.
        :param values: values to check
        :param lam: lambda parameter
        :return: True if values are poisson distributed, False otherwise
        """
        n = len(values)
        s = sum(values)
        v = 0
        for i in range(n):
            ex = poisson_lambda(lam, i) * s
            v += ((values[i] - ex) ** 2) / ex

        def res(alfa):
            ok = v > chi2.ppf(1 - alfa, n - 2)
            return IsPoissonResult(not ok)

        return AlfaWrapper(res)

    @staticmethod
    def mean(values: list[float], std: float | None = None) -> HypothesisPart:
        """
        Checks if the given values have some mean.
        :param values: values to check
        :param std: standard deviation of values
        :return: Object that can be compared to other mean or float value
        """
        return MeanPart(values, std)

    @staticmethod
    def proportion_mean(n: int, p: int, std: float | None = None) -> HypothesisPart:
        """
        **Deprecated** \n
        Checks if the given proportion have some mean.
        :param n: number of values
        :param p: number of successes
        :param std: standard deviation of values
        :return: Object that can be compared to other mean or float value
        """
        return ProportionMeanPart(n, p, std)

    @staticmethod
    def variation_estimate(values: list[float]) -> HypothesisPart:
        """
        Checks if the given values have some variation.
        :param values: values to check
        :return: Object that can be compared to float value
        """
        return VariationEstimatePart(values)

    @staticmethod
    def variation(n: int, var: float) -> HypothesisPart:
        """
        Checks if the given number of values with some variation have some variation.
        :param n: number of values
        :param var: variance of values
        :return: Object that can be compared to float value
        """
        return VariationPart(n, var)

    @staticmethod
    def difference(values_a: list[float], values_b: list[float]) -> HypothesisPart:
        """
        Checks if difference of two given values_a and values_b have some mean.
        :param values_a: first values
        :param values_b: second values
        :return: Object that can be compared to float value
        """
        return DifferencePart(values_a, values_b)
