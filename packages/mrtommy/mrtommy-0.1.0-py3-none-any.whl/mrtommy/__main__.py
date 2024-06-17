from mrtommy.scene import load_scene

if __name__ == "__main__":
    scenes = [
        load_scene("../resources/coffee_shop.json"),
        load_scene("../resources/2_coffee_shop.json"),
        load_scene("../resources/big_coffee_shop.json"),
    ]

    # run_solver(
    #     PRMSolver,
    #     {
    #         "landmarks": range(5000, 10100, 100),
    #         "k": [5, 10, 15],
    #     },
    #     scenes[2],
    # )

    # run_solver(
    #     RRTSolver,
    #     {
    #         "max_iterations": range(3000, 7100, 100),
    #         "max_distance": [1.5],
    #     },
    #     scenes[2],
    # )

    # run_solver(
    #     RRTStarSolver,
    #     {
    #         "max_iterations": range(3000, 7100, 100),
    #         "max_distance": [1.5],
    #         "radius": [3],
    #     },
    #     scenes[2],
    # )

    # run_solver(
    #     DRRTSolver,
    #     {
    #         "prm_landmarks": [2000, 4000],
    #         "prm_k": [0],
    #         "max_iterations": range(3000, 7100, 100),
    #         "max_distance": [1.5],
    #     },
    #     scenes[2],
    # )

    # run_solver(
    #     DRRTStarSolver,
    #     {
    #         "prm_landmarks": [1000],
    #         "prm_k": [0],
    #         "max_iterations": range(3000, 7100, 100),
    #         "max_distance": [1.5],
    #         "radius": [3],
    #     },
    #     scenes[2],
    # )

    # run_solver(
    #     HGraphSolver,
    #     {
    #         "solvers": [
    #             [PRMSolver(3000, 5) for i in range(2)],
    #             [PRMSolver(3000, 5) for i in range(3)],
    #             [PRMSolver(3000, 5) for i in range(5)],
    #             [PRMSolver(3000, 5) for i in range(10)],
    #             [RRTSolver(3000, 1.5) for i in range(2)],
    #             [RRTSolver(3000, 1.5) for i in range(3)],
    #             [RRTSolver(3000, 1.5) for i in range(5)],
    #             [RRTSolver(3000, 1.5) for i in range(10)],
    #             [RRTStarSolver(3000, 0.5, i) for i in range(2)],
    #             [RRTStarSolver(3000, 0.5, i) for i in range(3)],
    #             [RRTStarSolver(3000, 0.5, i) for i in range(5)],
    #             [PRMSolver(3000, 5) for i in range(2)]
    #             + [RRTSolver(3000, 1) for i in range(2)],
    #             [PRMSolver(3000, 5) for i in range(3)]
    #             + [RRTSolver(3000, 1) for i in range(3)],
    #         ],
    #         "local_solver": [RRTSolver(60, 0.4)],
    #         "neighborhood_distance": [4],
    #     },
    #     scenes[2],
    #     filename=lambda i, solver: f"./results/HGraph-{i}.png",
    # )

    # plot_results(
    #     "./results/PRMSolver.csv",
    #     "length",
    #     "landmarks",
    #     {"k": 10},
    #     filename="plots/prm_length.png",
    # )
    # plot_results(
    #     "./results/PRMSolver.csv",
    #     "time",
    #     "landmarks",
    #     {"k": 10},
    #     filename="plots/prm_time.png",
    # )
    # plot_results(
    #     "./results/RRTSolver.csv",
    #     "length",
    #     "max_iterations",
    #     {"max_distance": 0.5},
    #     filename="plots/rrt_length.png",
    # )
    # plot_results(
    #     "./results/RRTStarSolver.csv",
    #     "length",
    #     "max_iterations",
    #     {"max_distance": 0.5, "radius": 4},
    #     filename="plots/rrtstar_length.png",
    # )
    # plot_results(
    #     "./results/DRRTSolver.csv",
    #     "length",
    #     "prm_landmarks",
    #     {"max_distance": 0.5, "prm_k": 0, "max_iterations": 2000},
    #     filename="plots/drrt_length.png",
    # )

    # plot_results_comparison(
    #     [os.path.join("results", f) for f in os.listdir("results")],
    #     filename="plots/comparison.png",
    # )
    # plot_results_comparison(
    #     [
    #         os.path.join("results-coffee", f)
    #         for f in os.listdir("results-coffee")
    #     ],
    #     filename="plots/comparison-coffee.png",
    # )
