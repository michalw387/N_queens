from fileinput import filename
from numpy import save
from simulated_annealing_2d import SimulatedAnnealing2D
from show_3d import show_in_3d, show_from_files


def run_single_annealing(
    grid_size=10,
    temperature=1,
    cooling_rate=0.99,
    max_iterations=1000,
    show_results=True,
):
    simulated_annealing = SimulatedAnnealing2D()

    simulated_annealing.run_annealing_and_save(
        grid_size, temperature, cooling_rate, max_iterations
    )

    if show_results:
        simulated_annealing.print_results()

        filename = f"{simulated_annealing.grid_size}_queens_annealing.json"

        show_from_files([filename], dim=2)

    return simulated_annealing.best_cost, simulated_annealing.iterations


if __name__ == "__main__":

    simulated_annealing = SimulatedAnnealing2D()

    simulated_annealing.run_annealing_multiple(
        number_of_iterations=25,
        grid_size=10,
        temperature=1,
        cooling_rate=0.99,
        max_iterations_annealing=1000,
    )

    print(simulated_annealing.cost_mean)
