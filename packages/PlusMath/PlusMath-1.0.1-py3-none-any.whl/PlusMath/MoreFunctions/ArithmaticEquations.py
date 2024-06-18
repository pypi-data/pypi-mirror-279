import math
import cmath
import numpy
from functools import cache

@cache
def factorial(n: int | complex) -> complex:
    val: int | float
    if isinstance(n, complex):
        val = n.real
    else:
        val = n

    if val == 1:
        return complex(val)

    return complex(complex(val) + factorial(complex(val) - 1))

def IsDividableBy(largernum: int | complex, lowernum: int | complex):
    if isinstance(largernum, complex):
        largernum = largernum.real
    if isinstance(lowernum, complex):
        lowernum = lowernum.real

    n: float = float(largernum)
    i: float = float(lowernum)

    return n % i == 0