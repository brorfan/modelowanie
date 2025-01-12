import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Slider, RadioButtons
import sympy as sp

# Dane katalogowe
materials = {
    "Szkło": 1.5,
    "Woda": 1.33,
    "Lód": 1.37,
    "Topiony kwarc": 1.46,
    "Diament": 2.417,
}
n_Powietrze = 1.0003

# Przygotowanie wykresu
fig, ax = plt.subplots()

ax.set_title(
    "SYMULACJA WIĄZKI ŚWIATŁA PRZEZ SOCZEWĘ",  # Tytuł
    fontsize=18,  # Rozmiar czcionki
    fontweight='bold',
    color='darkblue',  # Kolor
    style='oblique',  # Styl
    loc='center',  # Pozycja
    pad=20  # Padding
)

# Ustawienie rozmiarów okna
dpi = 100  # Dots per inch (wspolczynnik zamiany pikseli na inches)
fig.set_size_inches(1000 / dpi, 580 / dpi)

ax.set_xlim(-9, 9)
ax.set_ylim(-5, 5)
line_y = 0  # oś OX
ax.axhline(y=line_y, color='purple', linestyle='--', label=f"y = {line_y}")

ax.set_aspect('equal')  # both axes are equal in proportion (i think?)

ax.axis('off')  # opcja włączenia i wyłączenia osi X i Y

# right lens
centerA = (0, 0)  # center coordinates
radiusA = 3  # radius of the circle (right side of the lens)
angleA = 180  # angle range in degrees (from 0 to 360)
thetaA = 90  # starting angle for the arc
widthA = radiusA  # width of the arc
heightA = 10  # height of the arc

# left lens
centerB = (0, 0)
radiusB = 2
angleB = 180
thetaB = -90
widthB = radiusB
heightB = 10

# rectangle in the middle
widthR = max(abs(widthA), abs(widthB))
heightR = heightA
centerR = (centerA[0] - (widthR / 2), centerA[1] - (heightR / 2))

# lines instead of the rectangle
lineA_height = centerA[1] + (heightA / 2)
lineB_height = centerA[1] - (heightA / 2)
lines_start = centerA[0] - (max(abs(widthA), abs(widthB)) / 2)
lines_length = centerA[0] + (max(abs(widthA), abs(widthB)) / 2)

fixed_centerA = (centerA[0] + (widthR / 2), centerA[1])
fixed_centerB = (centerB[0] - (widthR / 2), centerB[1])

plt.scatter(fixed_centerB[0], fixed_centerB[1], color='blue')
plt.scatter(fixed_centerA[0], fixed_centerA[1], color='purple')

arcA = patches.Arc(fixed_centerA, widthA, heightA, angle=angleA, theta1=thetaA, theta2=thetaA + angleA,
                   edgecolor='black', linewidth=2, facecolor='white')

arcB = patches.Arc(fixed_centerB, widthB, heightB, angle=angleB, theta1=thetaB, theta2=thetaB + angleB,
                   edgecolor='black', linewidth=2, facecolor='white')

rectangle = patches.Rectangle(centerR, widthR, heightR,
                              edgecolor='black', linewidth=2, facecolor='white')

lines = plt.hlines((lineA_height, lineB_height), lines_start, lines_length, colors='black', linestyles='solid',
                   linewidth=2)

# line_left = plt.vlines(lines_start, lineA_height, lineB_height, colors='black', linestyles='solid', linewidth=2)

# line_right = plt.vlines(lines_length, lineA_height, lineB_height, colors='black', linestyles='solid', linewidth=2)

arcA.angle = 180
arcB.angle = 180

if radiusA > 0:
    ax.add_patch(arcA)
    if radiusB > 0:
        ax.add_patch(arcB)
    elif radiusB < 0:
        arcB.angle = 360
        ax.add_patch(arcB)
    elif radiusB == 0:
        line_left = plt.vlines(lines_start, lineA_height, lineB_height, colors='black', linestyles='solid', linewidth=2)

