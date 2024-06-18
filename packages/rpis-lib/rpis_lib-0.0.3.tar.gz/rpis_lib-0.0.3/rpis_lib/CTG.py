from math import exp, factorial, sqrt
from scipy.stats import norm

from .consts import inf


def poisson(n: int, p: float, k: int | list[float]) -> float | tuple[float, float]:
    """
    Estimates number of successes in Bernoulli.
    :param n: number of samples
    :param p: probability distribution
    :param k: number or list of numbers of successes
    :return: estimated probability of given number of successes
    """
    if isinstance(k, list):
        return sum(poisson(n, p, _k) for _k in k), ((n * p) ** 2) / n
    else:
        return (((n * p) ** k) / factorial(k)) * exp(-n * p)


def poisson_lambda(lam: float, k: int) -> float:
    """
    Estimates number of successes in Bernoulli.
    :param lam: lambda parameter or mean value
    :param k: number of successes
    :return: estimated probability of given number of successes
    """
    return ((lam ** k) / factorial(k)) * exp(-lam)


def CTG(n: int, mean: float, std: float, lover_bound: float = -inf, upper_bound: float = inf) -> float:
    """
    Central Limit Theorem, estimates that sum of give variables is in given range
    :param n: number of samples
    :param mean: mean of distribution
    :param std: standard deviation of distribution
    :param lover_bound: lower bound of the range
    :param upper_bound: upper bound of the range
    :return:
    """

    def v(x):
        return (x - n * mean) / (std * sqrt(n))

    return float(norm.cdf(v(upper_bound)) - norm.cdf(v(lover_bound)))
