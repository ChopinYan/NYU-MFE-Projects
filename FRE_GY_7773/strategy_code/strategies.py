from abc import ABC
import yfinance as yf
from factors import *
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from back_testing import DIRECTION, ForLoopBackTester
import logging


class BaseStrategy(ABC):
    """ base strategy class, used for inheritance """
    def fit(self, price):
        pass

    def predict(self, price):
        pass


class NaiveStrategy(BaseStrategy):
    """ Naive strategy class """
    def __init__(self):
        super().__init__()
        self.buy = True
        self.count = -1

    def fit(self, price):
        pass

    def predict(self, price):
        """ buy and sell every 5 days """
        self.count += 1
        if ((self.count % 5) == 0) and (self.buy is True):
            self.buy = False
            return DIRECTION.BUY
        elif ((self.count % 5) == 0) and (self.buy is False):
            self.buy = True
            return DIRECTION.SELL
        else:
            return DIRECTION.HOLD


class LogisticStrategy(BaseStrategy):
    """ Logistic Regression Strategy """
    def __init__(self):
        super().__init__()
        self.dataframe = pd.DataFrame()
        self.prev_price = None
        self.buy = True
        self.model = None
        self.prediction = None

    def fit(self, price_update):
        price = pd.DataFrame.from_records(
            [
                {
                    'label': 1 if self.prev_price is None or price_update['Close'] > self.prev_price else -1,
                    'price': price_update['Close'],
                    'volume': price_update['Volume'],
                    'open_close': price_update['Open'] - price_update['Close'],
                    'high_low': price_update['High'] - price_update['Low'],
                    'price_volume_deviation': price_update['price_vol_deviation'],
                    'opening_price_gap': price_update['opening_price_gap'],
                    'abnormal_volume': price_update['abnormal_volume'],
                    'volume_swing_deviation': price_update['volume_swing_deviation'],
                    'volume_reverse': price_update['volume_reverse'],
                    'price_reverse': price_update['price_reverse']
                }
            ]
        )

        self.dataframe = pd.concat([self.dataframe, price])
        self.prev_price = price.iloc[-1]['price']

        # fit model with data until previous day
        if len(self.dataframe) > 1200:
            self.model = LogisticRegression().fit(
                self.dataframe.drop(['label'], axis=1).iloc[:-1], self.dataframe['label'].iloc[:-1])

    def predict(self, price_update):
        price = pd.DataFrame.from_records(
            [
                {
                    'label': 1 if price_update['Close'] > self.prev_price else -1,
                    'price': price_update['Close'],
                    'volume': price_update['Volume'],
                    'open_close': price_update['Open'] - price_update['Close'],
                    'high_low': price_update['High'] - price_update['Low'],
                    'price_volume_deviation': price_update['price_vol_deviation'],
                    'opening_price_gap': price_update['opening_price_gap'],
                    'abnormal_volume': price_update['abnormal_volume'],
                    'volume_swing_deviation': price_update['volume_swing_deviation'],
                    'volume_reverse': price_update['volume_reverse'],
                    'price_reverse': price_update['price_reverse']
                    }
            ]
        )

        if self.model is not None:
            self.prediction = self.model.predict(price.drop(['label'], axis=1))
            if (self.prediction == 1) and (self.buy is True):
                self.buy = False
                return DIRECTION.BUY
            elif (self.prediction == -1) and (self.buy is False):
                self.buy = True
                return DIRECTION.SELL
            else:
                return DIRECTION.HOLD
        else:
            return DIRECTION.HOLD


class GradientBoostStrategy(BaseStrategy):

    def __init__(self):
        super().__init__()
        self.dataframe = pd.DataFrame()
        self.prev_price = None
        self.buy = True
        self.model = None
        self.prediction = None

    def fit(self, price_update):
        price = pd.DataFrame.from_records(
            [
                {
                    'label': 1 if self.prev_price is None or price_update['Close'] > self.prev_price else -1,
                    'price': price_update['Close'],
                    'volume': price_update['Volume'],
                    'open_close': price_update['Open'] - price_update['Close'],
                    'high_low': price_update['High'] - price_update['Low'],
                    'price_volume_deviation': price_update['price_vol_deviation'],
                    'opening_price_gap': price_update['opening_price_gap'],
                    'abnormal_volume': price_update['abnormal_volume'],
                    'volume_swing_deviation': price_update['volume_swing_deviation'],
                    'volume_reverse': price_update['volume_reverse'],
                    'price_reverse': price_update['price_reverse']
                }
            ]
        )

        self.dataframe = pd.concat([self.dataframe, price])
        self.prev_price = price.iloc[-1]['price']

        # fit model with data until previous day
        if len(self.dataframe) > 1200:
            self.model = GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=1.0,
                max_depth=1,
                random_state=0).fit(
                self.dataframe.drop(['label'], axis=1).iloc[:-1], self.dataframe['label'].iloc[:-1])

    def predict(self, price_update):
        price = pd.DataFrame.from_records(
            [
                {
                    'label': 1 if price_update['Close'] > self.prev_price else -1,
                    'price': price_update['Close'],
                    'volume': price_update['Volume'],
                    'open_close': price_update['Open'] - price_update['Close'],
                    'high_low': price_update['High'] - price_update['Low'],
                    'price_volume_deviation': price_update['price_vol_deviation'],
                    'opening_price_gap': price_update['opening_price_gap'],
                    'abnormal_volume': price_update['abnormal_volume'],
                    'volume_swing_deviation': price_update['volume_swing_deviation'],
                    'volume_reverse': price_update['volume_reverse'],
                    'price_reverse': price_update['price_reverse']
                    }
            ]
        )

        if self.model is not None:
            self.prediction = self.model.predict(price.drop(['label'], axis=1))
            if (self.prediction == 1) and (self.buy is True):
                self.buy = False
                return DIRECTION.BUY
            elif (self.prediction == -1) and (self.buy is False):
                self.buy = True
                return DIRECTION.SELL
            else:
                return DIRECTION.HOLD
        else:
            return DIRECTION.HOLD


