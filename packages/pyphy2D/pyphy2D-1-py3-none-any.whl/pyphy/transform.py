from pyphy.vector2 import Vector2
import math as m

class Transform:
    def __init__(self, pos, angle) -> None:
        self.position = pos
        self.sin = m.sin(angle)
        self.cos = m.cos(angle)

    @classmethod
    def zero(cls) -> "Transform":
        return Transform(Vector2.zero(), 0)