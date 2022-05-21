import numpy as np
from finite_difference_method import FiniteDifferenceMethod

if __name__ == '__main__':
    mesh = np.power(2, range(4, 13))
    fdm_ap = FiniteDifferenceMethod(r=0.01, sigma=0.2, K=100, T=1)
    price_ap, boundary_ap = fdm_ap.implicit_scheme(upper_bound=200, time_step=128, space_step=128)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
