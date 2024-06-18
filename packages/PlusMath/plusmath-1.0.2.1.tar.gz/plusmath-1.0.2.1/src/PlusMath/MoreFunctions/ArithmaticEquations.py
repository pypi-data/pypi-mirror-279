import math
import cmath
import numpy
from functools import cache

@cache
def factorial(n: int | complex) -> complex:
    """Factorial of n (n!)
    :param n: int | complex
    :return: complex"""
    val: int | float
    if isinstance(n, complex):
        val = n.real
    else:
        val = n

    if val == 1:
        return complex(val)

    return complex(complex(val) + factorial(complex(val) - 1))

def fibonacci(n: int) -> int:
    """A recursive algorithm that calculates the fibonacci sequence
    :param n: The number you would like to parse into the function"""
    if n <= 1:
        return n
    
    return fibonacci(n - 1) + fibonacci(n - 2)

def IsDividableBy(largernum: int | complex, lowernum: int | complex) -> bool:
    """Returns whether the larger number is dividable by the lower number
    :param largernum: The larger number
    :param lowernum: The lower number
    :return: bool"""
    if isinstance(largernum, complex):
        largernum = largernum.real
    if isinstance(lowernum, complex):
        lowernum = lowernum.real

    n: float = float(largernum)
    i: float = float(lowernum)

    return n % i == 0