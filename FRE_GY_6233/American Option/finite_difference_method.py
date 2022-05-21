import numpy as np
import matplotlib.pyplot as plt
from tdma_solver import tridiagonal_system_solver


class AmericanPut:
    def __init__(self, K, r, sigma, T):
        """
        class for American put
        :param K:
        :param r:
        :param sigma:
        :param T:
        """
        self.K = K
        self.r = r
        self.sigma = sigma
        self.T = T

    def payoff(self, s):
        return max(self.K - s, 0.0)


class FiniteDifferenceMethod(AmericanPut):

    def __init__(self, K, r, sigma, T):
        """

        :param K:
        :param r:
        :param sigma:
        :param T:
        """
        super().__init__(K, r, sigma, T)
        # private member initialization
        self.upper_bound = None
        self.time_step = None
        self.space_step = None
        self.dt = None
        self.dx = None
        self.time_mesh = None
        self.space_mesh = None

        self.intrinsic_value = None
        self.a = None
        self.b = None
        self.c = None

        self.real_value = None
        self.free_boundary = None

    def implicit_scheme(self, upper_bound, time_step, space_step):
        """

        :param upper_bound:
        :param time_step:
        :param space_step:
        :return:
        """
        # Private member definition
        self.upper_bound = upper_bound
        self.time_step = time_step
        self.space_step = space_step
        self.dt = self.T / self.time_step
        self.dx = self.upper_bound / self.space_step
        self.time_mesh = np.linspace(0, self.T, self.time_step + 1)
        self.space_mesh = np.linspace(0, self.upper_bound, self.space_step + 1)
        # self.intrinsic_value = np.maximum(self.K - self.space_mesh, 0.0)
        self.intrinsic_value = np.array([self.payoff(s) for s in self.space_mesh])

        # Set vector a, b, c in the linear system
        self.a = [-0.5 * self.dt * (self.sigma * i) ** 2 for i in range(2, self.space_step)]
        self.b = [1 + self.dt * (self.r + self.r * i + (self.sigma * i) ** 2) for i in range(1, self.space_step)]
        self.c = [self.dt * (-self.r * i - 0.5 * (self.sigma * i) ** 2) for i in range(1, self.space_step - 1)]
        d = self.intrinsic_value[1:-1].copy()
        self.free_boundary = [self.K]

        for t in range(self.time_step - 1, -1, -1):

            # Adjust the first mesh for right-hand side vector
            d[0] -= (-0.5 * self.dt * self.sigma**2) * self.K * np.exp(-self.r * self.time_mesh[t+1])

            # Solve tridiagonal system
            result = tridiagonal_system_solver(self.a, self.b, self.c, d)

            # Get maximum of intrinsic value and solution of tridiagonal system
            d = np.maximum(result, self.intrinsic_value[1:-1])

            # for a given time t:
            # s is lower at the beginning, payoff of a put would be much higher
            # for d using maximum, at the beginning the value is equal to the intrinsic value (payoff)
            # we need to find the first index in d where the value is larger than intrinsic value
            # the first index where d != intrinsic value is the the prise with no early exercise: free boundary
            # e.g.
            # d = [3, 4, 5, 6, 7, 7, 8, 9, 10]
            # u = [3, 4, 5, 6, 7, 8, 9, 10, 11]
            # at index 4 the value is u instead of payoff, first index with no early exercise.
            boundary_index = np.where(d != self.intrinsic_value[1:-1])[0][0]
            self.free_boundary.append(self.space_mesh[boundary_index])

        # Prices according to the implicit method
        self.real_value = np.concatenate(([self.intrinsic_value[0]], d, [self.intrinsic_value[-1]]))
        self.free_boundary = self.free_boundary[::-1]

        return self.real_value, self.free_boundary

    def plot_real_value_boundary(self):
        # Canvas initialization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))
        fig.suptitle(f"Implicit finite difference with {self.time_step} time step and {self.space_step} space step")

        # Plot of the option price
        ax1.plot(self.space_mesh, self.real_value, label="Option price")
        ax1.plot(self.space_mesh, self.intrinsic_value, "--", label="Intrinsic value")
        ax1.set_title("Put option price")
        ax1.set_xlabel("Stock price")
        ax1.set_ylabel("Put price")
        ax1.legend(loc="best")

        # Plot of the free boundary
        ax2.plot(self.time_mesh, self.free_boundary)
        ax2.set_title("Free boundary")
        ax2.set_xlabel("Time to maturity (in years)")
        ax2.set_ylabel("Stock price")




