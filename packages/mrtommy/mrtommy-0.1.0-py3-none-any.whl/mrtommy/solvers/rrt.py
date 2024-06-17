import networkx as nx

from mrtommy.scene import Point2D, Scene
from mrtommy.solver import Solver
from mrtommy.utilities import distance


class RRTSolver(Solver):
    def __init__(self, max_iterations: int, max_distance: float):
        self.max_iterations = max_iterations
        self.max_distance = max_distance

    def move(self, start: Point2D, end: Point2D, max_distance: float):
        if start.distance(end) <= max_distance:
            return end

        difference = (end - start).normalized()

        return Point2D(
            start.x + difference.x * max_distance,
            start.y + difference.y * max_distance,
        )

    def get_position(self, scene: Scene):
        return scene.get_random_positions()

    def solve(self, scene):
        self.roadmap = nx.Graph()
        start = tuple(scene.start)
        end = tuple(scene.end)

        self.roadmap.add_node(start)

        for _ in range(self.max_iterations):
            positions = self.get_position(scene)

            closest = min(
                self.roadmap.nodes,
                key=lambda n: distance(positions, n),
            )
            positions = [
                self.move(c, p, self.max_distance)
                for c, p in zip(closest, positions)
            ]

            if not scene.check_edge(closest, positions):
                continue

            # make positions hashable
            positions = tuple(positions)

            self.roadmap.add_node(positions)
            self.roadmap.add_edge(
                closest, positions, weight=distance(closest, positions)
            )

        self.roadmap.add_node(end)
        for positions in self.roadmap.nodes:
            if scene.check_edge(positions, end):
                self.roadmap.add_edge(
                    positions, end, weight=distance(positions, end)
                )

        if not nx.algorithms.has_path(self.roadmap, start, end):
            return None

        return nx.algorithms.shortest_path(
            self.roadmap, start, end, weight="weight"
        )

    def __repr__(self):
        return f"RRT with iterations={self.max_iterations} and η={self.max_distance}"
