from abc import ABC
from back_testing import DIRECTION


class BaseStrategy(ABC):
    """ abstract base strategy class, used for inheritance """
    def events(self, price):
        pass


class BuyHoldStrategy(BaseStrategy):
    """ derived class for buy and hold strategy """
    def __init__(self, back_testing_period):
        super().__init__()
        self.buy = True
        self.count = 0
        self.back_testing_period = back_testing_period

    def events(self, price):
        """ buy and then hold for the whole back testing period """
        self.count += 1
        if self.buy is True:
            self.buy = False
            return DIRECTION.BUY
        elif (self.buy is False) & (self.count == self.back_testing_period):
            return DIRECTION.SELL
        else:
            return DIRECTION.HOLD


class NaiveStrategy(BaseStrategy):
    """ derived class for Naive strategy """
    def __init__(self, back_testing_period):
        super().__init__()
        self.buy = True
        self.count = -1
        self.back_testing_period = back_testing_period

    def events(self, price):
        """ buy and sell every 5 days """
        self.count += 1
        if ((self.count % 5) == 0) and (self.buy is True):
            self.buy = False
            return DIRECTION.BUY
        elif ((self.count % 5) == 0) and (self.buy is False):
            self.buy = True
            return DIRECTION.SELL
        elif (self.buy is False) & (self.count == self.back_testing_period - 1):
            return DIRECTION.SELL
        else:
            return DIRECTION.HOLD


class MACDStrategy(BaseStrategy):
    """
    derived class for strategies using technical analysis
    ----------------
    i.e. MACD
    """
    def __init__(self, back_testing_period):
        super().__init__()
        self.back_testing_period = back_testing_period
        self.count = 0
        self.buy = True
        self.prev_macd_line = None
        self.prev_signal_line = None

    def events(self, price):
        """ gold cross: buy; death cross: sell """
        self.count += 1

        # get daily data
        macd_line = price["macd_line"]
        signal_line = price["signal_line"]

        # design trading strategies
        if (not self.prev_macd_line) & (not self.prev_signal_line):
            self.prev_macd_line = macd_line
            self.prev_signal_line = signal_line
            return DIRECTION.HOLD

        if (self.buy is True) & (macd_line > signal_line) & (self.prev_macd_line < self.prev_signal_line):
            self.prev_signal_line = signal_line
            self.prev_macd_line = macd_line
            self.buy = False
            return DIRECTION.BUY
        elif (self.buy is False) & (macd_line < signal_line) & (self.prev_macd_line > self.prev_signal_line):
            self.prev_signal_line = signal_line
            self.prev_macd_line = macd_line
            self.buy = True
            return DIRECTION.SELL
        elif (self.buy is False) & (self.count == self.back_testing_period):  # THE LAST ORDER SHOULD BE SELL ORDER
            return DIRECTION.SELL
        else:
            return DIRECTION.HOLD


class DonchainStrategy(BaseStrategy):
    """
    Derived class for Donchain Channel Strategy
    -------------------
    price higher than the highest within a rolling window: buy
    price lower than the lowest within a rolling window: sell
    """
    def __init__(self, back_testing_period):
        super().__init__()
        self.buy = True

    def events(self, price):
        # define channels
        high_line = price["high_line"]
        low_line = price["low_line"]

        # design trading strategy
        if (self.buy is True) & (price["High"] > high_line):
            self.buy = False
            return DIRECTION.BUY
        elif (self.buy is False) & (price["Low"] < low_line):
            self.buy = True
            return DIRECTION.SELL
        else:
            return DIRECTION.HOLD