elif radiusA < 0:
    arcA.angle = 360
    ax.add_patch(arcA)
    if radiusB > 0:
        ax.add_patch(arcB)
    elif radiusB < 0:
        arcB.angle = 360
        ax.add_patch(arcB)
    elif radiusB == 0:
        line_left = plt.vlines(lines_start, lineA_height, lineB_height, colors='black', linestyles='solid', linewidth=2)

elif radiusA == 0:
    line_right = plt.vlines(lines_length, lineA_height, lineB_height, colors='black', linestyles='solid')
    if radiusB > 0:
        ax.add_patch(arcB)
    elif radiusB < 0:
        arcB.angle = 360
        ax.add_patch(arcB)
    elif radiusB == 0:
        line_left = plt.vlines(lines_start, lineA_height, lineB_height, colors='black', linestyles='solid', linewidth=2)

plt.axis('equal')
hline = ax.axhline(y=line_y, color='blue', linestyle='-', label=f"y = {line_y}")

# Define the position for the slider
slider_ax = plt.axes((0.05, 0.15, 0.03, 0.7))  # [left, bottom, width, height]

# Create a slider
amplitude_slider = Slider(
    ax=slider_ax,
    label="h",
    valmin=-5,  # Minimum value
    valmax=5,  # Maximum value
    valinit=0,  # Initial value
    valstep=0.01,  # Step size
    orientation="vertical"
)

red_normal_line = None


# tworzenie normalnej bazujac na punktach przeciecia i elipsy
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


# Function to remove the line
def remove_line():
    global hline, red_normal_line
    if hline:  # Check if the blue horizontal line exists
        hline.remove()  # Remove the blue line
        hline = None  # Reset the reference

    if red_normal_line:  # Check if the red normal line exists
        red_normal_line.remove()  # Remove the red normal line
        red_normal_line = None  # Reset the reference


# Function to redraw the line
def redraw_line(y_value):
    global hline, red_normal_line
    hline = ax.axhline(y=y_value, color='blue', linestyle='-', label=f"y = {y_value}")

    # Elipse parameters
    x_0, y_0 = fixed_centerB[0], fixed_centerB[1]
    a, b = radiusB / 2, 5
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
        red_normal_line, = ax.plot(x_values, y_values, color='red', label="Normal Line")

    fig.canvas.draw_idle()  # Redraw the plot


# Update function for the slider
def update(val):
    slider_value = amplitude_slider.val  # Get the slider value
    remove_line()  # Remove the old lines (both blue and red)
    redraw_line(slider_value)  # Redraw the line at the new slider value


# Connect the slider to the update function
amplitude_slider.on_changed(update)

# Wybór materiału soczewki

# Ustawienia wykresu
x = list(range(len(materials)))  # Indeksy dla materiałów (0, 1, 2, ...)
y = list(materials.values())  # Wartości n dla każdego materiału
selected_dot, = ax.plot([], [], 'ro', markersize=10)  # Kropka oznaczająca wybór


def n(n_1, n_2):
    return n_2 / n_1


# Funkcja aktualizująca zaznaczenie kropki
def update_dot(label):
    material_list = list(materials.keys())  # Konwertowanie dict_keys do listy
    index = material_list.index(label)  # Indeks wybranego materiału
    wsp_odbicia = n(n_1=n_Powietrze, n_2=materials[index])
    fig.canvas.draw_idle()  # Odśwież wykres


# RadioButtons
radio_ax = plt.axes([0.8, 0.1, 0.15, 0.3])  # Pozycja widżetu (x, y, szerokość, wysokość)
radio = RadioButtons(radio_ax, labels=list(materials.keys()))  # Utwórz RadioButtons

# Podłącz funkcję aktualizacji do RadioButtons
radio.on_clicked(update_dot)


# -----------------------------------------------------------
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


plt.show()
