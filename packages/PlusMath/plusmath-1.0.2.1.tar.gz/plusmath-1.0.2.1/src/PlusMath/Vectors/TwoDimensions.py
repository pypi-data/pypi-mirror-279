class Vector2:
    __slots__ = {'x', 'y', 'pos', 'weakref'}

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.pos: tuple = x, y

    def __repr__(self):
        return f"Vector2(x: {self.x}, y: {self.y})"

    def __eq__(self, other):
        return self.pos == other.pos

    def __gt__(self, other):
        return self.pos > other.pos

    def __ge__(self, other):
        return self.pos >= other.pos

    @classmethod
    def get_absolute(cls):
        return Vector2(0, 0)

class OrderedVector2:
    __slots__ = {'x', 'y', 'zOrder', 'pos', 'weakref'}

    def __init__(self, x: float, y: float, zOrder: float):
        self.x = x
        self.y = y
        self.zOrder = zOrder
        self.pos: tuple = x, y, zOrder

    def __repr__(self):
        return f"OrderedVector2(x: {self.x}, y: {self.y}, zOrder: {self.z})"

    def __eq__(self, other):
        return self.pos == other.pos

    def __gt__(self, other):
        return self.pos > other.pos

    def __ge__(self, other):
        return self.pos >= other.pos

    @classmethod
    def get_absolute(cls):
        return OrderedVector2(0, 0, 0)