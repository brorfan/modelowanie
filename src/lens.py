from matplotlib import patches, pyplot as plt


class Lens:
    def __init__(self, center, radius, angle, theta, width, height):
        self.center = center
        self.radius = radius
        self.angle = angle
        self.theta = theta
        self.width = width
        self.height = height


def create_lens(fixed_center_right, fixed_center_left, ax, width_r, lens_right: Lens, lens_left: Lens):
    # rectangle in the middle
    height_r = lens_right.height
    center_r = (lens_right.center[0] - (width_r / 2), lens_right.center[1] - (height_r / 2))

    # lines instead of the rectangle
    line_right_height = lens_right.center[1] + (lens_right.height / 2)
    line_left_height = lens_right.center[1] - (lens_right.height / 2)
    lines_start = lens_right.center[0] - (max(abs(lens_right.width), abs(lens_left.width)) / 2)
    lines_length = lens_right.center[0] + (max(abs(lens_right.width), abs(lens_left.width)) / 2)

    arc_right = patches.Arc(fixed_center_right, lens_right.width, lens_right.height, angle=lens_right.angle, theta1=lens_right.theta, theta2=lens_right.theta + lens_right.angle,
                       edgecolor='black', linewidth=2, facecolor='white')

    arc_left = patches.Arc(fixed_center_left, lens_left.width, lens_left.height, angle=lens_left.angle, theta1=lens_left.theta, theta2=lens_left.theta + lens_left.angle,
                       edgecolor='black', linewidth=2, facecolor='white')

    rectangle = patches.Rectangle(center_r, width_r, height_r,
                                  edgecolor='black', linewidth=2, facecolor='white')

    lines = plt.hlines((line_right_height, line_left_height), lines_start, lines_length, colors='black', linestyles='solid',
                       linewidth=2)

    arc_right.angle = 180
    arc_left.angle = 180

    if lens_right.radius > 0:
        ax.add_patch(arc_right)
        if lens_left.radius > 0:
            ax.add_patch(arc_left)
        elif lens_left.radius < 0:
            arc_left.angle = 360
            ax.add_patch(arc_left)
        elif lens_left.radius == 0:
            line_left = plt.vlines(lines_start, line_right_height, line_left_height, colors='black', linestyles='solid',
                                   linewidth=2)

    elif lens_right.radius < 0:
        arc_right.angle = 360
        ax.add_patch(arc_right)
        if lens_left.radius > 0:
            ax.add_patch(arc_left)
        elif lens_left.radius < 0:
            arc_left.angle = 360
            ax.add_patch(arc_left)
        elif lens_left.radius == 0:
            line_left = plt.vlines(lines_start, line_right_height, line_left_height, colors='black', linestyles='solid',
                                   linewidth=2)

    elif lens_right.radius == 0:
        line_right = plt.vlines(lines_length, line_right_height, line_left_height, colors='black', linestyles='solid')
        if lens_left.radius > 0:
            ax.add_patch(arc_left)
        elif lens_left.radius < 0:
            arc_left.angle = 360
            ax.add_patch(arc_left)
        elif lens_left.radius == 0:
            line_left = plt.vlines(lines_start, line_right_height, line_left_height, colors='black', linestyles='solid',
                                   linewidth=2)
