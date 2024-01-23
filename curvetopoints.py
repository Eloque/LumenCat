import numpy as np

# This comes straight from the Wikipedia article on Bezier curves
# And I have no deep insight in how this works
def quadratic_bezier(start, control, end, num_points=3):
    """
    Generate points along a quadratic Bezier curve.

    Parameters:
    start (tuple): The start point (x, y)
    control (tuple): The control point (x, y)
    end (tuple): The end point (x, y)
    num_points (int): The number of points to generate along the curve

    Returns:
    numpy.ndarray: An array of points along the Bezier curve
    """
    t = np.linspace(0, 1, num_points)
    x = (1 - t)**2 * start[0] + 2 * (1 - t) * t * control[0] + t**2 * end[0]
    y = (1 - t)**2 * start[1] + 2 * (1 - t) * t * control[1] + t**2 * end[1]

    points = np.column_stack((x, y))

    return points


