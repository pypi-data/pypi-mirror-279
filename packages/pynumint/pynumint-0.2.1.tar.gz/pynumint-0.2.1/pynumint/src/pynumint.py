import numpy as np

def trapezoidal_rule(f, a, b, n):
    h = (b - a) / n
    total = (f(a) + f(b)) / 2
    for i in range(1, n):
        total += f(a + i * h)
    return total * h

def simpsons_rule(f, a, b, n):
    if n % 2 != 0:
        raise ValueError("n must be an even number.")
    
    h = (b - a) / n
    x = [a + i * h for i in range(n + 1)]
    y = [f(xi) for xi in x]
    
    total = y[0] + y[-1]
    
    for i in range(1, n, 2):
        total += 4 * y[i]
    
    for i in range(2, n, 2):
        total += 2 * y[i]
    
    return (h / 3) * total

def midpoint_rule(f, a, b, n):
    h = (b - a) / n
    total = 0
    for i in range(n):
        total += f(a + (i + 0.5) * h)
    return total * h

def booles_rule(f, a, b, n):
    if n % 4 != 0:
        raise ValueError("n must be a multiple of 4.")
    
    h = (b - a) / n
    total = 0
    for i in range(0, n, 4):
        x0 = a + i * h
        x1 = x0 + h
        x2 = x0 + 2 * h
        x3 = x0 + 3 * h
        x4 = x0 + 4 * h
        total += 7 * f(x0) + 32 * f(x1) + 12 * f(x2) + 32 * f(x3) + 7 * f(x4)
    
    return (2 * h / 45) * total

def romberg_integration(f, a, b, tol=1e-6):
    R = [[0.5 * (b - a) * (f(a) + f(b))]]
    n = 1
    while True:
        h = float(b - a) / 2**n
        R.append([0.5 * R[n-1][0] + h * sum(f(a + (2*k - 1) * h) for k in range(1, 2**(n-1) + 1))])
        for m in range(1, n + 1):
            R[n].append(R[n][m-1] + (R[n][m-1] - R[n-1][m-1]) / (4**m - 1))
        if abs(R[n][n] - R[n-1][n-1]) < tol:
            return R[n][n]
        n += 1

def gauss_legendre_quadrature(f, a, b, n):
    [x, w] = np.polynomial.legendre.leggauss(n)
    t = 0.5 * (x + 1) * (b - a) + a
    return 0.5 * (b - a) * sum(w[i] * f(t[i]) for i in range(n))

def gauss_chebyshev_quadrature(f, n):
    # Compute Chebyshev nodes
    nodes = np.cos((2 * np.arange(1, n + 1) - 1) * np.pi / (2 * n))
    
    # Compute weights
    weights = np.pi / n
    
    # Compute integral using Gauss-Chebyshev quadrature formula
    integral = np.sum(weights * f(nodes))
    
    return integral

def gauss_laguerre_quadrature(f, n):
    # Compute Laguerre nodes
    nodes, weights = np.polynomial.laguerre.laggauss(n)
    
    # Compute integral using Gauss-Laguerre quadrature formula
    integral = np.sum(weights * f(nodes))
    
    return integral

def gauss_hermite_quadrature(f, n):
    # Compute Hermite nodes
    nodes, weights = np.polynomial.hermite.hermgauss(n)
    
    # Compute integral using Gauss-Hermite quadrature formula
    integral = np.sum(weights * f(nodes))
    
    return integral

def adaptive_simpsons_rule(f, a, b, epsilon, S=None, fa=None, fb=None, fm=None, n=1):
    if S is None:
        fa = f(a)
        fb = f(b)
        fm = f((a + b) / 2)
        S = (b - a) * (fa + 4 * fm + fb) / 6
    c = (a + b) / 2
    h = (b - a) / 2
    fd = f((a + c) / 2)
    fe = f((c + b) / 2)
    Sleft = h * (fa + 4 * fd + fm) / 12
    Sright = h * (fm + 4 * fe + fb) / 12
    if abs(Sleft + Sright - S) <= 15 * epsilon:
        return Sleft + Sright + (Sleft + Sright - S) / 15
    return adaptive_simpsons_rule(f, a, c, epsilon/2, Sleft, fa, fm, fd, n+1) + \
           adaptive_simpsons_rule(f, c, b, epsilon/2, Sright, fm, fb, fe, n+1)

def monte_carlo_integration(f, a, b, num_points=1000):
    points = np.random.uniform(a, b, num_points)
    values = f(points)
    return (b - a) * np.mean(values)

def double_integral(f, ax, bx, ay, by, nx=100, ny=100):
    x = np.linspace(ax, bx, nx)
    y = np.linspace(ay, by, ny)
    hx = (bx - ax) / (nx - 1)
    hy = (by - ay) / (ny - 1)
    integral = 0
    for i in range(nx):
        for j in range(ny):
            integral += f(x[i], y[j]) * hx * hy
    return integral

def simpsons_rule_with_error(f, a, b, n):
    h = (b - a) / n
    integral = f(a) + f(b)
    for i in range(1, n, 2):
        integral += 4 * f(a + i * h)
    for i in range(2, n-1, 2):
        integral += 2 * f(a + i * h)
    integral *= h / 3
    error = (b - a) * (b - a) * (b - a) * np.max([abs(f(a + i * h)) for i in range(n+1)]) / 180 / (n * n)
    return integral, error
