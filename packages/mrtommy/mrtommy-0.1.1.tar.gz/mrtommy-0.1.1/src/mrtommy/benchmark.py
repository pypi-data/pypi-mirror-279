import itertools as it
import os
import time
from typing import Callable, List, Optional, Type

import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

from mrtommy.geometry import Point2D
from mrtommy.scene import Scene
from mrtommy.solver import Solver
from mrtommy.utilities import distance


def total_length(path: Optional[list[list[Point2D]]]):
    if path is None:
        return 0

    length = 0
    for i in range(len(path) - 1):
        length += distance(path[i], path[i + 1])
    return length


def run_solver(
    solver_class: Type[Solver],
    options: dict[str, list],
    scene: Scene,
    filename: Optional[
        Callable[
            [
                int,
                Solver,
            ],
            str,
        ]
    ] = None,
):
    items = options.items()
    keys = [item[0] for item in items]
    values = [item[1] for item in items]

    results = pd.DataFrame(columns=["time", "success", "length"] + keys)

    for i, option_values in tqdm(list(enumerate(it.product(*values)))):
        solver_options = {keys[i]: option_values[i] for i in range(len(keys))}
        solver = solver_class(**solver_options)

        start = time.time()
        solution = solver.solve(scene)
        execution_time = time.time() - start

        success = solver.check(scene, solution)
        length = total_length(solution)
        results.loc[i] = [execution_time, success, length] + list(
            map(str, option_values)
        )

        if not filename:
            f = f"./results/{solver_class.__name__}-{'-'.join(map(str, option_values))}.png"
        else:
            f = filename(i, solver)

        solver.plot(
            scene,
            paths=solution,
            filename=f,
        )

    results.to_csv(f"./results/{solver_class.__name__}.csv")


def plot_results(
    result_filename: str,
    y_variable: str,
    x_variable: str,
    other_variable_values: dict[str, str],
    filename: Optional[str] = None,
    display=False,
):
    df = pd.read_csv(result_filename)
    for key in other_variable_values:
        df = df.loc[(df[key] == other_variable_values[key])]

    plt.clf()
    plt.plot(df[x_variable].to_numpy(), df[y_variable].to_numpy())
    plt.title(result_filename.split("/")[-1].split(".")[0])
    plt.xlabel(x_variable)
    plt.ylabel(y_variable)

    if filename is not None:
        plt.savefig(filename)
    if display:
        plt.show()


def plot_results_comparison(
    result_filenames: List[str],
    filename: Optional[str] = None,
    display=False,
):
    plt.clf()
    for f in result_filenames:
        if not f.endswith(".csv"):
            continue

        df = pd.read_csv(f)
        df = df.loc[df["success"]]
        df = df.loc[df["length"] < 100]
        df = df.loc[df["time"] < 100]
        xs = df["time"].to_numpy()
        ys = df["length"].to_numpy()
        plt.scatter(xs, ys, label=os.path.basename(f).split(".")[0])
    plt.legend(loc="upper right")

    if filename is not None:
        plt.savefig(filename)
    if display:
        plt.show()
