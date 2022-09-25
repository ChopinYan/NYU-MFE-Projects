import logging

import numpy as np
import pandas as pd
import yfinance as yf
from tqdm import tqdm

from back_testing import BackTester
from technical_strategies import (
    MACDStrategy,
    BuyHoldStrategy,
    DonchainStrategy
)
from utils import (
    annualized_return,
    annualized_volatility,
    sharpe_ratio,
    max_drawdown,
    z_score,
    p_value
)


def main(investment=20000, symbol="TSLA", log_path=None, strategy=None):
    """
    back testing
    :param investment: int; initial investment
    :param log_path: str, default=None; path of logging file
    :param symbol: str; ticker name
    :param strategy: abc.ABCMeta; trading strategy
    :return:
    """
    try:
        if log_path:
            std_filename = log_path
        else:
            std_filename = ".\\order_trace.log"
        logging.basicConfig(filename=std_filename, filemode='a',
                            format='%(asctime)s - %(message)s', level=logging.DEBUG)
        logging.info('')
        logging.info(f'Entering strategy')

        # select price volume data of facebook from yahoo finance
        ticker = yf.Ticker(symbol)

        # initialize single input data (of 1 min frequency)
        df_ticker = ticker.history(
            period='max',
            interval='1d',
            start=None,
            end="2022-09-20",
            actions=True,
            auto_adjust=True,  # Adj Close
            back_adjust=False
        ).drop(["Dividends", "Stock Splits"], axis=1)

        # initialize evaluation matrix for strategy performance
        matrix = pd.DataFrame(
            columns=["signal", "position", "close_price", "cash", "holdings", "total", "pnl", "cum_return"]
        )

        # initialize dataframes for MACD strategy
        df_ticker["ema_12"] = df_ticker["Close"].ewm(span=12, adjust=True).mean()
        df_ticker["ema_26"] = df_ticker["Close"].ewm(span=26, adjust=True).mean()
        df_ticker["macd_line"] = df_ticker["ema_12"] - df_ticker["ema_26"]
        df_ticker["signal_line"] = df_ticker["macd_line"].ewm(span=9, adjust=True).mean()

        # initialize dataframes for Donchain Channel strategy
        df_ticker["high_line"] = df_ticker["High"].rolling(20).max()
        df_ticker["low_line"] = df_ticker["Low"].rolling(20).min()

        df_ticker = df_ticker.dropna().reset_index()

        # initialize
        back_tester = BackTester(strategy=strategy(len(df_ticker)), cash=investment)

        # initialize single input data (of daily frequency)
        for date in tqdm(df_ticker.Date, postfix="Strategy Operating"):
            price_data = dict(df_ticker[df_ticker.Date == date].iloc[0])

            # set buy or sell signal and run the strategy
            action = back_tester.order_instruction(price_data)
            back_tester.order_execution(price_data, action)

            # fill the data
            matrix.loc[date] = [
                action,
                back_tester.list_position[-1],
                price_data["Close"],
                back_tester.list_cash[-1],
                back_tester.list_holdings[-1],
                back_tester.list_total[-1],
                back_tester.list_total[-1] - investment,
                (back_tester.list_total[-1] - investment) / investment
            ]

        # indicators for the strategy
        ret = matrix["pnl"].diff() / investment
        signal_size = np.minimum(
                len(matrix[matrix.signal == "sell"]),
                len(matrix[matrix.signal == "buy"])
            )
        indicators = pd.DataFrame({
            "annualized_return": [annualized_return(ret)],
            "annualized_volatility": [annualized_volatility(ret)],
            "total_return": [matrix["cum_return"].iloc[-1]],
            "annual_sharpe_ratio": [sharpe_ratio(ret)],
            "maximum_drawdown": [max_drawdown(ret)],
            "number_round_trip": [signal_size],
            "z_score": [z_score(ret, signal_size * 2)],
            "p_value": [p_value(ret, signal_size * 2)]
        })

        logging.info(f'Leaving strategy')
        return df_ticker, matrix, indicators  # , sharpe_ratio

    except FileNotFoundError as nf_error:
        logging.error(f'Leaving strategy incomplete with errors')
        return f'ERROR: {str(nf_error)}'
    except KeyError as key_error:
        logging.error(f'Leaving strategy incomplete with errors')
        return f'ERROR: {key_error.args[0]}'
    except Exception as gen_exc:
        logging.error(f'Leaving strategy incomplete with errors')
        raise gen_exc


if __name__ == "__main__":
    df_macd, matrix_macd, idx_macd = main(
        investment=20000,
        symbol="TSLA",
        log_path=None,
        strategy=MACDStrategy
    )  # , sr_macd

    idx_macd.to_csv("indicators.csv")
    matrix_macd.to_csv("matrix.csv")

    df_bh, matrix_bh, idx_bh = main(
        investment=20000,
        symbol="TSLA",
        log_path=None,
        strategy=BuyHoldStrategy
    )

    df_dc, matrix_dc, idx_dc = main(
        investment=20000,
        symbol="TSLA",
        log_path=None,
        strategy=DonchainStrategy
    )
