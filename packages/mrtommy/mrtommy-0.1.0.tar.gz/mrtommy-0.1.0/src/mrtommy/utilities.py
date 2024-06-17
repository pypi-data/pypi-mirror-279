from mrtommy.geometry import Point2D


def distance(positions1: list[Point2D], positions2: list[Point2D]):
    return sum([p1.distance(p2) for p1, p2 in zip(positions1, positions2)])


def nearest_neighbors(
    x: list[Point2D], locations: list[list[Point2D]], k: int
):
    neighbors = sorted(
        locations,
        key=lambda location: distance(x, location),
    )
    return neighbors[:k]
