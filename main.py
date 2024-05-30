from show_3d import show_from_files
from simulated_annealing_2d import SimulatedAnnealing2D

if __name__ == "__main__":

    # Enter the filenames of the txt files with the locations of the queens to show
    queens_filenames_txt = [
        "3_queens.txt",
        "4_queens.txt",
        "5_queens.txt",
        "6_queens.txt",
    ]

    show_from_files(queens_filenames_txt, labels=False)

    # ----------------------------

    # Simulated annealing

    simulated_annealing = SimulatedAnnealing2D()

    mean_cost = simulated_annealing.run_annealing_multiple(
        number_of_iterations=200,
        grid_size=6,
        starting_temperature=1,
        cooling_rate=0.99,
        annealing_max_iterations=1000,
    )

    print("--------------------")
    print(f"Mean cost: {mean_cost}")

    simulated_annealing.run_single_annealing(grid_size=6, show_results=True)
    simulated_annealing.run_multiple_annealings_and_plot(type="grid size")
    simulated_annealing.run_multiple_annealings_and_plot(type="cooling rate")
    simulated_annealing.run_multiple_annealings_and_plot(type="temperature")
