from matplotlib import patches, pyplot as plt


class Lens:
    def __init__(self, center, radius, angle, theta, width, height):
        self.center = center
        self.radius = radius
        self.angle = angle
        self.theta = theta
        self.width = width
        self.height = height


def create_lens(ax, lens_right: Lens, lens_left: Lens):

    line_right_height = lens_right.center[1] + (lens_right.height / 2)
    line_left_height = lens_right.center[1] - (lens_right.height / 2)
    created_objects = []

    arc_right = patches.Arc(lens_right.center, lens_right.width, lens_right.height, angle=lens_right.angle, theta1=lens_right.theta, theta2=lens_right.theta + lens_right.angle,
                       edgecolor='black', linewidth=1.5, facecolor='white')

    arc_left = patches.Arc(lens_left.center, lens_left.width, lens_left.height, angle=lens_left.angle, theta1=lens_left.theta, theta2=lens_left.theta + lens_left.angle,
                       edgecolor='black', linewidth=1.5, facecolor='white')

    lines = ax.hlines((line_right_height, line_left_height), lens_left.center[0], lens_right.center[0], colors='black', linestyles='solid',
                       linewidth=1.5)

    created_objects.append(lines)

    arc_right.angle = 180
    arc_left.angle = 180

    if lens_right.radius > 0:
        ax.add_patch(arc_right)
        created_objects.append(arc_right)
        if lens_left.radius > 0:
            ax.add_patch(arc_left)
            created_objects.append(arc_left)
        elif lens_left.radius < 0:
            arc_left.angle = 360
            ax.add_patch(arc_left)
            created_objects.append(arc_left)
    elif lens_right.radius < 0:
        arc_right.angle = 360
        ax.add_patch(arc_right)
        created_objects.append(arc_right)
        if lens_left.radius > 0:
            ax.add_patch(arc_left)
            created_objects.append(arc_left)
        elif lens_left.radius < 0:
            arc_left.angle = 360
            ax.add_patch(arc_left)
            created_objects.append(arc_left)

    return created_objects


def delete_lens(ax, created_objects):
    # Remove all created objects from the axes
    for obj in created_objects:
        obj.remove()
    ax.figure.canvas.draw()  # Redraw the canvas to update the plot
