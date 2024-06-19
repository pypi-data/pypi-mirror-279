from copy import deepcopy
from typing import Callable

from classes.lists import CustomList
from consts import MAX_ALFA, DEFAULT_ALFA
from typing_fix import Self, Any, Unpack


def process_alfa(self, args: tuple[float]):
    if len(args) == 0:
        return self

    if len(args) == 1:
        self.alfa = args[0]
        self.recalculate()
        return self

    res = CustomList()
    for arg in args:
        if not isinstance(arg, float):
            raise TypeError(f"Argument must be float ({type(arg)} != float in {arg})")
        if arg > MAX_ALFA:
            raise ValueError(f"Student debil :-) ({arg} > {MAX_ALFA})")
        res.append(self.clone(arg))
    return res


def alfa_to_percentage(alfa: float):
    return (1 - alfa) * 100


class AlfaWrapper:
    def __init__(self, func: Callable[[float], Any]):
        self.func = func
        self.alfa = DEFAULT_ALFA
        self.value = self.func(self.alfa)

    def __call__(self, *args: Unpack[float]) -> Self | list[Self]:
        if len(args) == 0:
            return self.value
        return process_alfa(self, args)

    def clone(self, alfa: float):
        c = deepcopy(self)
        c.alfa = alfa
        c.recalculate()
        return c

    def recalculate(self):
        self.value = self.func(self.alfa)

    def __str__(self):
        return f"[{alfa_to_percentage(self.alfa)}%] {str(self.value)}"

    def __repr__(self):
        return self.__str__()
