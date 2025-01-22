import numpy as np
import sympy as sp

from consts import n_Powietrze, MATERIALS
from src.lens import Lens


def normal_line_equation(a, b, x0, y0):
    # Calculate the derivative of the ellipse at (x0, y0)
    z, w = sp.symbols('z w')

    # Equation of the ellipse
    ellipse_eq = (z ** 2 / a ** 2) + (w ** 2 / b ** 2) - 1

    # Derivative of ellipse equation with respect to x (dy/dx)
    dy_dx = sp.diff(ellipse_eq, z) / sp.diff(ellipse_eq, w)

    if y0 == 0:
        slope_tangent = float('inf')  # The tangent at (x0, 0) is vertical (infinite slope)
    else:
        # Evaluate the derivative for other points
        slope_tangent = float(dy_dx.subs({z: x0, w: y0}))  # Example: a = 1, b = 1

    # The slope of the normal line is the negative reciprocal of the tangent slope
    slope_normal = -1 / slope_tangent if slope_tangent != 0 else float('inf')

    # Equation of the normal line at (x0, y0)
    # y - y0 = slope_normal * (x - x0)
    return - slope_normal, y0 + slope_normal * x0


def tilted_line_eq(x_p, y_p, a_normal, n1, n2):
    # angles taken from Snell's law
    alpha = np.arctan(a_normal)
    beta = np.arcsin((n1 / n2) * np.sin(alpha))

    # we get a function of a line y = m*x + y_p - a*x_p (y = mx + b)
    m = np.tan(alpha - beta)
    b = y_p - m * x_p

    return m, b


def draw_tilted_line(ax, x_p, x_k, a_tilted, b_tilted, plot_elements):
    # Create x values around the intersection point to plot the normal line
    x_values = np.linspace(x_p, x_k, 100)

    # Calculate corresponding y values of the normal line
    y_values = a_tilted * x_values + b_tilted

    # Plot the normal line (store the plot object)
    plot_elements['green_tilted_line'], = ax.plot(x_values, y_values, color='green', label="Tilted Line")


def end_line_eq(x_k, y_k, m_tilted, a_normal, n1, n2):
    # angles taken from Snell's law
    theta = np.arctan(m_tilted) + np.arctan(a_normal)
    epsilon = np.arcsin((n2 / n1) * np.sin(theta)) - np.arctan(a_normal)

    # we get a function of a line y = s*x + y_k - s*x_k (y = sx + b)
    s = np.tan(epsilon)
    b = y_k - np.tan(epsilon) * x_k

    return s, b


def draw_end_line(ax, x_p, a_end, b_end, plot_elements):
    # Create x values around the intersection point to plot the normal line
    x_values = np.linspace(x_p, x_p + 7, 100)

    # Calculate corresponding y values of the normal line
    y_values = a_end * x_values + b_end

    # Plot the normal line (store the plot object)
    plot_elements['purple_end_line'], = ax.plot(x_values, y_values, color='purple', label="End Line")


def remove_line(plot_elements):
    if plot_elements['hline']:  # Check if the blue horizontal line exists
        plot_elements['hline'].remove()  # Remove the blue line
        plot_elements['hline'] = None  # Reset the reference

    if plot_elements['first_red_normal_line']:  # Check if the red normal line exists
        plot_elements['first_red_normal_line'].remove()  # Remove the red normal line
        plot_elements['first_red_normal_line'] = None  # Reset the reference

    if plot_elements['second_red_normal_line']:  # Check if the red normal line exists
        plot_elements['second_red_normal_line'].remove()  # Remove the red normal line
        plot_elements['second_red_normal_line'] = None  # Reset the reference

    if plot_elements['green_tilted_line']:  # Check if the red normal line exists
        plot_elements['green_tilted_line'].remove()  # Remove the red normal line
        plot_elements['green_tilted_line'] = None  # Reset the reference

    if plot_elements['purple_end_line']:  # Check if the red normal line exists
        plot_elements['purple_end_line'].remove()  # Remove the red normal line
        plot_elements['purple_end_line'] = None  # Reset the reference


def redraw_line(fig, ax, y_value, lens_left: Lens, lens_right: Lens, plot_elements,
                radio_buttons):
    # PRAMATERES ---------------------------------
    hline = (0, y_value)  # Horizontal line equation
    selected_label = radio_buttons.value_selected

    # 1st Elipse parameters
    x_01, y_01 = lens_left.center[0], lens_left.center[1]
    a1, b1 = lens_left.radius / 2, 5

    # Get intersection points with the first ellipse
    points = intersection_with_ellipse(x_01, y_01, a1, b1, hline)
    point_x, point_y = points[0][0], points[0][1]

    # 1st normal line in the 1st intersection point
    print(a1, b1, point_x, point_y)
    slope_1st_normal, b_1st_normal = normal_line_equation(a1, b1, point_x, point_y)

    # 2nd Elipse parameters
    x_02, y_02 = lens_right.center[0], lens_right.center[1]
    a2, b2 = lens_right.radius / 2, 5

    # Tilted line equation
    tilted_line_equation = tilted_line_eq(point_x, point_y, slope_1st_normal, n_Powietrze,
                                          MATERIALS[selected_label])

    # Get intersection points with the second ellipse
    sec_points = intersection_with_ellipse(x_02, y_02, a2, b2, tilted_line_equation)
    sec_point_x, sec_point_y = sec_points[1][0], sec_points[1][1]

    # 2nd normal line in the 2nd intersection point
    slope_2nd_normal, b_2nd_normal = normal_line_equation(a2, b2, sec_point_x, sec_point_y)

    # End line equation
    end_line_equation = end_line_eq(sec_point_x, sec_point_y, tilted_line_equation[0], slope_2nd_normal, n_Powietrze,
                                    MATERIALS[selected_label])

    # PLOTTING -----------------------------------
    # Draw the horizontal laser
    plot_elements['hline'] = ax.hlines(y=y_value, xmin=-12, xmax=points[0][0], color='blue', linestyle='-',
                                       label=f"y = {y_value}")

    # Draw the tilted laser
    draw_tilted_line(ax, point_x, sec_point_x, tilted_line_equation[0], tilted_line_equation[1], plot_elements)
    # print(f"tilted = {tilted_line_equation}")

    # Draw the end laser
    draw_end_line(ax, sec_point_x, end_line_equation[0], end_line_equation[1], plot_elements)
    # print(f"tilted = {end_line_equation}")

    # NORMAL LINES --------------------------------
    draw_normal_lines = False
    if draw_normal_lines == True:
        # Create x values around the intersection point to plot the 1st normal line
        x_1st_normal_values = np.linspace(point_x - 3, point_x + 3, 100)

        # Calculate corresponding y values of the 1st normal line
        y_1st_normal_values = slope_1st_normal * x_1st_normal_values + b_1st_normal

        # Plot the 1st normal line (store the plot object)
        plot_elements['first_red_normal_line'], = ax.plot(x_1st_normal_values, y_1st_normal_values, color='red',
                                                          label="1st Normal Line")

        # Create x values around the intersection point to plot the 2nd normal line
        x_2nd_normal_values = np.linspace(sec_point_x - 3, sec_point_x + 3, 100)

        # Calculate corresponding y values of the 2nd normal line
        y_2nd_normal_values = slope_2nd_normal * x_2nd_normal_values + b_2nd_normal

        # Plot the 2nd normal line (store the plot object)
        plot_elements['second_red_normal_line'], = ax.plot(x_2nd_normal_values, y_2nd_normal_values, color='red',
                                                           label="2nd Normal Line")

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
    print(points)

    return points
