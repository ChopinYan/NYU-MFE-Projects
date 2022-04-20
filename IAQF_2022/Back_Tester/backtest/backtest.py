import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

IWV_QUOTE = "./backtest/data/IWV.pkl"
IWV_DIVIDEND = "./backtest/data/IWV_div.pkl"
RATE = "./backtest/data/RATE_0.pkl"  # RATE_0.pkl: assume interest rate=0


class Backtest:
    def __init__(self, signal, quote, rate, dividend,
                 strategy, start_date, end_date,
                 turnover=1, start_cash=1e6, fee=0, fillna=True):
        """

        :param signal: pd.DataFrame, columns=["sigdate", "signal"]
        :param quote: pd.DataFrame, columns=["sigdate", "open", "high", "low", "close"]
        :param rate: pd.DataFrame, columns=["sigdate", "rate"]
        :param dividend: pd.DataFrame, columns=["sigdate", "dividend"]
        :param strategy: function, input: signal {0, 1, -1}, output: weight
        :param start_date: str
        :param end_date: str
        :param turnover: int
        :param start_cash: int
        """

        self.signal = signal.set_index("sigdate")
        self.signal.sort_index(inplace=True)
        self.quote = quote.set_index("sigdate")
        self.quote.sort_index(inplace=True)
        self.rate = rate.set_index("sigdate")
        self.rate.sort_index(inplace=True)
        self.dividend = dividend.set_index("sigdate")
        self.dividend.sort_index(inplace=True)

        self.strategy = strategy

        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.start_cash = start_cash
        self.turnover = turnover
        self.fee = fee

        self.dates = self.quote.index
        self.dates = self.dates[(self.dates >= self.start_date) & (self.dates <= self.end_date)]
        self.day_count = 0

        self.signal = self.signal.reindex(self.dates)
        if fillna:
            self.signal = self.signal.fillna(method="ffill")
        self.rate = self.rate.reindex(self.dates).fillna(method="ffill")
        self.dividend = self.dividend.reindex(self.dates, fill_value=0)

        self.holding = pd.DataFrame(columns=["share", "price", "value"])  # index is date
        self.pre_holding = pd.DataFrame(columns=["share", "price"])
        self.trade = pd.DataFrame(columns=["sigdate", "share", "price"])
        self.summary = pd.DataFrame(columns=["cash", "value", "tot_asset"])  # index is date
        self.pre_summary = pd.DataFrame(columns=["cash", "value", "tot_asset"])

    def clear(self):
        self.holding = pd.DataFrame(columns=["share", "price", "value"])  # index is date
        self.pre_holding = pd.DataFrame(columns=["share", "price"])
        self.trade = pd.DataFrame(columns=["sigdate", "share", "price"])
        self.summary = pd.DataFrame(columns=["cash", "value", "tot_asset"])  # index is date
        self.pre_summary = pd.DataFrame(columns=["cash", "value", "tot_asset"])

    def run(self):
        for dt in self.dates:
            today_dividend = self.dividend.loc[dt, "dividend"]
            if self.day_count % self.turnover == 0:
                # execute trade / adjust holding
                today_signal = self.signal.loc[dt, "signal"]
                today_quote = self.quote.loc[dt]

                if self.day_count == 0:
                    pre_cash = self.start_cash
                    pre_asset = pre_cash
                    self.pre_holding = pd.Series({"share": 0, "price": today_quote.open})
                    last_rate = self.rate.iloc[0].rate
                else:
                    pre_cash = self.pre_summary.cash
                    pre_asset = self.pre_summary.tot_asset
                    last_rate = self.rate.shift().loc[dt, "rate"]

                pre_cash += pre_cash * last_rate
                pre_cash += today_dividend * self.pre_holding.share
                pre_asset += today_dividend * self.pre_holding.share

                if np.isnan(today_signal):
                    cash = pre_cash + self.pre_holding.share * today_quote.open \
                           - (abs(self.pre_holding.share) * today_quote.open) * self.fee
                    self.trade = self.trade.append({"sigdate": dt, "share": -self.pre_holding.share,
                                                    "price": today_quote.open}, ignore_index=True)
                    self.summary.loc[dt] = [cash, 0, cash]
                    self.pre_summary = self.summary.loc[dt]
                    self.holding.loc[dt] = [0, today_quote.close, 0]
                    self.pre_holding = self.holding.loc[dt, ["share", "price"]]
                    continue

                today_weight = self.strategy(today_signal)
                today_target = pre_asset * today_weight / self.pre_holding.price  # target share (no rounding)

                today_diff = today_target - self.pre_holding.share
                cash = pre_cash - today_diff * today_quote.open - (abs(today_diff) * today_quote.open) * self.fee
                value = today_target * today_quote.close

                if today_diff != 0:
                    self.trade = self.trade.append({"sigdate": dt, "share": today_diff, "price": today_quote.open},
                                                   ignore_index=True)
                self.summary.loc[dt] = [cash, value, cash + value]
                self.pre_summary = self.summary.loc[dt]
                self.holding.loc[dt] = [today_target, today_quote.close, value]
                self.pre_holding = self.holding.loc[dt, ["share", "price"]]

            else:
                today_quote = self.quote.loc[dt]
                last_rate = self.rate.shift().loc[dt, "rate"]  # get last day rate

                cash = self.pre_summary.cash * (1 + last_rate)
                cash += today_dividend * self.pre_holding.share
                today_holding = self.pre_holding.share
                value = today_holding * today_quote.close

                self.summary.loc[dt] = [cash, value, cash + value]
                self.pre_summary = self.summary.loc[dt]
                self.holding.loc[dt] = [today_holding, today_quote.close, value]
                self.pre_holding = self.holding.loc[dt, ["share", "price"]]

            self.day_count += 1

    def show_info(self, rf=0, benchmark=None):
        print(f"start date: \t\t{str(self.start_date)}")
        print(f"end date: \t\t{str(self.end_date)}")
        print(f"day count: \t\t{len(self.dates)}")
        print(f"start cash: \t\t{self.start_cash}")
        print(f"cumulative return: \t{self._calc_cumulative_ret()[-1]}")
        print(f"annualized return: \t{self.calc_comp_ann_ret()}")
        print(f"annualized sharpe: \t{self.calc_sharpe(rf)}")
        if benchmark is not None:
            print(f"annualized IR: \t{self.calc_ir(benchmark)}")
        print(f"annualized sortino: \t{self.calc_sortino(rf)}")
        print(f"calmar ratio: \t{self.calc_calmar()}")
        print(f"max drawndown: \t{self.calc_maxdrawdown()}")

    def show_result(self, benchmark):
        fig = plt.figure(figsize=(14, 6*4))
        gs = GridSpec(5, 1, wspace=0.1, hspace=0.1)

        ax_return_sheet = plt.subplot(gs[:2, :])
        self.plot_cumulative_ret(benchmark=benchmark, ax=ax_return_sheet)

        ax_signal = plt.subplot(gs[2, :], sharex=ax_return_sheet)
        self.plot_signal(ax=ax_signal)

        ax_turnover = plt.subplot(gs[3, :], sharex=ax_return_sheet)
        self.plot_turnover(ax=ax_turnover)

        ax_drawdown = plt.subplot(gs[4, :], sharex=ax_return_sheet)
        self.plot_maxdrawdown(ax=ax_drawdown)

    def plot_nav(self, ax=None):
        if ax is None:
            ax = plt.gca()
        ax.plot(self.summary.tot_asset)

    def plot_cumulative_ret(self, benchmark=None, ax=None):
        if ax is None:
            ax = plt.gca()

        ax.plot(self._calc_cumulative_ret(), label="strategy")

        if benchmark is not None:
            bench_ret = self.__calc_cumulative_ret(benchmark.loc[self.start_date:self.end_date])
            ax.plot(bench_ret, label="benchmark")

        plt.legend()

    def plot_daily_ret(self, ax=None):
        if ax is None:
            ax = plt.gca()
        ax.plot(self._calc_daily_ret())

    def plot_maxdrawdown(self, ax=None):
        if ax is None:
            ax = plt.gca()
        ax.plot(self._calc_drawdown(), label="underwater")
        plt.legend()

    def plot_signal(self, ax=None):
        if ax is None:
            ax = plt.gca()
        ax.plot(self.signal, label="signal")
        plt.legend()

    def plot_turnover(self, ax=None):
        if ax is None:
            ax = plt.gca()

        turnover = self._calc_turnover().fillna(0)
        ax.bar(turnover.index, turnover, label="turnover")
        ax.plot(turnover.rolling(60).mean(), "r", label="turnover (60day average)")
        plt.legend()

    @staticmethod
    def __calc_daily_ret(price):
        return price / price.shift() - 1

    def _calc_daily_ret(self):
        nav = self.summary.tot_asset
        return self.__calc_daily_ret(nav)

    @staticmethod
    def __calc_cumulative_ret(price):
        return price / price.iloc[0] - 1

    def _calc_cumulative_ret(self):
        return self.summary.tot_asset / self.start_cash - 1

    def _calc_ann_ret(self):
        return self._calc_daily_ret().mean() * 252  # arithmetic mean

    def calc_comp_ann_ret(self):
        cumu_ret = self._calc_cumulative_ret()[-1]
        n = len(self.dates)
        return (cumu_ret + 1)**(252/n) - 1  # compound

    def calc_sharpe(self, rf=0):
        daily_ret = self._calc_daily_ret() - ((rf+1)**(1/252) - 1)
        return daily_ret.mean() / daily_ret.std() * np.sqrt(252)

    def calc_ir(self, benchmark):
        daily_ret = self._calc_daily_ret()
        bench_ret = self.__calc_daily_ret(benchmark)
        excess_ret = daily_ret - bench_ret
        return excess_ret.mean() / excess_ret.std() * np.sqrt(252)

    def calc_sortino(self, rf=0):
        daily_ret = self._calc_daily_ret() - ((rf+1)**(1/252) - 1)
        return daily_ret.mean() / daily_ret[daily_ret < 0].std() * np.sqrt(252)

    def calc_calmar(self):
        return self.calc_comp_ann_ret() / self.calc_maxdrawdown()

    def _calc_drawdown(self):
        nav = self.summary.tot_asset
        dd = nav / nav.cummax() - 1
        return dd

    def calc_maxdrawdown(self):
        dd = self._calc_drawdown()
        return -dd.min()

    def _calc_turnover(self):
        trade_value = self.trade.copy()
        trade_value["value"] = abs(trade_value.share * trade_value.price)
        trade_value = trade_value.groupby("sigdate").value.sum()
        trade_value = trade_value.reindex(self.dates, fill_value=0)

        port_value = self.summary["tot_asset"].shift()
        port_value.iloc[0] = self.start_cash

        return trade_value / port_value


