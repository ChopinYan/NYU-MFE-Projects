import numpy as np


def tridiagonal_system_solver(a, b, c, d):
    """
    tridiagonal_system_solver refer to 6083
    :param a: np.array or list; a in matrix A
    :param b: np.array or list; b in matrix A
    :param c: np.array or list; c in matrix A
    :param d: np.array or list; right vector B
    :return:
    """
    # n is the length of the right vector
    n = len(d)

    # modify first row coefficients
    c, d = c.copy(), d.copy()
    c[0] = c[0] / b[0]
    d[0] = d[0] / b[0]

    # loop
    for i in range(1, n - 1):
        temp = b[i] - a[i - 1] * c[i - 1]
        c[i] = c[i] / temp
        d[i] = (d[i] - a[i - 1] * d[i - 1]) / temp

    # modify last row coefficients
    d[n-1] = (d[n-1] - a[n-2] * d[n-2]) / (b[n-1] - a[n-2] * c[n-2])
    x = d

    # back substitute
    for i in range(n - 2, -1, -1):
        x[i] = d[i] - c[i] * x[i + 1]

    return x

