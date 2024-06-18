try:
    from typing import Self as s
except:
    from typing import TypeVar

    s = TypeVar("Self")

Self = s
