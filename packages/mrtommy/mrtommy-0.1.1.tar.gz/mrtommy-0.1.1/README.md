<h1 align="center">
    🤖 Mr. Tommy
    <br />
    <a href="https://rye.astral.sh">
        <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/rye/main/artwork/badge.json" alt="Rye">
    </a>
    <a href="https://github.com/astral-sh/ruff">
        <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
    </a>
</h1>
<p align="center">
    <b>Multi-Robot Trajectory Organization and Motion Modeling Yard</b>
</p>

Tommy is a Python library that aims to speed up the development and experimentation of motion planning.
Among the goals of Tommy are:

-   Easy to work with (typing) and extend.
-   Easy to experiment with (matplotlib and notebook workflow).
-   Comparable performance.

Tommy was developed as part of the [Algorithmic Robotics and Motion Planning](https://www.cgl.cs.tau.ac.il/courses/algorithmic-robotics-and-motion-planning-fall-2023-2024/) course given in Tel Aviv University by Prof. Dan Halperin.

## Getting Started

Install the dependencies with `pip install numpy networkx matplotlib tqdm pandas`, or use Rye.

Uncomment pieces of code inside the [main](src/mrtommy/__main__.py), add the necessary imports, then run `python3 -m mrtommy` from inside `src`.

## Acknowledgements

Mr. Tommy is **heavily** inspired by [discopygal](https://www.cs.tau.ac.il/~cgl/discopygal/docs/index.html), although it aims to provide a different experience.
