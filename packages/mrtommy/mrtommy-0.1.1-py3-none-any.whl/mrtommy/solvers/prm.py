import networkx as nx

from mrtommy.solver import Solver
from mrtommy.utilities import distance, nearest_neighbors


class PRMSolver(Solver):
    def __init__(self, landmarks: int, k: int):
        self.landmarks = landmarks
        self.k = k

    def solve(self, scene):
        self.roadmap = nx.Graph()

        start = tuple(scene.start)
        end = tuple(scene.end)

        self.roadmap.add_node(start)
        self.roadmap.add_node(end)

        for _ in range(self.landmarks):
            self.roadmap.add_node(tuple(scene.get_random_valid_positions()))

        for v in self.roadmap.nodes:
            for neighbor in nearest_neighbors(v, self.roadmap.nodes, self.k):
                if scene.check_edge(v, neighbor):
                    self.roadmap.add_edge(
                        v, neighbor, weight=distance(v, neighbor)
                    )

        if not nx.algorithms.has_path(self.roadmap, start, end):
            return None

        return nx.algorithms.shortest_path(
            self.roadmap, start, end, weight="weight"
        )

    def __repr__(self):
        return f"PRM with landmarks={self.landmarks} and k={self.k}"
