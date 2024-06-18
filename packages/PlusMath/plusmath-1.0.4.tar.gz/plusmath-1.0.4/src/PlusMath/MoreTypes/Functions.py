from __future__ import annotations
from .Numbers import Number
import math

def IsPrime(self: int | float | Number = Number(0)) -> bool:
    value = None
    if isinstance(self, Number):
        value = self.value
    else:
        value = self

    maximum: float = math.sqrt(value)
    for i in range(2, math.ceil(maximum)):
        if value % i == 0:
            return False

    return True
