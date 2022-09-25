import math
import pandas as pd
import scipy.stats


N_WEEKS_PER_YEAR = 50
N_DAYS_PER_YEAR = 252


def annualized_return(ret, period=N_DAYS_PER_YEAR):
    return ret.mean() * period


def annualized_volatility(ret, period=N_DAYS_PER_YEAR):
    return ret.std() * math.sqrt(period)


def sharpe_ratio(ret, period=N_DAYS_PER_YEAR):
    return ret.mean() / ret.std() * math.sqrt(period)


def max_drawdown(ret):
    cum_return = ret.cumsum()
    cum_return = pd.Series([0] + list(cum_return.values))
    n = len(cum_return)
    drawdown = [0] * n
    for i in range(1, n):
        drawdown[i] = cum_return.iloc[i] - max(cum_return.iloc[:i])
    mdd = min(drawdown)
    return mdd


def z_score(ret, size):
    return ret.mean() / ret.std() * math.sqrt(size)


def p_value(ret, size):
    tscore = z_score(ret, size)
    return scipy.stats.norm.sf(abs(tscore))
