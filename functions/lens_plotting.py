import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sympy as sp

fig, ax = plt.subplots()

ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)

ax.set_aspect('equal')  # both axes are equal in proportion (i think?)

ax.axis('off')  # an option to turn off the axis

# right lens
centerA = (0, 0)  # center coordinates
radiusA = -2  # radius of the circle (right side of the lens)
angleA = 180  # angle range in degrees (from 0 to 360)
thetaA = 90  # starting angle for the arc
widthA = radiusA  # width of the arc
heightA = 10  # height of the arc

# left lens
centerB = (0, 0)
radiusB = -1
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


fixed_centerA = (centerA[0] + (widthR/2), centerA[1])
fixed_centerB = (centerB[0] - (widthR/2), centerB[1])

# Definicja zmiennych
x, y, a, b = sp.symbols('x y a b')

# Równanie elipsy
ellipse_eq = x**2/a**2 + y**2/b**2 - 1

# Obliczanie pochodnej implicitnej (dy/dx)
dy_dx = sp.diff(ellipse_eq, x) / sp.diff(ellipse_eq, y)

# Wyświetlenie nachylenia stycznej (dy/dx)
slope_tangent = sp.simplify(dy_dx)

# Nachylenie normalnej (prostopadłe do stycznej)
slope_normal = -1 / slope_tangent

# Współrzędne punktu na elipsie
x0, y0 = sp.symbols('x0 y0')

# Równanie normalnej w punkcie (x0, y0)
normal_eq = y - y0 - slope_normal * (x - x0)

# Wyświetlanie równania normalnej
# sp.pprint(normal_eq)

normal_eq_at_point = normal_eq.subs({a: widthB, b: heightB, x0: 2, y0: 3})
sp.pprint(normal_eq_at_point)

arcA = patches.Arc(fixed_centerA, widthA, heightA, angle=angleA, theta1=thetaA, theta2=thetaA + angleA,
                   edgecolor='black', linewidth=2, facecolor='white')

arcB = patches.Arc(fixed_centerB, widthB, heightB, angle=angleB, theta1=thetaB, theta2=thetaB + angleB,
                   edgecolor='black', linewidth=2, facecolor='white')

rectangle = patches.Rectangle(centerR, widthR, heightR,
                              edgecolor='black', linewidth=2, facecolor='white')

lines = plt.hlines((lineA_height, lineB_height), lines_start, lines_length, colors='black', linestyles='solid', linewidth=2)

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


plt.show()
