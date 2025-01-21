import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons, TextBox
from tkinter import messagebox, Tk
from consts import MATERIALS, DPI
from lens import Lens, create_lens, delete_lens
from math_utlis import remove_line, redraw_line

# Funkcja do wyświetlania okna błędu
def show_error(message):
    # Tworzymy ukryte okno główne, które będzie potrzebne do pokazania komunikatu
    root = Tk()
    root.withdraw()  # Ukrywamy główne okno
    messagebox.showerror("Błąd", message)  # Pokazujemy okno z komunikatem o błędzie
    root.destroy()  # Zamykanie okna po wyświetleniu komunikatu

# Tworzenie figury i osi
fig, ax = plt.subplots()

# Tytuł wykresu
ax.set_title(
    "SYMULACJA WIĄZKI ŚWIATŁA PRZEZ SOCZEWKĘ WYPUKŁĄ",
    fontsize=18,
    fontweight='bold',
    color='darkblue',
    style='oblique',
    loc='center',
    pad=20,
)

# Słownik do przechowywania elementów wykresu
plot_elements = {
    'hline': None,
    'first_red_normal_line': None,
    'second_red_normal_line': None,
    'green_tilted_line': None,
    'purple_end_line': None
}

# Ustawienie rozmiarów okna
fig.set_size_inches(1000 / DPI, 580 / DPI)

# Ustawienia osi
ax.set_xlim(-9, 9)
ax.set_ylim(-5, 5)
line_y = 0  # Oś OX
ax.axhline(y=line_y, color='purple', linestyle='--', label=f"y = {line_y}")
ax.set_aspect('equal')
ax.axis('off')

# Inicjalizacja soczewek
lens_right = Lens((0, 0), 1, 180, 90, 1, 10)
lens_left = Lens((0, 0), 4, 180, -90, 4, 10)

# Obliczanie pozycji soczewek
width_r = max(abs(lens_right.width), abs(lens_left.width))
fixed_center_right = (lens_right.center[0] + (width_r / 2), lens_right.center[1])
fixed_center_left = (lens_left.center[0] - (width_r / 2), lens_left.center[1])

# Tworzenie soczewek
created_objects = create_lens(fixed_center_right, fixed_center_left, ax, width_r, lens_right, lens_left)
plot_elements['hline'] = ax.axhline(y=line_y, color='blue', linestyle='-', label=f"y = {line_y}")

plt.axis('equal')

# Tworzenie suwaka
slider_ax = plt.axes((0.05, 0.15, 0.03, 0.7))  # [x, y, width, height]
amplitude_slider = Slider(
    ax=slider_ax,
    label="h",
    valmin=-5,  # Minimum value
    valmax=5,  # Maximum value
    valinit=0,  # Initial value
    valstep=0.2,  # Step size
    orientation="vertical"
)

# Tworzenie przycisków radiowych
radio_ax = plt.axes((0.8, 0.1, 0.15, 0.3))  # Pozycja widżetu (x, y, szerokość, wysokość)
radio = RadioButtons(radio_ax, labels=list(MATERIALS.keys()))  # Utwórz RadioButtons

# Tworzenie pól tekstowych
input_left_ax = plt.axes((0.9, 0.7, 0.05, 0.04))  # [x, y, width, height]
input_left = TextBox(input_left_ax, 'Promień lewej soczewki: \n (Wartości 0<x<10)', lens_left.radius, color='1', hovercolor='0.9')
input_right_ax = plt.axes((0.9, 0.62, 0.05, 0.04))  # [x, y, width, height]
input_right = TextBox(input_right_ax, 'Promień prawej soczewki: \n (Wartości 0<x<10)', lens_right.radius, color='1', hovercolor='0.9')


# Funkcja aktualizująca
def actualisation(label):
    global created_objects, width_r, fixed_center_left, fixed_center_right
    try:
        # Pobranie wartości z pól tekstowych
        lens_left.radius = float(input_left.text)
        lens_left.width = float(input_left.text)
        lens_right.radius = float(input_right.text)
        lens_right.width = float(input_right.text)

        if not (0 < lens_left.radius < 10) or not (0 < lens_right.radius < 10):
            raise ValueError("Promień soczewki musi być w zakresie (0, 10)")

        width_r = max(abs(lens_right.width), abs(lens_left.width))
        fixed_center_right = (lens_right.center[0] + (width_r / 2), lens_right.center[1])
        fixed_center_left = (lens_left.center[0] - (width_r / 2), lens_left.center[1])

        print(f"Selected Label: {label}")
        delete_lens(ax, created_objects)  # Usunięcie poprzednich obiektów
        created_objects = create_lens(fixed_center_right, fixed_center_left, ax, width_r, lens_right, lens_left)
        remove_line(plot_elements)  # Usunięcie linii
        redraw_line(fig, ax, amplitude_slider.val, fixed_center_left, fixed_center_right, lens_left.radius, lens_right.radius,
                    plot_elements, radio)  # Rysowanie nowych linii
    except ValueError as e:
        show_error(f"Błąd: {e}")  # Wyświetlenie okna błędu
    except Exception as e:
        show_error(f"Nieoczekiwany błąd: {e}")  # Wyświetlenie ogólnego okna błędu


# Podłącz funkcję aktualizacji do RadioButtons i pól tekstowych
radio.on_clicked(actualisation)
input_left.on_submit(actualisation)
input_right.on_submit(actualisation)


# Funkcja aktualizacji suwaka
def update(val):
    try:
        slider_value = amplitude_slider.val
        remove_line(plot_elements)  # Usunięcie poprzednich linii
        redraw_line(fig, ax, slider_value, fixed_center_left, fixed_center_right, lens_left.radius, lens_right.radius,
                    plot_elements, radio)  # Rysowanie nowych linii
    except Exception as e:
        show_error(f"Błąd przy aktualizacji suwaka: {e}")  # Wyświetlenie okna błędu


# Podłącz funkcję aktualizacji suwaka
amplitude_slider.on_changed(update)

# Ustawienia wykresu
x = list(range(len(MATERIALS)))  # Indeksy dla materiałów (0, 1, 2, ...)
y = list(MATERIALS.values())  # Wartości n dla każdego materiału
selected_dot, = ax.plot([], [], 'ro', markersize=10)  # Kropka oznaczająca wybór

actualisation('woda')
plt.show()
