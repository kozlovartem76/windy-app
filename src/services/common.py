import numpy as np


def polynomial_interpolation(x, coordinate_values, temperature_values, degree):

    if x < min(coordinate_values) or x > max(coordinate_values):
        raise ValueError("Coordinates not in area")

    index_nearest = np.argmin(np.abs(np.array(coordinate_values) - x))

    coefficients = np.polyfit(
        coordinate_values[index_nearest:index_nearest + degree + 1],
        temperature_values[index_nearest:index_nearest + degree + 1],
        degree
    )
    polynomial = np.poly1d(coefficients)

    interpolated_temperature = polynomial(x)

    return interpolated_temperature

def round_to_nearest_and_get_index(coordinate, step, coordinate_list):
    relative_coordinate = coordinate - coordinate_list[0]
    rounded_relative_coordinate = round(relative_coordinate / step) * step
    rounded_coordinate = rounded_relative_coordinate + coordinate_list[0]
    
    index_nearest = np.argmin(np.abs(np.array(coordinate_list) - rounded_coordinate))

    return rounded_coordinate, index_nearest

