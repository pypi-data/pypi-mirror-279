import itertools as it
import json
import math
import random
from typing import List

from mrtommy.geometry import Point2D, Segment2D


class ObstacleDisc:
    """A disc which robots can't intersect with."""

    location: Point2D
    radius: float

    def __init__(self, location: Point2D, radius: float):
        self.location = location
        self.radius = radius


class RobotDisc:
    """A disc robot which must go from start to end."""

    start: Point2D
    end: Point2D
    radius: float

    def __init__(self, start: Point2D, end: Point2D, radius: float):
        self.start = start
        self.end = end
        self.radius = radius


class Scene:
    """
    Main class to hold Scene information.
    A motion planning scene is a set of robots which need to get from start to end in a
    path of straight lines without intersecting any of the obstacles.
    """

    robots: List[RobotDisc]
    obstacles: List[ObstacleDisc]
    x_min: float
    x_max: float
    y_min: float
    y_max: float

    def __init__(self, robots: list[RobotDisc], obstacles: list[ObstacleDisc]):
        """Initialize a scene from a JSON file containing its information. See the scene JSON schema to learn more about this format."""

        self.robots = robots
        self.obstacles = obstacles

        x_min, y_min = math.inf, math.inf
        x_max, y_max = -math.inf, -math.inf

        for robot in self.robots:
            x_min = min(
                x_min, robot.start.x - robot.radius, robot.end.x - robot.radius
            )
            y_min = min(
                y_min, robot.start.y - robot.radius, robot.end.y - robot.radius
            )
            x_max = max(
                x_max, robot.start.x + robot.radius, robot.end.x + robot.radius
            )
            y_max = max(
                y_max, robot.start.y + robot.radius, robot.end.y + robot.radius
            )

        for obstacle in self.obstacles:
            x_min = min(x_min, obstacle.location.x - obstacle.radius)
            y_min = min(y_min, obstacle.location.y - obstacle.radius)
            x_max = max(x_max, obstacle.location.x + obstacle.radius)
            y_max = max(y_max, obstacle.location.y + obstacle.radius)

        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def get_boundary(self) -> tuple[float, float, float, float]:
        """Returns x_min, x_max, y_min, y_max of the scene"""

        return self.x_min, self.x_max, self.y_min, self.y_max

    def get_random_positions(self) -> list[Point2D]:
        """Returns a random position sampled at uniform inside the boundary of the scene for each robot"""

        return [
            Point2D(
                random.uniform(self.x_min, self.x_max),
                random.uniform(self.y_min, self.y_max),
            )
            for _ in self.robots
        ]

    def check(self, positions: list[Point2D]):
        """Checks, if the robots are at the given locations (robots[i] at positions[i]), if there are any invalid intersections or not."""

        for robot, position in zip(self.robots, positions):
            for obstacle in self.obstacles:
                if (
                    position.distance(obstacle.location)
                    < obstacle.radius + robot.radius
                ):
                    return False

        for (robot1, position1), (robot2, position2) in it.combinations(
            zip(self.robots, positions), 2
        ):
            if position1.distance(position2) < robot1.radius + robot2.radius:
                return False

        return True

    def get_random_valid_positions(self) -> list[Point2D]:
        p = self.get_random_positions()
        while not self.check(p):
            p = self.get_random_positions()
        return p

    def check_edge(self, start: list[Point2D], end: list[Point2D]):
        """Checks, if the robots are at the given locations (robots[i] at positions[i]), and move in straight lines to the end locations, if there are any invalid intersections or not."""

        assert len(start) == len(end) == len(self.robots)

        for robot_index in range(len(self.robots)):
            for obstacle in self.obstacles:
                if (
                    Segment2D(start[robot_index], end[robot_index]).distance(
                        obstacle.location
                    )
                    < obstacle.radius + self.robots[robot_index].radius
                ):
                    return False

        for r1, r2 in it.combinations(range(len(self.robots)), 2):
            robot1 = self.robots[r1]
            robot2 = self.robots[r2]
            if (
                Segment2D(start[r1], end[r1]).distance(
                    Segment2D(start[r2], end[r2])
                )
                < robot1.radius + robot2.radius
            ):
                return False

        return True

    @property
    def start(self):
        return [r.start for r in self.robots]

    @property
    def end(self):
        return [r.end for r in self.robots]


def load_scene(filename: str):
    with open(filename, "r") as f:
        serialized_scene = json.load(f)

    robots = [
        RobotDisc(Point2D(*r["start"]), Point2D(*r["end"]), r["radius"])
        for r in serialized_scene["robots"]
    ]
    obstacles = [
        ObstacleDisc(Point2D(*o["location"]), o["radius"])
        for o in serialized_scene["obstacles"]
    ]

    return Scene(robots, obstacles)
