import math
from typing import Optional, Union

from mrtommy.constants import EPSILON


class Point2D:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance(self, other: "Point2D"):
        return (self - other).norm()

    def __mul__(self, other: "Point2D"):
        return self.x * other.x + self.y * other.y

    def __sub__(self, other: "Point2D"):
        return Point2D(self.x - other.x, self.y - other.y)

    def norm(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalized(self):
        norm = self.norm()
        return Point2D(self.x / norm, self.y / norm)


class Line2D:
    start: Point2D
    end: Point2D

    def __init__(self, start: Point2D, end: Point2D):
        self.start = start
        self.end = end

    def representation(self) -> tuple[float, float, float]:
        """Returns the a,b,c in the representation of the line as ax+by+c=0"""

        if self.start.x == self.end.x:
            return 1, 0, self.start.x

        slope = (self.end.y - self.start.y) / (self.end.x - self.start.x)
        return slope, -1, (self.start.y - slope * self.start.x)

    def distance(self, point: Point2D):
        """Returns the distance between this line and the given point"""

        a, b, c = self.representation()
        return abs(a * point.x + b * point.y + c) / math.sqrt(a * a + b * b)

    def intersection(self, other: "Line2D") -> Optional[Point2D]:
        """Returns the intersection of these two lines, or None if there isn't any"""

        a1, b1, c1 = self.representation()
        a2, b2, c2 = other.representation()

        denominator = b1 * a2 - a1 * b2
        if denominator == 0 or a1 == 0 or a2 == 0:
            return None

        numerator = a1 * c2 - c1 * a2
        y = numerator / denominator
        x = (-b1 * y - c1) / a1
        return Point2D(x, y)

    def contains(self, point: Point2D):
        """Checks whether the given point is on this line"""

        a, b, c = self.representation()
        return abs(a * point.x + b * point.y + c) < EPSILON

    def perpendicular(self, point: Point2D):
        """Returns the line perpendicular to this line passing at the given point"""

        a, b, c = self.representation()
        offset = a * point.y - b * point.x
        return line_from_representation(b, -a, offset)

    def __eq__(self, other: "Line2D"):
        return self.representation() == other.representation()


def line_from_representation(a: float, b: float, c: float) -> Line2D:
    """Initializes the line from the given ax+by+c=0 representation"""

    if a == 0:
        return Line2D(Point2D(0, -c / b), Point2D(1, -c / b))

    if b == 0:
        return Line2D(Point2D(-c / a, 0), Point2D(-c / a, 1))

    return Line2D(Point2D(1, -(a + c) / b), Point2D(0, -c / b))


class Segment2D:
    start: Point2D
    end: Point2D

    def __init__(self, start: Point2D, end: Point2D):
        self.start = start
        self.end = end

    def line(self):
        return Line2D(self.start, self.end)

    def length(self):
        return (self.end - self.start).norm()

    def contains(self, point: Point2D):
        """Checks whether the given point is inside this segment"""

        if not self.line().contains(point):
            return False

        dot_product = (point - self.start) * (self.end - self.start)
        if dot_product < 0 or dot_product > self.length() ** 2:
            return False

        return True

    def intersection(
        self, other: Union[Line2D, "Segment2D"]
    ) -> Optional[Point2D]:
        if isinstance(other, Segment2D):
            p = self.line().intersection(other.line())
            if p is not None and self.contains(p) and other.contains(p):
                return p
            return None

        assert isinstance(other, Line2D)
        p = self.line().intersection(other)
        if p is not None and self.contains(p):
            return p
        return None

    def distance(self, other: Union[Point2D, Line2D, "Segment2D"]):
        """Returns the distance between this segment and the given object"""

        if isinstance(other, Point2D):
            closest = self.intersection(self.line().perpendicular(other))
            if closest is not None:
                return closest.distance(other)

            return min(
                self.start.distance(other),
                self.end.distance(other),
            )

        if isinstance(other, Segment2D):
            if self.intersection(other) is not None:
                return 0

            return min(
                self.distance(other.start),
                self.distance(other.end),
                other.distance(self.start),
                other.distance(self.end),
            )

        assert isinstance(other, Line2D)
        if self.intersection(other) is not None:
            return 0
        return min(other.distance(self.start), other.distance(self.end))
