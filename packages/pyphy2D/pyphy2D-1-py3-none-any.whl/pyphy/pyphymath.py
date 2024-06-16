from pyphy.vector2 import Vector2
import math as m

class math:
    DistanceThreshhold = 0.5

    @property
    def pi(self) -> float:
        return 3.141592653589793

    @staticmethod
    def Average(*args) -> float:
        return sum(args) / len(args)

    @staticmethod
    def ToDegrees(radians: float) -> float:
        return radians * 180 / math.pi

    @staticmethod
    def distance(vec1: Vector2, vec2: Vector2) -> float:
        return ((vec1.x - vec2.x)**2 + (vec1.y - vec2.y)**2)**0.5
    
    @staticmethod
    def angle_radians(vec1: Vector2, vec2: Vector2) -> float:
        return m.atan2(vec2.y - vec1.y, vec2.x - vec1.x)
    
    @staticmethod
    def angle_degrees(vec1: Vector2, vec2: Vector2) -> float:
        return m.degrees(m.atan2(vec2.y - vec1.y, vec2.x - vec1.x))
    
    @staticmethod
    def normaliseVector(vector: Vector2) -> None:
        temp = vector
        return temp.Normalise()
    
    @staticmethod
    def clamp(value: float, minValue: float, maxValue: float) -> float:
        return min(maxValue, max(minValue, value))
    
    @staticmethod
    def EqApprox(a: float, b: float) -> bool:
        return abs(a - b) < math.DistanceThreshhold
    
    @staticmethod
    def EqApproxVec(a: Vector2, b: Vector2) -> bool:
        return (a.x - b.x)**2 + (a.y - b.y)**2 < math.DistanceThreshhold ** 2