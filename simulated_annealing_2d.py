import random
import math
import os
import json
import numpy as np
import matplotlib.pyplot as plt

from show_3d import show_from_files


DEFAULT_GRID_SIZE = 8


class SimulatedAnnealing2D:

    def __init__(self, grid_size=DEFAULT_GRID_SIZE):
        self.grid_size = grid_size

    def random_positions(self):
        return random.sample(range(1, self.grid_size + 1), self.grid_size)

    def cost(self, positions):
        cost = 0
        for i in range(self.grid_size):
            for j in range(i + 1, self.grid_size):
                if (
                    positions[i] == positions[j]
                    or abs(positions[i] - positions[j]) == j - i
                ):
                    cost += 1
        return cost

    def generate_different_indexes(self):
        i, j = 0, 0

        while i == j:
            i = random.randint(0, self.grid_size - 1)
            j = random.randint(0, self.grid_size - 1)

        return i, j

    def simulated_annealing(
        self,
        temperature=1.0,
        cooling_rate=0.98,
        max_iterations=1000,
        starting_position=None,
    ):
        positions = (
            self.random_positions() if starting_position is None else starting_position
        )
        best_positions = positions
        best_cost = self.cost(positions)

        iterations = 0

        while temperature > 0.1 and iterations < max_iterations:
            new_positions = positions.copy()

            i, j = self.generate_different_indexes()

            new_positions[i], new_positions[j] = new_positions[j], new_positions[i]
            new_cost = self.cost(new_positions)

            if new_cost < best_cost:
                best_positions = new_positions
                best_cost = new_cost

            if new_cost < self.cost(positions):
                positions = new_positions
            elif random.random() < pow(
                math.e, (self.cost(positions) - new_cost) / temperature
            ):
                positions = new_positions

            temperature *= cooling_rate
            iterations += 1

        self.best_positions = best_positions
        self.best_cost = best_cost
        self.iterations = iterations

        return best_positions, best_cost, iterations

    def generate_array(self, positions):
        array = []
        for i in range(self.grid_size):
            row = [0] * self.grid_size
            row[positions[i] - 1] = 1
            array.append(row)
        return array

    def save_positions_to_json(self, positions, filename=None):
        if filename is None:
            filename = f"{self.grid_size}_queens_annealing.json"
        file_path = os.path.dirname(__file__) + f"\\locations_files\\2D\\{filename}"

        positions = self.generate_array(positions)

        with open(file_path, "w") as file:
            json.dump(positions, file)

    def print_results(self):
        print(f"Positions: {self.best_positions}")
        print(f"Cost (number of conflicts): {self.best_cost} ")
        print(f"Number of iterations: {self.iterations}")

    def run_annealing_and_save(
        self,
        grid_size=None,
        temperature=1.0,
        cooling_rate=0.98,
        max_iterations=1000,
        print_results=False,
    ):
        if grid_size is not None:
            self.grid_size = grid_size

        annealing_position, _, _ = self.simulated_annealing(
            temperature, cooling_rate, max_iterations
        )

        if print_results:
            self.print_results()

        self.save_positions_to_json(annealing_position)

    def run_annealing_multiple(
        self,
        number_of_iterations=25,
        grid_size=None,
        starting_temperature=1.0,
        cooling_rate=0.98,
        annealing_max_iterations=1000,
    ):
        if grid_size is not None:
            self.grid_size = grid_size

        self.costs = []

        positions = self.random_positions()

        for _ in range(number_of_iterations):
            _, best_cost, _ = self.simulated_annealing(
                starting_temperature, cooling_rate, annealing_max_iterations, positions
            )

            self.costs.append(best_cost)

        self.cost_mean = sum(self.costs) / number_of_iterations
        return self.cost_mean

    def run_single_annealing(
        self,
        grid_size=10,
        temperature=1,
        cooling_rate=0.99,
        max_iterations=1000,
        show_results=False,
    ):
        simulated_annealing = SimulatedAnnealing2D()

        simulated_annealing.run_annealing_and_save(
            grid_size, temperature, cooling_rate, max_iterations
        )

        if show_results:
            print("--------------------")
            print("Results for single annealing:")
            simulated_annealing.print_results()

            filename = f"{simulated_annealing.grid_size}_queens_annealing.json"

            show_from_files([filename], dim=2)
            print("--------------------")

        return simulated_annealing.best_cost, simulated_annealing.iterations

    def run_multiple_annealings_and_plot(
        self,
        type="cooling_rate",
        grid_size=8,
        repeat_iterations=200,
        temperature=1,
        cooling_rate=0.99,
        max_iterations=1000,
    ):

        simulated_annealing = SimulatedAnnealing2D()

        mean_costs = []

        if type == "cooling rate":
            cooling_rates = np.arange(0.8, 0.99, 0.01)

            for cr in cooling_rates:
                simulated_annealing.run_annealing_multiple(
                    number_of_iterations=repeat_iterations,
                    grid_size=grid_size,
                    starting_temperature=temperature,
                    cooling_rate=cr,
                    annealing_max_iterations=max_iterations,
                )
                mean_costs.append(simulated_annealing.cost_mean)

            self.plot_costs(cooling_rates, mean_costs, type)

        if type == "temperature":
            temperatures = np.arange(1, 10, 0.5)

            for temp in temperatures:
                simulated_annealing.run_annealing_multiple(
                    number_of_iterations=repeat_iterations,
                    grid_size=grid_size,
                    starting_temperature=temp,
                    cooling_rate=cooling_rate,
                    annealing_max_iterations=max_iterations,
                )
                mean_costs.append(simulated_annealing.cost_mean)

            self.plot_costs(temperatures, mean_costs, type)

        if type == "grid size":
            grid_sizes = np.arange(4, 11, 1)

            for grid_size in grid_sizes:
                simulated_annealing.run_annealing_multiple(
                    number_of_iterations=repeat_iterations,
                    grid_size=grid_size,
                    starting_temperature=temperature,
                    cooling_rate=cooling_rate,
                    annealing_max_iterations=max_iterations,
                )
                mean_costs.append(simulated_annealing.cost_mean)

            self.plot_costs(grid_sizes, mean_costs, type)

        return mean_costs

    @staticmethod
    def plot_costs(x, y, title):
        plt.plot(x, y)
        plt.xlabel(title)
        plt.ylabel("Mean costs")
        plt.title(f"Mean cost for different {title}")
        plt.grid()
        plt.show()
