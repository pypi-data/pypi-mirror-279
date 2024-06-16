from pyphy.pygame_integration import PyphyPygame
from pyphy.transform import Transform
from pyphy.boundingbox import AABB
from pyphy.vector2 import Vector2
from pyphy.pyphymath import math

class Body:
    CIRCLE = 0
    BOX = 1
    POLYGON = 2

    def __init__(self, pos: Vector2, mass: float, density: float, restitution: float, area: float, shape, radius: float, width: float, height: float, static: bool, vertices=None) -> None:
        self.position = pos
        self.linearVelocity = Vector2.zero()
        self.angularVelocity = 0
        self.angle = 0

        self.mass = mass
        self.InvMass = 0 if static else (1 / self.mass)
        self.density = density
        self.restitution = restitution
        self.area = area
        self.shape = shape
        self.radius = radius
        self.width = width
        self.height = height
        self.isStatic = static

        if self.shape != Body.CIRCLE:
            self.vertices = vertices or self.__createBoxVertices__(width, height)
        else:
            self.vertices = None

        self.Inertia = self.CalculateRotationalInertia()
        self.InvInertia = 0 if self.isStatic else (1 / self.Inertia)

        self.StaticFriction = 0.6
        self.DynamicFriction = 0.4

        self.force = Vector2.zero()

        self.texture = None
        self.color = (0, 255, 255) if static else (255, 255, 0)

        self.transformedVertices = self.vertices
        self.transformedVerticesUpdateRequired = True

        self.aabb = None
        self.aabbUpdateRequired = True

        self.triangles = None if shape == Body.CIRCLE else self.__createTriangleBox__()

    def SetTexture(self, texture) -> None:
        if self.shape == Body.CIRCLE:
            self.texture = PyphyPygame.ScaleImage(texture, (self.radius*2, self.radius*2))
        else:
            self.texture = PyphyPygame.ScaleImage(texture, (self.width, self.height))

    def SetFriction(self, staticFrictionCof, dynamicFrictionCof) -> None:
        self.StaticFriction = staticFrictionCof
        self.DynamicFriction = dynamicFrictionCof
    
    @staticmethod
    def __createTriangleBox__() -> list[int]:
        return [0, 1, 2, 0, 2, 3]

    @staticmethod
    def __createBoxVertices__(width, height) -> list[Vector2]:
        return [
            Vector2(-width/2, height/2),
            Vector2(width/2, height/2),
            Vector2(width/2, -height/2),
            Vector2(-width/2, -height/2)
        ]
    
    @staticmethod
    def __calculatePolygonArea__(vertices: list[Vector2]) -> float:
        n = len(vertices)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += vertices[i].x * vertices[j].y
            area -= vertices[j].x * vertices[i].y
        area = abs(area) / 2.0
        return area
    
    def CalculateRotationalInertia(self) -> float:
        if self.shape == Body.CIRCLE:
            return self.mass * self.radius ** 2 / 2

        elif self.shape == Body.BOX:
            return self.mass / 12 * (self.width ** 2 + self.height ** 2)
        
        elif self.shape == Body.POLYGON:
            inertia = 0.0
            for i in range(len(self.vertices)):
                j = (i + 1) % len(self.vertices)
                cross = self.vertices[i].cross(self.vertices[j])
                dot = self.vertices[i].dot(self.vertices[i] + self.vertices[j])
                inertia += (cross * dot)
            self.shape = Body.BOX
            return (self.density / 6.0) * abs(inertia)
    
    def getAABB(self) -> AABB:
        if not self.aabbUpdateRequired:
            return self.aabb

        minX = float('inf')
        minY = float('inf')
        maxX = float('-inf')
        maxY = float('-inf')

        if self.shape == Body.CIRCLE:
            minX = self.position.x - self.radius
            minY = self.position.y - self.radius
            maxX = self.position.x + self.radius
            maxY = self.position.y + self.radius

        else:
            tv = self.getTransformedVertices()
            for v in tv:
                minX = min(v.x, minX)
                minY = min(v.y, minY)
                maxX = max(v.x, maxX)
                maxY = max(v.y, maxY)

        self.aabb = AABB(minX, minY, maxX, maxY)
        self.aabbUpdateRequired = False
        return self.aabb

    def getTransformedVertices(self) -> None:
        if not self.transformedVerticesUpdateRequired:
            return self.transformedVertices
        
        transformer = Transform(self.position, self.angle)
        self.transformedVertices = [Vector2.transform(vertex, transformer) for vertex in self.vertices]
        self.transformedVerticesUpdateRequired = False
        return self.transformedVertices
    
    def step(self, gravity, dt) -> None:
        if self.isStatic:
            return
        
        self.linearVelocity += gravity * dt
        self.position += self.linearVelocity * dt
        self.angle += self.angularVelocity * dt

        self.force = Vector2.zero()
        self.transformedVerticesUpdateRequired = True
        self.aabbUpdateRequired = True

    def ApplyForce(self, force: Vector2) -> None:
        self.force = force

    def Move(self, velocity: Vector2) -> None:
        self.position += velocity
        self.transformedVerticesUpdateRequired = True
        self.aabbUpdateRequired = True

    def MoveTo(self, position: Vector2) -> None:
        self.position = position
        self.transformedVerticesUpdateRequired = True
        self.aabbUpdateRequired = True

    def Rotate(self, angle: float) -> None:
        self.angle += angle
        self.angle %= 360
        self.transformedVerticesUpdateRequired = True
        self.aabbUpdateRequired = True

    @staticmethod
    def __scale_and_transform_vertices__(vertices: list[Vector2], width: float, height: float, position: Vector2) -> list[Vector2]:
        scaled_vertices = []
        for vertex in vertices:
            scaled_vertex = Vector2(vertex.x * width, -vertex.y * height)
            scaled_vertices.append(scaled_vertex)
        return scaled_vertices

    @classmethod
    def CreateCircleBody(cls, radius: float, center: Vector2, density: float, restitution: float, static: bool) -> "Body":
        area = 3.14 * radius ** 2
        mass = area * density
        return cls(center, mass, density, math.clamp(restitution, 0, 1), area, Body.CIRCLE, radius, 0, 0, static)

    @classmethod
    def CreateBoxBody(cls, width: float, height: float, pos: Vector2, density: float, restitution: float, static: bool) -> "Body":
        area = width * height
        mass = area * density
        return cls(pos, mass, density, math.clamp(restitution, 0, 1), area, Body.BOX, 0, width, height, static)
    
    @classmethod
    def CreatePolygon(cls, vertices: list[Vector2], width: float, height: float, pos: Vector2, density: float, restitution: float, static: bool) -> "Body":
        transformed_vertices = cls.__scale_and_transform_vertices__(vertices, width, height, pos)
        area = cls.__calculatePolygonArea__(transformed_vertices)
        mass = area * density
        return cls(pos, mass, density, math.clamp(restitution, 0, 1), area, Body.POLYGON, 0, width, height, static, transformed_vertices)