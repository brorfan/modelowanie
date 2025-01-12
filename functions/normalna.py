import sympy as sp

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

normal_eq_at_point = normal_eq.subs({a: 4, b: 5, x0: 2, y0: 3})
sp.pprint(normal_eq_at_point)