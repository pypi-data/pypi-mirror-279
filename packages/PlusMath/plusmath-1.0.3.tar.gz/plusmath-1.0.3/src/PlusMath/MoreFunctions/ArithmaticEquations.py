import math

def factorial(n: int) -> int:
    """Factorial of n (n!)
    :param n: int
    :return: int"""

    if n in [0, 1]:
        return n

    SUM = 1
    for i in range(1, n + 1):
        SUM *= i
    return SUM

def fibonacci(n: int) -> int:
    """A recursive algorithm that calculates the fibonacci sequence
    :param n: The number you would like to parse into the function"""
    if n <= 1:
        return n

    return int(((1 + math.sqrt(5)) ** n - (1 - math.sqrt(5)) ** n) / (2 ** n * math.sqrt(5)))

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