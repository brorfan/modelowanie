import numpy as np
import sympy as sp


def normal_line_equation(a, b, x0, y0):
    # Calculate the derivative of the ellipse at (x0, y0)
    z, w = sp.symbols('z w')

    # Equation of the ellipse
    ellipse_eq = (z ** 2 / a ** 2) + (w ** 2 / b ** 2) - 1

    # Derivative of ellipse equation with respect to x (dy/dx)
    dy_dx = sp.diff(ellipse_eq, z) / sp.diff(ellipse_eq, w)

    # Evaluate the derivative (dy/dx) at (x0, y0)
    slope_tangent = float(dy_dx.subs({z: x0, w: y0}))

    # The slope of the normal line is the negative reciprocal of the tangent slope
    slope_normal = -1 / slope_tangent if slope_tangent != 0 else float('inf')

    # Equation of the normal line at (x0, y0)
    # y - y0 = slope_normal * (x - x0)
    return - slope_normal, y0 + slope_normal * x0


def remove_line(plot_elements):
    if plot_elements['hline']:  # Check if the blue horizontal line exists
        plot_elements['hline'].remove()  # Remove the blue line
        plot_elements['hline'] = None  # Reset the reference

    if plot_elements['red_normal_line']:  # Check if the red normal line exists
        plot_elements['red_normal_line'].remove()  # Remove the red normal line
        plot_elements['red_normal_line'] = None  # Reset the reference


def redraw_line(fig, ax, y_value, fixed_center_left, radius_left, plot_elements):
    plot_elements['hline'] = ax.axhline(y=y_value, color='blue', linestyle='-', label=f"y = {y_value}")

    # Elipse parameters
    x_0, y_0 = fixed_center_left[0], fixed_center_left[1]
    a, b = radius_left / 2, 5
    line = (0, y_value)  # Horizontal line equation

    # Get intersection points with ellipse
    points = intersection_with_ellipse(x_0, y_0, a, b, line)

    if points:
        point_x, point_y = points[0][0], points[0][1]

        # Get the slope and equation of the normal line
        slope_normal, y_intercept = normal_line_equation(a, b, point_x, point_y)

        # Create x values around the intersection point to plot the normal line
        x_values = np.linspace(point_x - 5, point_x + 5, 100)

        # Calculate corresponding y values of the normal line
        y_values = slope_normal * x_values + y_intercept

        # Plot the normal line (store the plot object)
        plot_elements['red_normal_line'], = ax.plot(x_values, y_values, color='red', label="Normal Line")

    fig.canvas.draw_idle()  # Redraw the plot


def intersection_with_ellipse(x_0, y_0, a, b, line):
    # Tworzymy zmienne symboliczne
    z, w = sp.symbols('z w')

    # Równanie elipsy
    ellipse_eq = ((z - x_0) ** 2 / a ** 2) + ((w - y_0) ** 2 / b ** 2) - 1

    # Rozkład równania prostej w postaci y = mx + c
    m, c = line

    # Podstawiamy równanie prostej do równania elipsy
    ellipse_eq_sub = ellipse_eq.subs(w, m * z + c)

    # Rozwiązujemy równanie dla x
    solutions_x = sp.solve(ellipse_eq_sub, z)

    # Obliczamy odpowiednie y dla punktów x
    points = []
    for sol_x in solutions_x:
        sol_y = m * sol_x + c
        points.append((sol_x, sol_y))

    return points
