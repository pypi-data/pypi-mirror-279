import networkx as nx

from mrtommy.geometry import Point2D
from mrtommy.scene import Scene
from mrtommy.solvers.rrt import RRTSolver
from mrtommy.utilities import distance


class RRTStarSolver(RRTSolver):
    def __init__(
        self, max_iterations: int, max_distance: float, radius: float
    ):
        self.radius = radius
        super().__init__(max_iterations, max_distance)

    def solve(self, scene: Scene) -> list[list[Point2D]]:
        self.roadmap = nx.Graph()
        start = tuple(scene.start)
        self.roadmap.add_node(start, cost=0, parent=start)

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
            cost = self.roadmap.nodes[closest]["cost"] + distance(
                closest, positions
            )

            self.roadmap.add_node(positions, cost=cost, parent=closest)
            self.roadmap.add_edge(
                closest, positions, weight=distance(closest, positions)
            )

            neighbors = nx.ego_graph(
                self.roadmap, positions, self.radius, distance="weight"
            )
            for neighbor in neighbors.nodes:
                neighbor_distance = distance(neighbor, positions)
                neighbor_cost = (
                    self.roadmap.nodes[neighbor]["cost"] + neighbor_distance
                )
                if neighbor_cost < cost:
                    if not scene.check_edge(neighbor, positions):
                        continue
                    cost = neighbor_cost
                    self.roadmap.remove_edge(closest, positions)
                    self.roadmap.add_edge(
                        neighbor, positions, weight=neighbor_distance
                    )
                    self.roadmap.nodes[positions]["parent"] = neighbor
                    closest = neighbor

            for neighbor in neighbors.nodes:
                neighbor_distance = distance(positions, neighbor)
                new_cost = cost + neighbor_distance
                if new_cost < self.roadmap.nodes[neighbor]["cost"]:
                    if not scene.check_edge(neighbor, positions):
                        continue
                    self.roadmap.nodes[neighbor]["cost"] = new_cost
                    self.roadmap.nodes[neighbor]["parent"] = positions
                    self.roadmap.add_edge(
                        positions, neighbor, weight=neighbor_distance
                    )
                    self.roadmap.remove_edge(
                        self.roadmap.nodes[neighbor]["parent"], neighbor
                    )

        end = tuple(scene.end)
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
        return f"RRT* with iterations={self.max_iterations}, η={self.max_distance} and radius={self.radius}"
