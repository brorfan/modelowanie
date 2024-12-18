import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots()

ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)

ax.set_aspect('equal')  # both axes are equal in proportion (i think?)

ax.axis('off')  # an option to turn off the axis

# right lens
centerA = (0, 0)  # center coordinates
radiusA = 2  # radius of the circle (right side of the lens)
angleA = 180  # angle range in degrees (from 0 to 360)
thetaA = 90  # starting angle for the arc
widthA = radiusA # width of the arc
heightA = 10  # height of the arc

# left lens
centerB = (0, 0)
radiusB = -1
angleB = 180
thetaB = -90
widthB = radiusB
heightB = 10

# rectangle in the middle
widthR = max(widthA, widthB)
heightR = heightA
centerR = (centerA[0] - (widthR / 2), centerA[1] - (heightR / 2))

fixed_centerA = (centerA[0] + (widthR/2), centerA[1])
fixed_centerB = (centerB[0] - (widthR/2), centerB[1])

arcA = patches.Arc(fixed_centerA, widthA, heightA, angle=angleA, theta1=thetaA, theta2=thetaA + angleA,
                   edgecolor='black', linewidth=2, facecolor='white')

arcB = patches.Arc(fixed_centerB, widthB, heightB, angle=angleB, theta1=thetaB, theta2=thetaB + angleB,
                   edgecolor='black', linewidth=2, facecolor='white')

rectangle = patches.Rectangle(centerR, widthR, heightR,
                              edgecolor='black', linewidth=2, facecolor='white')

arcA.angle = 180
arcB.angle = 180
if radiusA > 0:
    ax.add_patch(arcA)
    ax.add_patch(rectangle)
    if radiusB > 0:
        ax.add_patch(arcB)
    elif radiusB < 0:
        arcB.angle = 360
        ax.add_patch(arcB)
elif radiusA < 0:
    arcA.angle = 360
    ax.add_patch(rectangle)
    ax.add_patch(arcA)
    if radiusB > 0:
        ax.add_patch(arcB)
    elif radiusB < 0:
        arcB.angle = 360
        ax.add_patch(arcB)
elif radiusA == 0:
    ax.add_patch(rectangle)
    if radiusB > 0:
        ax.add_patch(arcB)
    elif radiusB < 0:
        arcB.angle = 360
        ax.add_patch(arcB)


plt.show()
