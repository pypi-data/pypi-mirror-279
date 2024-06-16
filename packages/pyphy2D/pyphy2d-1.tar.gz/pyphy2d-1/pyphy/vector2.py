class Vector2:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def Normalise(self) -> None:
        mag = self.magnitude
        if mag == 0:
            self.x, self.y = 0, 0
            return self
        self.x /= mag
        self.y /= mag
        return self

    def dot(self, other) -> float:
        return self.x * other.x + self.y * other.y

    def cross(self, other) -> float:
        return self.x * other.y - self.y * other.x

    def to_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)
    
    @property
    def magnitude(self) -> float:
        return (self.x**2 + self.y**2)**0.5
    
    @classmethod
    def from_tuple(cls, tup) -> "Vector2":
        if not isinstance(tup, tuple):
            raise TypeError(f'Invalid Input {type(tup)}')
        return Vector2(*tup)

    @classmethod
    def zero(cls) -> "Vector2":
        return Vector2(0, 0)
    
    @staticmethod
    def transform(vector, transformer) -> "Vector2":
        rx = transformer.cos * vector.x - transformer.sin * vector.y
        ry = transformer.sin * vector.x + transformer.cos * vector.y
        return Vector2(rx + transformer.position.x, ry + transformer.position.y)
    
    def __add__(self, other) -> "Vector2":
        if isinstance(other, (int, float)):
            return Vector2(self.x + other, self.y + other)
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __iadd__(self, other):
        self.x, self.y = self.x + other.x, self.y + other.y
        return self
    
    def __sub__(self, other) -> "Vector2":
        if isinstance(other, (int, float)):
            return Vector2(self.x - other, self.y - other)
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __isub__(self, other):
        if isinstance(other, (int, float)):
            self.x, self.y = self.x - other, self.y - other
            return self
        self.x, self.y = self.x - other.x, self.y - other.y
        return self
    
    def __mul__(self, scalar: float) -> "Vector2":
        return Vector2(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar: float) -> "Vector2":
        return Vector2(self.x / scalar, self.y / scalar)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Vector2):
            return False
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __str__(self) -> tuple:
        return f'Vector2({self.x}, {self.y})'
    
    def __getitem__(self, index: int) -> float:
        return (self.x, self.y)[index]
        
    def __len__(self) -> int:
        return 2
    
    def __neg__(self) -> "Vector2":
        return Vector2(-self.x, -self.y)