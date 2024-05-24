import random
import math
import os
import json

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
        self, temperature=1.0, cooling_rate=0.98, max_iterations=1000
    ):
        positions = self.random_positions()
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
        print(f"Cost: {self.best_cost}")
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

        annealing_position, best_cost, iterations = self.simulated_annealing(
            temperature, cooling_rate, max_iterations
        )

        if print_results:
            self.print_results()

        self.save_positions_to_json(annealing_position)

    def run_annealing_multiple(
        self,
        number_of_iterations=25,
        grid_size=None,
        temperature=1.0,
        cooling_rate=0.98,
        max_iterations_annealing=1000,
    ):
        if grid_size is not None:
            self.grid_size = grid_size

        self.costs = []

        for _ in range(number_of_iterations):
            _, best_cost, _ = self.simulated_annealing(
                temperature, cooling_rate, max_iterations_annealing
            )

            self.costs.append(best_cost)

        self.cost_mean = sum(self.costs) / number_of_iterations
        return self.costs
