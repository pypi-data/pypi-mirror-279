from pyphy.vector2 import Vector2
from pyphy.body import Body

class Manifold:
    def __init__(self, bodyA: Body, bodyB: Body, normal: Vector2, depth: float, contact1: Vector2, contact2: Vector2, contactCount: int) -> None:
        self.bodyA = bodyA
        self.bodyB = bodyB
        self.normal = normal
        self.depth = depth
        self.contact1 = contact1
        self.contact2 = contact2
        self.contactCount = contactCount