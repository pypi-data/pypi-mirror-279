from pyphy.boundingbox import AABB
from pyphy.vector2 import Vector2
from pyphy.pyphymath import math
from pyphy.body import Body

class Collisions:

    @staticmethod
    def IntersectAABB(a: AABB, b: AABB) -> bool:
        if a.maxVector.x <= b.minVector.x or b.maxVector.x <= a.minVector.x:
            return False
        if a.maxVector.y <= b.minVector.y or b.maxVector.y <= a.minVector.y:
            return False
        return True

    @staticmethod
    def FindContactPoints(bodyA: Body, bodyB: Body) -> tuple[Vector2, Vector2, int]:
        contact1 = Vector2.zero()
        contact2 = Vector2.zero()
        contactCount = 0
        
        if bodyA.shape == Body.BOX:
            if bodyB.shape == Body.BOX:
                contact1, contact2, contactCount = Collisions.FindContactPointsPolygon(bodyA.getTransformedVertices(), bodyB.getTransformedVertices())
            elif bodyB.shape == Body.CIRCLE:
                contact1 = Collisions.FindContactPointCirclePolygon(bodyB.position, bodyB.radius, bodyA.position, bodyA.getTransformedVertices())
                contactCount = 1

        elif bodyA.shape == Body.CIRCLE:
            if bodyB.shape == Body.BOX:
                contact1 = Collisions.FindContactPointCirclePolygon(bodyA.position, bodyA.radius, bodyB.position, bodyB.getTransformedVertices())
                contactCount = 1
            elif bodyB.shape == Body.CIRCLE:
                contact1 = Collisions.FindContactPointCircles(bodyA.position, bodyA.radius, bodyB.position)
                contactCount = 1

        return contact1, contact2, contactCount
    
    @staticmethod
    def FindContactPointsPolygon(verticesA: list[Vector2], verticesB: list[Vector2]) -> tuple[Vector2, Vector2, int]:
        contact1 = Vector2.zero()
        contact2 = Vector2.zero()
        contactCount = 0
        minDist = float('inf')

        for p in verticesA:
            for j, va in enumerate(verticesB):
                vb = verticesB[(j + 1)%len(verticesB)]

                dist, cp = Collisions.PointSegmentDistance(p, va, vb)

                if math.EqApprox(dist, minDist) and not math.EqApproxVec(cp, contact1):
                    contact2 = cp
                    contactCount = 2

                elif dist < minDist:
                    minDist = dist
                    contact1 = cp
                    contactCount = 1

        for p in verticesB:
            for j, va in enumerate(verticesA):
                vb = verticesA[(j + 1)%len(verticesA)]

                dist, cp = Collisions.PointSegmentDistance(p, va, vb)

                if math.EqApprox(dist, minDist) and not math.EqApproxVec(cp, contact1):
                    contact2 = cp
                    contactCount = 2

                elif dist < minDist:
                    minDist = dist
                    contact1 = cp
                    contactCount = 1

        return contact1, contact2, contactCount
    
    @staticmethod
    def FindContactPointCirclePolygon(circleCenter: Vector2, radius: float, polyCenter: Vector2, vertices: list[Vector2]) -> Vector2:
        minDist = float('inf')

        for i, va in enumerate(vertices):
            vb = vertices[(i+1)%len(vertices)]
            dist, contact = Collisions.PointSegmentDistance(circleCenter, va, vb)
            if dist < minDist:
                minDist = dist
                cp = contact

        return cp

    @staticmethod
    def FindContactPointCircles(centerA: Vector2, radiusA: float, centerB: Vector2) -> Vector2:
        direction = centerB - centerA
        direction.Normalise()

        return centerA + direction * radiusA
    
    @staticmethod
    def PointSegmentDistance(p: Vector2, a: Vector2, b: Vector2) -> tuple[float, Vector2]:
        ab = b - a
        ap = p - a
        proj = ap.dot(ab)
        abLenSq = ab.x ** 2 + ab.y ** 2
        d = proj / abLenSq

        if d < 0:
            cp = a
        elif d >= 1:
            cp = b
        else:
            cp = a + ab * d
        
        return (p.x - cp.x) ** 2 + (p.y - cp.y) ** 2, cp
    
    @staticmethod
    def Collide(bodyA: Body, bodyB: Body) -> tuple[bool, Vector2, float]:
        normal = Vector2.zero()
        depth = 0

        if bodyA.shape == Body.BOX:
            if bodyB.shape == Body.BOX:
                return Collisions.IntersectPolygons(bodyA.getTransformedVertices(), bodyA.position, bodyB.getTransformedVertices(), bodyB.position)
            elif bodyB.shape == Body.CIRCLE:
                c, normal, depth = Collisions.IntersectCirclePolygon(bodyB.position, bodyB.radius, bodyA.getTransformedVertices(), bodyA.position)
                return c, -normal, depth

        elif bodyA.shape == Body.CIRCLE:
            if bodyB.shape == Body.BOX:
                return Collisions.IntersectCirclePolygon(bodyA.position, bodyA.radius, bodyB.getTransformedVertices(), bodyB.position)
            elif bodyB.shape == Body.CIRCLE:
                return Collisions.IntersectCircles(bodyA, bodyB)

        return False, normal, depth

    @staticmethod
    def IntersectCircles(a: Body.CIRCLE, b: Body.CIRCLE) -> bool:
        normal = Vector2.zero()
        depth = 0

        distance = math.distance(a.position, b.position)
        radii = a.radius + b.radius
        collided = distance < radii

        if not collided:
            return False, normal, depth
        
        normal = b.position - a.position
        normal.Normalise()
        if distance > 0:
            depth = radii / distance
        else:
            depth = radii

        return collided, normal, depth
    
    @staticmethod
    def findClosestPointPolygon(center: Vector2, vertices: list[Vector2]) -> int:
        result = -1
        minDistance = float('inf')

        for vertex in vertices:
            distance = math.distance(vertex, center)
            if distance < minDistance:
                minDistance = distance
                result = vertices.index(vertex)

        return result
    
    @staticmethod
    def projectVertices(vertices: list[Vector2], axis: Vector2) -> tuple[float, float]:
        minimum = float('inf')
        maximum = float('-inf')

        for vertex in vertices:
            proj = vertex.dot(axis)

            minimum = min(proj, minimum)
            maximum = max(proj, maximum)
        
        return minimum, maximum
    
    @staticmethod
    def projectCircle(center: Vector2, radius: float, axis: Vector2) -> tuple[float, float]:
        direction = math.normaliseVector(axis)
        directionAndRadius = direction * radius

        p1 = center + directionAndRadius
        p2 = center - directionAndRadius

        minimum = p1.dot(axis)
        maximum = p2.dot(axis)

        if minimum > maximum:
            minimum, maximum = maximum, minimum

        return minimum, maximum

    @staticmethod
    def IntersectPolygons(verticesA: list[Vector2], centerA: Vector2, verticesB: list[Vector2], centerB: Vector2) -> bool:
        normal = Vector2.zero()
        depth = float('inf')

        for i, va in enumerate(verticesA):
            vb = verticesA[(i+1)%len(verticesA)]

            edge = vb - va
            axis = Vector2(-edge.y, edge.x)
            axis.Normalise()

            minA, maxA = Collisions.projectVertices(verticesA, axis)
            minB, maxB = Collisions.projectVertices(verticesB, axis)

            if minA >= maxB or minB >= maxA:
                return False, normal, depth
            
            axisDepth = min(maxB - minA, maxA - minB)
            if axisDepth < depth:
                depth = axisDepth
                normal = axis
            
        for i, va in enumerate(verticesB):
            vb = verticesB[(i+1)%len(verticesB)]

            edge = vb - va
            axis = Vector2(-edge.y, edge.x)
            axis.Normalise()

            minB, maxB = Collisions.projectVertices(verticesB, axis)
            minA, maxA = Collisions.projectVertices(verticesA, axis)

            if minA >= maxB or minB >= maxA:
                return False, normal, depth
            
            axisDepth = min(maxB - minA, maxA - minB)
            if axisDepth < depth:
                depth = axisDepth
                normal = axis

        direction = centerB - centerA

        if direction.dot(normal) < 0:
            normal = -normal

        return True, normal, depth
    
    @staticmethod
    def IntersectCirclePolygon(centerCircle: Vector2, radius: float, vertices: list[Vector2], centerPolygon: Vector2):
        normal = Vector2.zero()
        axis = Vector2.zero()
        depth = float('inf')

        for i, va in enumerate(vertices):
            vb = vertices[(i+1)%len(vertices)]

            edge = vb - va
            axis = Vector2(-edge.y, edge.x)
            axis.Normalise()

            minA, maxA = Collisions.projectVertices(vertices, axis)
            minB, maxB = Collisions.projectCircle(centerCircle, radius, axis)

            if minA >= maxB or minB >= maxA:
                return False, normal, depth
            
            axisDepth = min(maxB - minA, maxA - minB)
            if axisDepth < depth:
                depth = axisDepth
                normal = axis

        cpIndex = Collisions.findClosestPointPolygon(centerCircle, vertices)
        cp = vertices[cpIndex]

        axis = cp - centerCircle
        axis.Normalise()

        minA, maxA = Collisions.projectVertices(vertices, axis)
        minB, maxB = Collisions.projectCircle(centerCircle, radius, axis)

        if minA >= maxB or minB >= maxA:
            return False, normal, depth
        
        axisDepth = min(maxB - minA, maxA - minB)
        if axisDepth < depth:
            depth = axisDepth
            normal = axis

        direction = centerPolygon - centerCircle

        if direction.dot(normal) < 0:
            normal = -normal

        return True, normal, depth