import matplotlib.pyplot as plt
import numpy as np

from matplotlib.widgets import Button, Slider, TextBox

simulation_data = {
    "time": 2.0,
    "height": 50.0
}

# colours
white = "#fff"
red = "#FF474D"


# random function to check if inputs work
def f(time, height, idk):
    return time * np.sin(2 * np.pi * height * idk)


# defining initial height on the slider and graph
init_height = 50
init_time = 2
idk = np.linspace(0, 1, 500)

# random graph and function etc
fig, ax = plt.subplots()
line, = ax.plot(idk, f(init_time, init_height, idk), lw=2)
ax.set_xlabel('Time [s]')

# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.25, bottom=0.35)

# horizontal slider for the height
axheight = fig.add_axes([0.25, 0.2, 0.65, 0.03])
height_slider = Slider(
    ax=axheight,
    label='Height [mm]',
    valmin=1,
    valmax=100,
    valinit=init_height,
)

axbox = fig.add_axes([0.25, 0.15, 0.65, 0.03])
text_box = TextBox(axbox, "Evaluate", textalignment="center")


# function called each time any input from user is changed
def update_figure():
    line.set_ydata(f(simulation_data['time'], simulation_data['height'], idk))
    fig.canvas.draw_idle()


def slider_update(val: float):
    simulation_data['height'] = val
    update_figure()


def time_input_update(val: str):
    try:
        simulation_data['time'] = float(val)
    except Exception:
        change_box_color(red)
    update_figure()


def change_box_color(colour):
    text_box.color = colour
    text_box.hovercolor = colour


# register the update function with each slider
height_slider.on_changed(slider_update)
text_box.on_submit(time_input_update)
text_box.on_text_change(lambda x: change_box_color(white))

# button to reset values
resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
reset_button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    height_slider.reset()


reset_button.on_clicked(reset)

plt.show()
