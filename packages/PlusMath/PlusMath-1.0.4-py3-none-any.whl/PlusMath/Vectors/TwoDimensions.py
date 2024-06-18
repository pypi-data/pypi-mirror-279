from typing import Self

class Vector2:
    __slots__ = {'x', 'y', 'pos', 'weakref'}

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.pos: float = x + y

    def __repr__(self):
        return f"Vector2(x: {self.x}, y: {self.y})"

    def __eq__(self, other: Self):
        return (self.x, self.y) == (other.x, other.y)

    def __gt__(self, other):
        return self.pos > other.pos

    def __ge__(self, other):
        return self.pos >= other.pos

    def distance(self, other: Self) -> float:
        return ((other.y - self.y) + (other.x - self.x)) / 2

    @classmethod
    def get_absolute(cls):
        return Vector2(0, 0)

class OrderedVector2:
    __slots__ = {'x', 'y', 'zOrder', 'pos', 'weakref'}

    def __init__(self, x: float, y: float, zOrder: int):
        self.x = x
        self.y = y
        self.zOrder = zOrder
        self.pos: float = x + y + zOrder

    def __repr__(self):
        return f"OrderedVector2(x: {self.x}, y: {self.y}, zOrder: {self.z})"

    def __eq__(self, other: Self):
        return (self.x, self.y, self.zOrder) == (other.x, other.y, other.zOrder)

    def __gt__(self, other):
        return self.pos > other.pos

    def __ge__(self, other):
        return self.pos >= other.pos

    def distance(self, other: Self) -> float:
        return ((other.y - self.y) + (other.x - self.x)) / 2

    @classmethod
    def get_absolute(cls):
        return OrderedVector2(0, 0, 0)