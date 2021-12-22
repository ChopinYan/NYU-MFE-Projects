import pandas as pd


def price_volume_deviation(price, volume, win=10):
    """
    deviation of price and volume
    = -1 * corr(price(last 10 days), volume(last 10 days))
    :param price:
    :param volume:
    :param win:
    :return:
    """
    factor = price.rolling(win).corr(volume)
    return factor


def opening_price_gap(close_price, open_price):
    """
    gap between today's open price and previous day's close price
    = open_price(today) / close_price(last day)
    :param close_price:
    :param open_price:
    :return:
    """
    factor = open_price / close_price.shift(1)
    return factor


def abnormal_volume(volume, win=10):
    """
    abnormal volume within previous 10 days
    = -1 volume(today) / mean(volume (last 10 days))
    :param win:
    :param volume:
    :return:
    """
    factor = volume / volume.rolling(win).mean()
    return factor


def volume_swing_deviation(volume, high, low, win=10):
    """
    = -1 * corr(high(last 10 days) / low(last 10 days), volume(last  10 days))
    :param volume:
    :param high:
    :param low:
    :param win:
    :return:
    """
    amplitude = high / low
    factor = -1 * amplitude.rolling(win).corr(volume)
    return factor


def volume_reverse(volume, win=10):
    """
    = ts_min(-volume, 10)
    :param win:
    :param volume:
    :return:
    """
    factor = -volume.rolling(win).min()
    return factor


def price_reverse(high, close, win=10):
    """
    ts_corr(-high, log(close), 5)
    :param high:
    :param close:
    :param win:
    :return:
    """
    factor = high.rolling(win).corr(close)
    return factor


