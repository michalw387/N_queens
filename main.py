from fileinput import filename
from numpy import save
from simulated_annealing_2d import SimulatedAnnealing2D
from show_3d import show_in_3d, show_from_files


if __name__ == "__main__":

    simulated_annealing = SimulatedAnnealing2D()

    simulated_annealing.execute(
        grid_size=8, temperature=1, cooling_rate=0.99, max_iterations=1000
    )

    simulated_annealing.print_results()

    filename = f"{simulated_annealing.grid_size}_queens_annealing.json"

    show_from_files([filename], dim=2)
