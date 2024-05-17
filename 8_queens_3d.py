from docplex.mp.model import CpoModel
import json

# -----------------------------------------------------------------------------
# Initialize the problem data
# -----------------------------------------------------------------------------

# Set model parameters
NB_QUEEN = 8

# -----------------------------------------------------------------------------
# Build the model
# -----------------------------------------------------------------------------

# Create model
mdl = CpoModel()

# Create column index of each queen
# locations = mdl.integer_var_cube(NB_QUEEN, NB_QUEEN, NB_QUEEN, 0, 1, "X")
locations = mdl.integer_var_matrix(NB_QUEEN, NB_QUEEN, 0, NB_QUEEN - 1, "X")
# mdl.integer_var_dict(NB_QUEEN, NB_QUEEN, NB_QUEEN, 0, NB_QUEEN - 1, "X")

# One queen per row
mdl.add(mdl.all_diff(locations))

# One queen per diagonal xi - xj != i - j
mdl.add(mdl.all_diff(locations[i] + i for i in range(NB_QUEEN)))

# One queen per diagonal xi - xj != j - i
mdl.add(mdl.all_diff(locations[i] - i for i in range(NB_QUEEN)))


# -----------------------------------------------------------------------------
# Solve the model and display the result
# -----------------------------------------------------------------------------

# Solve model
msol = mdl.solve(TimeLimit=10)

# Print solution
if msol:
    print("Solution:", end="")
    for v in locations:
        print(f" {msol[v]},", end="")
    print("\n")
    # Draw chess board
    for l in range(NB_QUEEN):
        qx = msol[locations[l]]
        for c in range(NB_QUEEN):
            field = "1" if c == qx else "0"
            print(field + " ", end="")
        print("")
    # Save solutions to a file

    # Create a list to store the chess board
    chess_board = []

    # Populate the chess board
    for l in range(NB_QUEEN):
        qx = msol[locations[l]]
        row = []
        for c in range(NB_QUEEN):
            row.append(1 if c == qx else 0)
        chess_board.append(row)

    # Save the chess board as JSON
    with open(f"{NB_QUEEN}_queens.json", "w") as file:
        json.dump(chess_board, file)
else:
    print("Solve status: {}\n".format(msol.get_solve_status()))
