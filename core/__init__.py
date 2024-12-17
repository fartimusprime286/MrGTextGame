import math
from enum import Enum
from typing import Self


class Color:
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    def to_foreground_color(self):
        if self == NONE_COLOR:
            return ""

        return f"\x1b[38;2;{self.r};{self.g};{self.b}m"

    def to_background_color(self):
        if self == NONE_COLOR:
            return ""

        return f"\x1b[48;2;{self.r};{self.g};{self.b}m"

    def with_background_color(self, bg: Self):
        if self == NONE_COLOR and bg == NONE_COLOR:
            return ""
        elif self == NONE_COLOR:
            return bg.to_background_color()
        elif bg == NONE_COLOR:
            return self.to_foreground_color()
        else:
            return f"\x1b[38;2;{self.r};{self.g};{self.b};48;2;{bg.r};{bg.g};{bg.b}m"

    def mode_reliant(self, color_mode: str):
        if color_mode == "foreground":
            return self.to_foreground_color()
        elif color_mode == "background":
            return self.to_background_color()
        else:
            raise ValueError("color_mode must be either foreground or background.")

    @staticmethod
    def reset_string():
        return "\x1b[39;49m"

    def __eq__(self, other: Self):
        return self.r == other.r and self.g == other.g and self.b == other.b

    def __hash__(self):
        return hash((self.r, self.g, self.b))

    def __str__(self):
        return f"TrueColor24Bit({self.r}, {self.g}, {self.b})"

NONE_COLOR = Color(-1, -1, -1)

class DefaultColors(Enum):
    NONE = NONE_COLOR
    BLACK = Color(0, 0, 0)
    WHITE = Color(255, 255, 255)
    RED = Color(255, 0, 0)
    BLUE = Color(0, 0, 255)

class Vec2:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def is_zero(self):
        return self.magnitude() == 0

    def normalized(self):
        magnitude = self.magnitude()
        if magnitude == 0:
            return Vec2(self.x, self.y)

        return Vec2(self.x / magnitude, self.y / magnitude)

    def is_horizontal(self):
        return self.x > self.y

    def is_vertical(self):
        return self.y > self.x

    def magnitude(self) -> float:
        return math.sqrt((self.x ** 2) + (self.y ** 2))

    def distance_to(self, other: Self) -> float:
        return math.sqrt(((self.x - other.x) ** 2) + ((self.y - other.y) ** 2))

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vec2(self.x * other.x, self.y * other.y)

    def __truediv__(self, other):
        return Vec2(self.x / other.x, self.y / other.y)

    def __floordiv__(self, other):
        return Vec2(self.x // other.x, self.y // other.y)

    def __mod__(self, other):
        return Vec2(self.x % other.x, self.y % other.y)

    def __pow__(self, power):
        return Vec2(self.x ** power.x, self.y ** power.y)

    def __lt__(self, other):
        return self.magnitude() < other.magnitude()

    def __le__(self, other):
        return self.magnitude() <= other.magnitude()

    def __gt__(self, other):
        return self.magnitude() > other.magnitude()

    def __ge__(self, other):
        return self.magnitude() >= other.magnitude()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"Vec2({self.x}, {self.y})"

class Direction(Enum):
    UP = Vec2(0, -1)
    DOWN = Vec2(0, 1)
    LEFT = Vec2(-1, 0)
    RIGHT = Vec2(1, 0)

    def raycast_pos(self, pos: Vec2, size: Vec2) -> Vec2:
        match self:
            case Direction.UP:
                return pos + Vec2(size.x / 2, -0.1)
            case Direction.DOWN:
                return pos + Vec2(size.x / 2, size.y + 0.1)
            case Direction.LEFT:
                return pos + Vec2(-0.1, size.y / 2)
            case Direction.RIGHT:
                return pos + Vec2(size.x, size.y / 2)

class BoundingBox:
    def __init__(self, min_pos: Vec2, max_pos: Vec2):
        self._min: Vec2 = min_pos
        self._max: Vec2 = max_pos

    def is_overlapping(self, other: Self) -> bool:
        return not (self._max.x < other.min().x or self._min.x > other.max().x or self._max.y < other.min().y or self._min.y > other.max().y)

    def min(self) -> Vec2:
        return self._min

    def max(self) -> Vec2:
        return self._max


def clamp(n, n_min, n_max):
    if n < n_min:
        return n_min
    elif n > n_max:
        return n_max
    else:
        return n
