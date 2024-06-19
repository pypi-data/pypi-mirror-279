from copy import deepcopy
from functools import partial
from typing import Callable
from rpis_lib.typing_fix import Self, Unpack

from rpis_lib.consts import DEFAULT_ALFA, MAX_ALFA
from .alfa_wrapper import process_alfa, alfa_to_percentage
from .enums import HypothesisType
from .lists import CustomList


class HypothesisResult:
    def __init__(self, value: bool):
        self.value = value

    def __call__(self, *args, **kwargs):
        return self.value

    def __str__(self):
        return self.value.__str__()

    def __repr__(self):
        return self.__str__()

    def __bool__(self):
        return self.value


HypothesisFunction = Callable[[float, HypothesisType], bool]
HypothesisResultConstructor = Callable[[HypothesisFunction, float, HypothesisType], HypothesisResult]


class HypothesisPart:
    CompareHypothesisResultConstructor = Callable[
        [Self, float | Self, HypothesisType], HypothesisResult]

    def __gt__(self, other: Self | float) -> HypothesisResult:
        return self._get_result_type(other)(self, other, HypothesisType.RIGHT)

    def __lt__(self, other: Self | float) -> HypothesisResult:
        return self._get_result_type(other)(self, other, HypothesisType.LEFT)

    def __ne__(self, other: Self | float) -> HypothesisResult:
        return self._get_result_type(other)(self, other, HypothesisType.BOTH)

    def get_calculate(self, other: Self | float, _type: HypothesisType):
        if isinstance(other, float) or isinstance(other, int):
            return partial(self._calculate, other, _type)
        return partial(self._compare, other, _type)

    def _get_result_type(self, other) -> CompareHypothesisResultConstructor:
        raise NotImplemented()

    def _calculate(self, other: float, _type: HypothesisType, alfa: float):
        raise NotImplemented()

    def _compare(self, other: Self, _type: HypothesisType, alfa: float):
        raise NotImplemented()


class CompareHypothesisResult(HypothesisResult):

    def __init__(self, part1: HypothesisPart, part2: HypothesisPart | float, _type: HypothesisType, alfa=DEFAULT_ALFA):
        self.part1 = part1
        self.part2 = part2
        self._type = _type
        self.alfa = alfa

        self.calculate = self.part1.get_calculate(self.part2, _type)
        super().__init__(self.calculate(self.alfa))

    def clone(self, alfa: float):
        c = deepcopy(self)
        c.alfa = alfa
        c.recalculate()
        return c

    def recalculate(self):
        self.value = self.calculate(self.alfa)

    def __call__(self, *args: Unpack[float]) -> Self | list[Self]:
        return process_alfa(self, args)

    def __str__(self):
        if self._type == HypothesisType.BOTH:
            return f"[{alfa_to_percentage(self.alfa)}%] {self._str_both()}"
        elif self._type == HypothesisType.LEFT:
            return f"[{alfa_to_percentage(self.alfa)}%] {self._str_left()}"
        elif self._type == HypothesisType.RIGHT:
            return f"[{alfa_to_percentage(self.alfa)}%] {self._str_right()}"

    def _str_both(self):
        raise NotImplemented()

    def _str_left(self):
        raise NotImplemented()

    def _str_right(self):
        raise NotImplemented()
