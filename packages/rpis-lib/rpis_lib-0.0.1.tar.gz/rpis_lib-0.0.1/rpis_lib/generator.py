from math import log, cos, pi, sqrt, floor
from typing import Callable


class Generator:

    @staticmethod
    def uniform(n: int, seed: int = 5, lower_bound: float = 0, upper_bound: float = 1) -> list[float]:
        """
        Generate n random numbers between lower_bound and upper_bound from uniform distribution.
        :param n: count of random numbers
        :param seed: random seed
        :param lower_bound: lower bound
        :param upper_bound: upper bound
        :return: list of random numbers
        """
        A = 2147483647
        u = [seed]

        for i in range(n - 1):
            u.append((u[i] * 16807) % A)

        return [(x / A) * (upper_bound - lower_bound) + lower_bound for x in u]

    @staticmethod
    def exponential(n: int, seed: int = 5, lam: float = 1) -> list[float]:
        """
        Generate n random numbers from exponential distribution.
        :param n: count of random numbers
        :param seed: random seed
        :param lam: lam of exponential distribution
        :return: list of random numbers
        """
        cx = Generator.uniform(n, seed)
        return [-log(1 - x) / lam for x in cx]

    @staticmethod
    def normal(n, seed: int = 5):
        """
        Generate n random numbers from normal distribution.
        :param n: count of random numbers
        :param seed: random seed
        :return: list of random numbers
        """
        cxy = Generator.uniform(n * 2, seed)
        cy, cx = cxy[n:], cxy[:n]
        return [sqrt(-2 * log(x)) * cos(2 * pi * y) for x, y in zip(cx, cy)]

    @staticmethod
    def discrete(n: int, k: int = 6, seed: int = 5):
        """
        Generate n random numbers between 1 and k from discrete distribution.
        :param n: count of random numbers
        :param k: count of discrete values [1,k]
        :param seed: random seed
        :return: list of random numbers
        """
        cx = Generator.uniform(n, seed, 1, k + 1)
        return [k if x == k + 1 else floor(x) for x in cx]


def integral_mc(fun: Callable[[float], float], n: int = 1000000, lower_bound: float = 0, upper_bound: float = 1,
                seed: int = 5):
    """
    Calculate integral of fun using Monte Carlo method.
    :param fun: function to be integrated
    :param n: count of random numbers
    :param lower_bound: bottom limit of integral
    :param upper_bound: upper limit of integral
    :param seed: seed for random generator
    :return: integral value
    """
    cx = Generator.uniform(n, seed, lower_bound, upper_bound)
    cy = [fun(x) for x in cx]
    return sum(cy) / n
