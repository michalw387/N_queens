from fileinput import filename
from numpy import save
from simulated_annealing_2d import simulated_annealing, save_positions_to_json
from show_3d import show_in_3d, show_from_files


if __name__ == "__main__":
    positions, cost, iterations = simulated_annealing(
        temperature=1.0, cooling_rate=0.98, max_iterations=1000
    )

    save_positions_to_json(positions)

    filename = f"{len(positions)}_queens_annealing.json"

    show_from_files([filename], labels=True, dim=2)
