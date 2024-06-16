from pyphy.vector2 import Vector2

class AABB:
    def __init__(self, minX: float, minY: float, maxX: float, maxY: float) -> None:
        self.minVector = Vector2(minX, minY)
        self.maxVector = Vector2(maxX, maxY)