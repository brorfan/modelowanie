import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons

from consts import MATERIALS, DPI

from lens import Lens, create_lens
from math_utlis import remove_line, redraw_line

fig, ax = plt.subplots()

ax.set_title(
    "SYMULACJA WIĄZKI ŚWIATŁA PRZEZ SOCZEWKĘ",
    fontsize=18,
    fontweight='bold',
    color='darkblue',
    style='oblique',
    loc='center',
    pad=20,
)

plot_elements = {
    'hline': None,
    'first_red_normal_line': None,
    'second_red_normal_line': None,
    'green_tilted_line': None,
    'purple_end_line': None
}

# Ustawienie rozmiarów okna
fig.set_size_inches(1000 / DPI, 580 / DPI)

ax.set_xlim(-9, 9)
ax.set_ylim(-5, 5)
line_y = 0  # oś OX

ax.axhline(y=line_y, color='purple', linestyle='--', label=f"y = {line_y}")

ax.set_aspect('equal')  # both axes are equal in proportion (i think?)

ax.axis('off')  # opcja włączenia i wyłączenia osi X i Y

lens_right = Lens((0, 0), 1, 180, 90, 1, 10)
lens_left = Lens((0, 0), 4, 180, -90, 4, 10)

# rectangle in the middle
width_r = max(abs(lens_right.width), abs(lens_left.width))

fixed_center_right = (lens_right.center[0] + (width_r / 2), lens_right.center[1])
fixed_center_left = (lens_left.center[0] - (width_r / 2), lens_left.center[1])

# draws the centers of the eliptic figures
# plt.scatter(fixed_center_left[0], fixed_center_left[1], color='blue')
# plt.scatter(fixed_center_right[0], fixed_center_right[1], color='purple')

# line_left = plt.vlines(lines_start, lineA_height, lineB_height, colors='black', linestyles='solid', linewidth=2)

# line_right = plt.vlines(lines_length, lineA_height, lineB_height, colors='black', linestyles='solid', linewidth=2)

create_lens(fixed_center_right, fixed_center_left, ax, width_r, lens_right, lens_left)
plot_elements['hline'] = ax.axhline(y=line_y, color='blue', linestyle='-', label=f"y = {line_y}")

plt.axis('equal')

# Define the position for the slider
slider_ax = plt.axes((0.05, 0.15, 0.03, 0.7))  # [x, y, width, height]

# Create a slider
amplitude_slider = Slider(
    ax=slider_ax,
    label="h",
    valmin=-5,  # Minimum value
    valmax=5,  # Maximum value
    valinit=0,  # Initial value
    valstep=0.2,  # Step size
    orientation="vertical"
)

# Create buttons
radio_ax = plt.axes((0.8, 0.1, 0.15, 0.3))  # Pozycja widżetu (x, y, szerokość, wysokość)
radio = RadioButtons(radio_ax, labels=list(MATERIALS.keys()))  # Utwórz RadioButtons

# Funkcja aktualizująca
def actualisation(label):
    slider_value = amplitude_slider.val
    print(f"Selected Label: {label}")
    remove_line(plot_elements)
    redraw_line(fig, ax, slider_value, fixed_center_left, fixed_center_right, lens_left.radius, lens_right.radius, plot_elements, radio)

# Podłącz funkcję aktualizacji do RadioButtons
radio.on_clicked(actualisation)

# Update function for the slider
def update(val):
    slider_value = amplitude_slider.val  # Get the slider value
    remove_line(plot_elements)  # Remove the old lines (both blue and red and green)
    redraw_line(fig, ax, slider_value, fixed_center_left, fixed_center_right, lens_left.radius, lens_right.radius, plot_elements, radio)  # Redraw the line at the new slider value


# Connect the slider to the update function
amplitude_slider.on_changed(update)

# Ustawienia wykresu
x = list(range(len(MATERIALS)))  # Indeksy dla materiałów (0, 1, 2, ...)
y = list(MATERIALS.values())  # Wartości n dla każdego materiału
selected_dot, = ax.plot([], [], 'ro', markersize=10)  # Kropka oznaczająca wybór




plt.show()