class EasyBacktest(Backtest):
    def __init__(self, signal, start_date, end_date, strategy="ls2", start_cash=1e6, fillna=True):
        """

        :param signal: pd.DataFrame, columns=["sigdate", "signal"]
        :param strategy: str, ["l2", "l3", "ls2", "ls3"]
            l2: long-out of market strategy with 2 clusters
            l3: long-out of market strategy with 3 clusters
            ls2: long-short strategy with 2 clusters
            ls3: long-short strategy with 3 clusters
        :param start_date: str "yyyy-mm-dd"
        :param end_date: str "yyyy-mm-dd"
        :param fillna: bool default True, whether fill na value in signal
        """
        quote = pd.read_pickle(IWV_QUOTE)
        dividend = pd.read_pickle(IWV_DIVIDEND)
        rate = pd.read_pickle(RATE)

        if strategy == "l2":
            strategy_in = self.__long_2
        elif strategy == "l3":
            strategy_in = self.__long_3
        elif strategy == "ls2":
            strategy_in = self.__long_short_2
        elif strategy == "ls3":
            strategy_in = self.__long_short_3
        else:
            raise

        super().__init__(signal, quote, rate, dividend, strategy_in, start_date, end_date,
                         start_cash=start_cash, fillna=fillna)

    def run(self, rf=0):
        super().clear()
        super().run()
        super().show_info(rf, benchmark=self.quote.close)
        super().show_result(self.quote.close)

    def show_result(self, rf):
        super().show_info(rf)
        super().show_result(self.quote.close)

    @staticmethod
    def __long_short_2(signal):
        """
        long-short strategy for 2 cluster. return target weight in IWV
        """
        if signal == 1:
            return 1
        elif signal == 0:
            return -1
        else:
            raise

    @staticmethod
    def __long_short_3(signal):
        """
        long-short strategy for 3 cluster. return target weight in IWV
        """
        if signal == 1:
            return 1
        elif signal == 0:
            return 0
        elif signal == -1:
            return -1
        else:
            raise

    @staticmethod
    def __long_2(signal):
        """
        long-out of market strategy for 2 cluster. return target weight in IWV
        """
        if signal == 1:
            return 1
        elif signal == 0:
            return 0
        else:
            raise

    @staticmethod
    def __long_3(signal):
        """
        long-out of market strategy for 3 cluster. return target weight in IWV
        """
        if signal == 1:
            return 1
        elif signal == 0 or signal == -1:
            return 0
        else:
            raise
