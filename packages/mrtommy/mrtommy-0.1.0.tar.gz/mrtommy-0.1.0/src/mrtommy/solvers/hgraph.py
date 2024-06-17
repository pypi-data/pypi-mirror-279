import itertools as it

import networkx as nx

from mrtommy.scene import RobotDisc, Scene
from mrtommy.solver import Solver
from mrtommy.utilities import distance


class HGraphSolver(Solver):
    def __init__(
        self,
        solvers: list[Solver],
        local_solver: Solver,
        neighborhood_distance: float,
    ):
        self.solvers = solvers
        self.local_solver = local_solver
        self.neighborhood_distance = neighborhood_distance

    def solve(self, scene):
        self.roadmap = nx.Graph()
        start = tuple(scene.start)
        end = tuple(scene.end)

        paths = []
        for solver in self.solvers:
            path = solver.solve(scene)
            if path is not None:
                paths.append(path)
                for i in range(len(path) - 1):
                    self.roadmap.add_edge(path[i], path[i + 1])

        # TODO: implement All-Pairs H-Graph or Edit-Distance H-Graph
        for p1, p2 in it.combinations(paths, 2):
            for v1 in p1:
                for v2 in p2:
                    # Neighborhood
                    if distance(v1, v2) > self.neighborhood_distance:
                        continue

                    local_scene = Scene(
                        [
                            RobotDisc(start, end, robot.radius)
                            for robot, start, end in zip(scene.robots, v1, v2)
                        ],
                        scene.obstacles,
                    )
                    local_path = self.local_solver.solve(local_scene)
                    if local_path is not None:
                        for i in range(len(local_path) - 1):
                            self.roadmap.add_edge(
                                local_path[i], local_path[i + 1]
                            )

        if not nx.algorithms.has_path(self.roadmap, start, end):
            return None

        return nx.algorithms.shortest_path(
            self.roadmap, start, end, weight="weight"
        )

    def __repr__(self):
        return (
            f"HGraph with local={self.local_solver.__class__.__name__} and "
            + ", ".join([s.__class__.__name__ for s in self.solvers])
        )
