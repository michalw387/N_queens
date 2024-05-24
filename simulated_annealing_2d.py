import random
import math
import os
import numpy as np
import json

GRID_SIZE = 8


def random_positions(grid_size=GRID_SIZE):
    return random.sample(range(1, grid_size + 1), grid_size)


def cost(positions):
    cost = 0
    for i in range(GRID_SIZE):
        for j in range(i + 1, GRID_SIZE):
            if (
                positions[i] == positions[j]
                or abs(positions[i] - positions[j]) == j - i
            ):
                cost += 1
    return cost


def generate_different_indexes():
    i, j = 0, 0

    while i == j:
        i = random.randint(0, GRID_SIZE - 1)
        j = random.randint(0, GRID_SIZE - 1)

    return i, j


def simulated_annealing(temperature=1.0, cooling_rate=0.98, max_iterations=1000):
    positions = random_positions()
    best_positions = positions
    best_cost = cost(positions)

    iterations = 0

    while temperature > 0.1 and iterations < max_iterations:
        new_positions = positions.copy()

        i, j = generate_different_indexes()

        new_positions[i], new_positions[j] = new_positions[j], new_positions[i]
        new_cost = cost(new_positions)

        if new_cost < best_cost:
            best_positions = new_positions
            best_cost = new_cost

        if new_cost < cost(positions):
            positions = new_positions
        elif random.random() < pow(math.e, (cost(positions) - new_cost) / temperature):
            positions = new_positions

        temperature *= cooling_rate
        iterations += 1

    return best_positions, best_cost, iterations


def generate_array(positions):
    array = []
    for i in range(GRID_SIZE):
        row = [0] * GRID_SIZE
        row[positions[i] - 1] = 1
        array.append(row)
    return array


def save_positions_to_json(positions, filename=f"{GRID_SIZE}_queens_annealing.json"):
    file_path = os.path.dirname(__file__) + f"\\locations_files\\2D\\{filename}"

    positions = generate_array(positions)

    with open(file_path, "w") as file:
        json.dump(positions, file)


annealing_position, best_cost, iterations = simulated_annealing(
    temperature=10, cooling_rate=0.99, max_iterations=1000
)
print(f"Postions: {annealing_position}")
print(f"Cost: {best_cost}")
print(f"Number of iterations: {iterations}")


save_positions_to_json(annealing_position)
