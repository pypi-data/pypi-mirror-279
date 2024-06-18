from __future__ import annotations
from typing import Any
import math

class Number(float):
    def __init__(self, value: int | float = 0):
        self.value = value
        self._val = value

    def __repr__(self):
        return self.value

    def __int__(self):
        return round(self.value)

    def __str__(self):
        return str(self.value)

    def __float__(self):
        return float(self.value)

    @property
    def IsPrime(self) -> bool:
        """Returns whether the number is prime or not

        :return: bool"""
        value = self.value

        maximum: float = math.sqrt(value)
        for i in range(2, math.ceil(maximum)):
            if value % i == 0:
                return False

        return True
