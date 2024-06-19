try:
    from typing import Self as S
    from typing import Any as A
    from typing import Unpack as U
except:
    from typing import TypeVar

    S = TypeVar("Self")
    A = TypeVar("Any")
    U = TypeVar("Unpack")

Self = S
Any = A
Unpack = U
