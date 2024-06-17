import itertools as it
from typing import Optional

import matplotlib.pyplot as plt
import networkx as nx

from mrtommy.scene import Point2D, Scene, Segment2D


class Solver:
    """
    A solver should be able to solve a specific Scene.
    Any subclass must override the solve function, and may set the roadmap if relevant to some graph where each vertex is a tuple of Point2D.

    The solver can also be checked and plotted using the check and plot functions accordingly.
    """

    roadmap: Optional[nx.Graph]

    def solve(self, scene: Scene) -> Optional[list[list[Point2D]]]:
        """
        Solves the motion planning problem by giving a list of points to travel through for each robot,
        where the robots travel in straight lines (each element is a list of Point2D for every robot)
        """
        pass

    def check(self, scene: Scene, solution: Optional[list[list[Point2D]]]):
        """Checks the given solution is valid and there are no intersections"""

        if solution is None:
            return False

        for s in solution:
            if len(scene.robots) != len(s):
                raise Exception(
                    "Each list of points in the solution must be a location for each robot!"
                )

        for robot, start in zip(scene.robots, solution[0]):
            if start != robot.start:
                return False

        for robot, end in zip(scene.robots, solution[-1]):
            if end != robot.end:
                return False

        for i in range(len(solution) - 1):
            for robot_index in range(len(scene.robots)):
                robot = scene.robots[robot_index]
                path = Segment2D(
                    solution[i][robot_index], solution[i + 1][robot_index]
                )
                for obstacle in scene.obstacles:
                    if (
                        path.distance(obstacle.location)
                        < robot.radius + obstacle.radius
                    ):
                        return False

            for r1, r2 in it.combinations(range(len(scene.robots)), 2):
                p1 = Segment2D(solution[i][r1], solution[i + 1][r2])
                p2 = Segment2D(solution[i][r1], solution[i + 1][r2])
                robot1 = scene.robots[r1]
                robot2 = scene.robots[r2]
                if p1.distance(p2) < robot1.radius + robot2.radius:
                    return False

        return True

    def solve_and_check(self, scene: Scene):
        """Solves and checks the solution of the given scene."""

        solution = self.solve(scene)
        if self.check(scene, solution):
            print("Solution is valid!")
        else:
            print("Solution invalid!")

        return solution

    def plot(
        self,
        scene: Scene,
        paths: Optional[list[list[Point2D]]] = None,
        filename: Optional[str] = None,
        display=False,
        plot_roadmap=True,
        title=True,
        robot_colors: list[str] = [
            "yellow",
            "green",
            "cyan",
            "blue",
            "indigo",
            "fuchsia",
        ],
        obstacle_color="red",
    ):
        """
        Plots the scene, and the given solution `paths` if available.

        If `display` is set, opens a matplotlib window with the plot. If `filename` is set, saves the plot to the given filename.
        """

        plt.clf()
        plt.plot(
            [scene.x_min, scene.x_max, scene.x_max, scene.x_min, scene.x_min],
            [scene.y_min, scene.y_min, scene.y_max, scene.y_max, scene.y_min],
            color="black",
        )

        for obstacle in scene.obstacles:
            circle = plt.Circle(
                (obstacle.location.x, obstacle.location.y),
                obstacle.radius,
                color=obstacle_color,
            )
            plt.gca().add_patch(circle)

        if plot_roadmap and self.roadmap is not None:
            for s, e in self.roadmap.edges:
                for p1, p2 in zip(s, e):
                    plt.plot([p1.x, p2.x], [p1.y, p2.y], color="black")

        if paths is not None:
            for robot_index in range(len(scene.robots)):
                for i in range(len(paths) - 1):
                    plt.plot(
                        [paths[i][robot_index].x, paths[i + 1][robot_index].x],
                        [paths[i][robot_index].y, paths[i + 1][robot_index].y],
                        linewidth=3,
                        color=robot_colors[robot_index],
                    )

        for index, robot in enumerate(scene.robots):
            circle = plt.Circle(
                (robot.start.x, robot.start.y),
                robot.radius,
                color=robot_colors[index],
            )
            plt.gca().add_patch(circle)
            circle = plt.Circle(
                (robot.end.x, robot.end.y),
                robot.radius,
                color=robot_colors[index],
            )
            plt.gca().add_patch(circle)

        if title:
            plt.title(str(self))

        if filename is not None:
            plt.savefig(filename)
        if display:
            plt.show()
