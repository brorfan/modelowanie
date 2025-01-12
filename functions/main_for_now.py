import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Slider

# Dane katalogowe
n_szkla = 1.5
n_wody = 1.33
n_lodu = 1.37
n_topionego_kwarcu = 1.46
n_diamentu = 2.417
n_powietrza = 1.0003

# Przygotowanie wykresu
fig, ax = plt.subplots()

ax.set_title(
    "SYMULACJA WIĄZKI ŚWIATŁA PRZEZ SOCZEWĘ",  # Tytuł
    fontsize=18,      # Rozmiar czcionki
    fontweight='bold',
    color='darkblue',  # Kolor
    style='oblique',    # Styl
    loc='center',      # Pozycja
    pad=20             # Padding
)

# Ustawienie rozmiarów okna
dpi = 100  # Dots per inch (wspolczynnik zamiany pikseli na inches)
fig.set_size_inches(950 / dpi, 580 / dpi)

ax.set_xlim(-9, 9)
ax.set_ylim(-5, 5)
line_y = 0 # oś OX
ax.axhline(y=line_y, color='purple', linestyle='--', label=f"y = {line_y}")

ax.set_aspect('equal')  # both axes are equal in proportion (i think?)

ax.axis('off')  # opcja włączenia i wyłączenia osi X i Y

# right lens
centerA = (0, 0)  # center coordinates
radiusA = 2  # radius of the circle (right side of the lens)
angleA = 180  # angle range in degrees (from 0 to 360)
thetaA = 90  # starting angle for the arc
widthA = radiusA  # width of the arc
heightA = 10  # height of the arc

# left lens
centerB = (0, 0)
radiusB = 1
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

plt.scatter(fixed_centerB, fixed_centerA, color='blue')

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

# Function to remove the line
def remove_line():
    global hline
    if hline:  # Check if the line exists
        hline.remove()  # Remove the line
        hline = None  # Reset the reference

# Function to redraw the line
def redraw_line(y_value):
    global hline
    hline = ax.axhline(y=y_value, color='blue', linestyle='-', label=f"y = {y_value}")
    fig.canvas.draw_idle()  # Refresh the figure

# Update function for the slider
def update(val):
    slider_value = amplitude_slider.val  # Get the slider value
    remove_line()  # Remove the old line
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

plt.show()
