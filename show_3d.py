from os import name
import matplotlib.pyplot as plt
import numpy as np
import json


def get_file_path(filename, dim=3):
    file_path = "locations_files\\"

    if dim == 3:
        file_path += "3D\\"
    elif dim == 2:
        file_path += "2D\\"

    file_path += filename
    return file_path


def import_locations_from_txt(filename="8_towers.txt", dim=3):
    file_path = get_file_path(filename, dim)
    with open(file_path, "r") as file:
        locations = file.read()
    return convert_text_to_list(locations)


def import_locations_from_json(filename="8_towers.json", dim=3):
    file_path = get_file_path(filename, dim)
    with open(file_path, "r") as file:
        raw_locations = file.read()
    return np.array(json.loads(raw_locations)).ravel()


def convert_text_to_list(raw_text):
    # Remove unnecessary characters and split by lines
    lines = raw_text.replace("[[", "[").replace("]]", "]").split("\n")

    # Remove empty lines and whitespace
    lines = [line.strip() for line in lines if line.strip()]

    lines = [line.replace(" ", ",") for line in lines]

    # Join the lines and evaluate as Python code
    nested_list = eval(",".join(lines))

    # Flatten the nested list
    flat_list = [item for sublist in nested_list for item in sublist]

    return flat_list


def color_points_by_location(locations, points):
    red_points = []
    blue_points = []

    for point in points:
        red_points.append(
            [point[i] for i in range(len(locations)) if locations[i] == 1]
        )
        blue_points.append(
            [point[i] for i in range(len(locations)) if locations[i] == 0]
        )

    return np.array(red_points), np.array(blue_points)


def add_labels(ax, locations, x, y, z=None):
    for i in range(len(locations)):
        ax.text(
            x[i],
            y[i],
            z[i],
            f"{x[i]} {y[i]} {z[i]}",
            color="black",
            fontsize=8,
            ha="center",
            va="bottom",
        )


def show_in_2d(locations):
    grid_size = round(len(locations) ** (1 / 2))
    fig = plt.figure(figsize=(10, 10))
    ax = fig.subplots()

    x = np.array(range(grid_size))
    y = np.array(range(grid_size))
    X, Y = np.meshgrid(x, y)
    x, y = X.ravel(), Y.ravel()

    red_points, blue_points = color_points_by_location(locations, np.array([x, y]))

    ax.scatter(
        blue_points[0],
        blue_points[1],
        c="b",
        marker="o",
        s=100,
        label="Empty position",
    )
    ax.scatter(
        red_points[0],
        red_points[1],
        c="r",
        marker="o",
        s=100,
        label="Queen's position",
    )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    ax.set_xticks(np.arange(0, grid_size))
    ax.set_yticks(np.arange(0, grid_size))

    plt.title(f"Grid for {grid_size}x{grid_size}", fontsize=20)
    plt.grid()
    plt.legend(loc="upper right", bbox_to_anchor=(1, 0.5))
    plt.show()


def show_in_3d(locations, color_points=True, labels=False, print_connections=False):
    points_size = 50
    points_size_ratio = 0.3

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(projection="3d")

    grid_size = round(len(locations) ** (1 / 3))

    # # Create 3D grid
    x = np.array(range(1, grid_size + 1))
    y = np.array(range(1, grid_size + 1))
    z = np.array(range(1, grid_size + 1))
    Y, X, Z = np.meshgrid(x, y, z)
    x, y, z = X.ravel(), Y.ravel(), Z.ravel()

    if color_points:

        red_points, blue_points = color_points_by_location(
            locations, np.array([x, y, z])
        )

        ax.scatter(
            blue_points[0],
            blue_points[1],
            blue_points[2],
            c="#51ace8",
            marker="o",
            s=points_size * pow(grid_size, 1 / 5) * points_size_ratio,
        )
        ax.scatter(
            red_points[0],
            red_points[1],
            red_points[2],
            c="r",
            marker="o",
            s=points_size * pow(grid_size, 1 / 5),
        )

    else:
        ax.scatter(
            x, y, z, c=x + y + z, marker="o", s=points_size * pow(grid_size, 1 / 3)
        )

    if labels:
        add_labels(ax, locations, x, y, z)

    if print_connections:
        for i in range(len(locations)):
            for j in range(i + 1, len(locations)):
                if (
                    (x[i] == x[j] and y[i] == y[j])
                    or (y[i] == y[j] and z[i] == z[j])
                    or (x[i] == x[j] and z[i] == z[j])
                ):
                    ax.plot(
                        [x[i], x[j]],
                        [y[i], y[j]],
                        [z[i], z[j]],
                        c="k",
                        linewidth=0.5,
                    )

    ax.set_xlabel("X Label")
    ax.set_ylabel("Y Label")
    ax.set_zlabel("Z Label")

    ax.set_xticks(np.arange(1, grid_size))
    ax.set_yticks(np.arange(1, grid_size))
    ax.set_zticks(np.arange(1, grid_size))

    plt.title(f"Grid for {grid_size}x{grid_size}x{grid_size}", fontsize=20)
    plt.show()


def print_indexes(grid_size):
    for z_offset in range(grid_size):
        print("main loop", z_offset + 1)
        for x_offset in range(grid_size - z_offset):
            print("\tsub loop", x_offset + 1)
            for i in range(min(grid_size - x_offset, grid_size - z_offset)):
                print("\t\t", i + x_offset, i, i + z_offset)


def print_indexes_down(grid_size):
    for z_offset in range(1, grid_size + 1):
        print("main loop", z_offset + 1)
        for x_offset in range(1, grid_size - z_offset + 1):
            print("\tsub loop", x_offset + 1)
            for i in range(1, min(grid_size - x_offset, grid_size - z_offset) + 1):
                print("\t\t", i + x_offset, i, grid_size - z_offset + 1 - i)


def generate_empty_locations(grid_size):
    locations = np.zeros((grid_size, grid_size, grid_size)).flatten()
    return locations


def show_from_files(filenames, labels=False, dim=3):
    for filename in filenames:
        if filename.endswith(".json"):
            locations = import_locations_from_json(filename, dim)
        else:
            locations = import_locations_from_txt(filename, dim)
        if dim == 3:
            show_in_3d(locations, labels=labels)
        elif dim == 2:
            show_in_2d(locations)


if __name__ == "__main__":

    # print_indexes(4)

    # print_indexes_down(4)

    filenames_txt = [
        "5_queens.txt",
        "6_queens.txt",
        "7_queens.txt",
    ]

    filenames_txt = ["5_queens.txt"]

    show_from_files(filenames_txt, labels=False)
    show_from_files(filenames_txt, labels=True)

    empty_locations_4 = generate_empty_locations(4)
    empty_locations_6 = generate_empty_locations(6)
    # show_in_3d(empty_locations)
    # show_in_3d(empty_locations_4, labels=True, color_points=False)
    # show_in_3d(empty_locations_6, labels=True, color_points=False)

    empty_locations = generate_empty_locations(6)
    # show_in_3d(empty_locations, color_points=False)

    filenames_json = ["8_queens.json"]
    # show_from_files(filenames_json, dim=2)