def main(symbol="FB", nb_of_rows=1800, log_path=None, strategy=None, title="Naive"):
    """
    back testing
    :param log_path: str, default=None; path of logging file
    :param title: str; strategy name
    :param symbol: str; ticker name
    :param nb_of_rows: int; number of rows in training data
    :param strategy: Class; i.e. NaiveStrategy
    :return: plot and matrix
    """
    try:
        if log_path:
            std_filename = log_path
        else:
            std_filename = ".\\order_trace.log"
        logging.basicConfig(filename=std_filename, filemode='a',
                            format='%(asctime)s - %(message)s', level=logging.DEBUG)
        logging.info('')
        logging.info(f'Entering {title} strategy')

        # initialize
        back_tester = ForLoopBackTester(strategy)

        # select price volume data of facebook from yahoo finance
        ticker = yf.Ticker(symbol)

        # initialize single input data (of 1 min frequency)
        df_ticker = ticker.history(
            period='7d',
            interval='1m',
            start=None,
            end=None,
            actions=True,
            auto_adjust=True,
            back_adjust=False).drop(["Dividends", "Stock Splits"], axis=1)

        # initialize evaluation matrix for strategy performance
        matrix = pd.DataFrame(columns=["signal", "position", "close_price", "cash", "holdings", "total", "pnl"])

        # initialize dataframes for factors or parameters
        df_ticker["price_vol_deviation"] = price_volume_deviation(df_ticker.Close, df_ticker.Volume)
        df_ticker["opening_price_gap"] = opening_price_gap(df_ticker.Close, df_ticker.Open)
        df_ticker["abnormal_volume"] = abnormal_volume(df_ticker.Volume)
        df_ticker["volume_swing_deviation"] = volume_swing_deviation(df_ticker.Volume, df_ticker.High, df_ticker.Low)
        df_ticker["volume_reverse"] = volume_reverse(df_ticker.Volume)
        df_ticker["price_reverse"] = price_reverse(df_ticker.High, df_ticker.Close)
        df_ticker = df_ticker.dropna().reset_index()

        # initialize single input data (of 1 min frequency)
        for date in df_ticker.Datetime[:nb_of_rows]:
            price_information = dict(df_ticker[df_ticker.Datetime == date].iloc[0])

            # set buy or sell signal and run the strategy
            action = back_tester.on_market_data_received(price_information)
            back_tester.buy_sell_or_hold_something(price_information, action)

            # fill the data
            matrix.loc[date] = [
                action,
                back_tester.list_position[-1],
                price_information["Close"],
                back_tester.list_cash[-1],
                back_tester.list_holdings[-1],
                back_tester.list_total[-1],
                back_tester.list_total[-1] - 100000
            ]
        # print("PNL:%.2f" % (naive_back_tester.list_total[-1] - 10000))

        # sharpe ratio for the strategy
        sharpe_ratio = matrix["total"].pct_change().mean() / matrix["total"].pct_change().std()

        # initialize decay matrix
        dcy_mat = pd.DataFrame()
        buy_idx = matrix[(matrix["signal"] == "buy")].index
        for idx in buy_idx:
            idx_num = matrix.index.get_loc(idx)
            dcy_win = matrix.iloc[idx_num: idx_num + 5]["pnl"] - matrix.iloc[idx_num]["pnl"]
            dcy_win = dcy_win.reset_index()["pnl"]
            dcy_mat = pd.concat([dcy_mat, dcy_win], axis=1)
        sell_idx = matrix[(matrix["signal"] == "sell")].index
        for idx in sell_idx:
            idx_num = matrix.index.get_loc(idx)
            dcy_win = matrix.iloc[idx_num: idx_num + 5]["pnl"] - matrix.iloc[idx_num]["pnl"]
            dcy_win = -dcy_win.reset_index()["pnl"]
            dcy_mat = pd.concat([dcy_mat, dcy_win], axis=1)

        # plot decay
        dcy_mat.plot(
            legend=False, figsize=(10, 6), grid=True, title="Signal Decay" + title, xlabel="minute", ylabel="PnL"
        )

        logging.info(f'Leaving {title} strategy')
        return matrix, dcy_mat, sharpe_ratio

    except FileNotFoundError as nf_error:
        logging.error(f'Leaving {title} incomplete with errors')
        return f'ERROR: {str(nf_error)}'
    except KeyError as key_error:
        logging.error(f'Leaving {title} incomplete with errors')
        return f'ERROR: {key_error.args[0]}'
    except Exception as gen_exc:
        logging.error(f'Leaving {title} incomplete with errors')
        raise gen_exc


if __name__ == "__main__":
    matrix_naive, decay_naive, sr_naive = main(strategy=NaiveStrategy(), title="Naive")
    matrix_logit, decay_logit, sr_logit = main(strategy=LogisticStrategy(), title="Logistic")
    matrix_gbdt, decay_gbdt, sr_gbdt = main(strategy=GradientBoostStrategy(), title="GradientBoosting")

