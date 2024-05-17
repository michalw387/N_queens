# import numpy as np
# from scipy.optimize import dual_annealing


# def objective(locations):
#     return np.sum(locations)


# lw = [0.0] * 10
# up = [1.0] * 10
# result = dual_annealing(objective, bounds=list(zip(lw, up)))

# # print(result.x)

# # print(result.fun)


# # summarize the result
# print("Status : %s" % result["message"])
# print("Total Evaluations: %d" % result["nfev"])
# # evaluate solution
# solution = result["x"]
# evaluation = objective(solution)
# print("Solution: f(%s) = %.5f" % (solution, evaluation))
# -*- coding: utf-8 -*-
from __future__ import print_function
from show_3d import *
import math
import random
from collections import defaultdict
from simanneal import Annealer


def check_positions(locations):
    grid_size = round(len(locations) ** (1 / 3))
    locations_3d = np.array(locations).reshape(grid_size, grid_size, grid_size)

    for i in range(grid_size):
        for j in range(grid_size):
            for k in range(grid_size):
                if locations_3d[i][j][k] == 1:
                    if (
                        np.sum(locations_3d[i][j]) > 1
                        or np.sum(locations_3d[i][:, k]) > 1
                        or np.sum(locations_3d[:, j][k]) > 1
                    ):
                        return False
    return True

    # for i in range(len(locations)):
    #     for j in range(i + 1, len(locations)):
    #         if locations[i] == locations[j]:
    #             return False
    #         if (
    #             locations[i][0] == locations[j][0]
    #             or locations[i][1] == locations[j][1]
    #             or locations[i][2] == locations[j][2]
    #         ):
    #             return False
    #         if (
    #             abs(locations[i][0] - locations[j][0])
    #             == abs(locations[i][1] - locations[j][1])
    #             == abs(locations[i][2] - locations[j][2])
    #         ):
    #             return False
    # return True


class N_Queens(Annealer):
    """Test annealer with a travelling salesman problem."""

    # pass extra data (the distance matrix) into the constructor
    def __init__(self, state):
        self.size = len(state ** (1 / 3))
        self.locations = state
        super(N_Queens, self).__init__(state)  # important!

    def move(self):
        """Swaps two cities in the route."""
        # no efficiency gain, just proof of concept
        # demonstrates returning the delta energy (optional)
        initial_energy = self.energy()

        a = random.randint(0, len(self.state) - 1)
        b = random.randint(0, len(self.state) - 1)
        self.state[a], self.state[b] = self.state[b], self.state[a]

        return self.energy() - initial_energy

    def energy(self):
        """Calculates the length of the route."""
        e = 0
        for i in range(len(self.state)):
            e += self.distance_matrix[self.state[i - 1]][self.state[i]]
        return e


if __name__ == "__main__":

    # initial state, a randomly-ordered itinerary
    grid_size = 3
    while True:
        init_state = [round(random.random()) for _ in range(grid_size**3)]
        if check_positions(init_state):
            break

    show_in_3d(init_state)

    tsp = N_Queens(init_state)
    tsp.set_schedule(tsp.auto(minutes=0.2))
    # since our state is just a list, slice is the fastest way to copy
    tsp.copy_strategy = "slice"
    state, e = tsp.anneal()

    while state[0] != "New York City":
        state = state[1:] + state[:1]  # rotate NYC to start

    print()
    print("%i mile route:" % e)
    print(" ➞  ".join(state))
