class Vector3:
    __slots__ = {'x', 'y', 'z', 'pos', 'weakref'}

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
        self.pos: tuple = x, y, z

    def __repr__(self):
        return f"Vector3(x: {self.x}, y: {self.y}, z: {self.z})"

    def __eq__(self, other):
        return self.pos == other.pos

    def __gt__(self, other):
        return self.pos > other.pos

    def __ge__(self, other):
        return self.pos >= other.pos

    @classmethod
    def get_absolute(cls):
        return Vector3(0, 0, 0)