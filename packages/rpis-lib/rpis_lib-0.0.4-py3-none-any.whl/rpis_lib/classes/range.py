class Range:
    def __init__(self, lower: float, upper: float) -> None:
        self.lower = lower
        self.upper = upper

    def __str__(self) -> str:
        return f"({self.lower},{self.upper})"

    def __repr__(self) -> str:
        return self.__str__()

    def __contains__(self, key) -> bool:
        return self.lower < key < self.upper

    def tuple(self) -> tuple[float, float]:
        return self.lower, self.upper
