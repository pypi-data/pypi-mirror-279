from typing import Self

class Vector3:
    __slots__ = {'x', 'y', 'z', 'pos', 'weakref'}

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
        self.pos: float = x + y + z

    def __repr__(self):
        return f"Vector3(x: {self.x}, y: {self.y}, z: {self.z})"

    def __eq__(self, other: Self):
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)

    def __gt__(self, other):
        return self.pos > other.pos

    def __ge__(self, other):
        return self.pos >= other.pos

    def distance(self, other: Self) -> float:
        return ((other.y - self.y) + (other.x - self.x) + (other.z - self.z)) / 3

    @classmethod
    def get_absolute(cls):
        return Vector3(0, 0, 0)