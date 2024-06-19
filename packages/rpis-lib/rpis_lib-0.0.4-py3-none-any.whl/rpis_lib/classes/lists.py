from typing import TypeVar

from typing_fix import Self

T = TypeVar("T")


class CustomList:
    def __init__(self):
        self.results = []

    def append(self, result: T) -> Self:
        self.results.append(result)
        return self

    def __iter__(self):
        return iter(self.results)

    def __len__(self):
        return len(self.results)

    def __getitem__(self, i):
        return self.results[i]

    def __setitem__(self, i, value):
        self.results[i] = value
        return self

    def __delitem__(self, i):
        del self.results[i]
        return self

    def __contains__(self, item):
        return item in self.results

    def __str__(self):
        return "\n".join(str(ele) for ele in self.results)

    def __repr__(self):
        return self.__str__()
