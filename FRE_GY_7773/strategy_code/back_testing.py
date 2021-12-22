import logging


class DIRECTION:
    BUY = 1
    SELL = -1
    HOLD = 0


class ForLoopBackTester:

    def __init__(self, strategy=None, commission=0.00025):
        self.list_position = []
        self.list_cash = []
        self.list_holdings = []
        self.list_total = []

        self.long_signal = False
        # default two sides commissions
        self.commission = commission
        self.position = 0
        self.cash = 100000
        self.total = 0
        self.holdings = 0

        self.market_data_count = 0
        self.prev_price = None
        self.statistical_model = None
        # self.historical_data = pd.DataFrame(columns=['Trade', 'Price', 'OpenClose', 'HighLow'])
        self.strategy = strategy

    def on_market_data_received(self, price_update):
        if self.strategy:
            self.strategy.fit(price_update)
            predicted_value = self.strategy.predict(price_update)
        else:
            predicted_value = DIRECTION.HOLD

        if predicted_value == DIRECTION.BUY:
            return 'buy'
        if predicted_value == DIRECTION.SELL:
            return 'sell'
        return 'hold'

    def buy_sell_or_hold_something(self, price_update, action):
        if action == 'buy':
            cash_needed = 10 * price_update['Close'] * (1 + self.commission)  # commission
            if self.cash - cash_needed >= 0:
                logging.info(f'{str(price_update["Datetime"])} '
                             f'send buy order for 10 shares price={price_update["Close"]}')
                self.position += 10
                self.cash -= cash_needed
            else:
                logging.info('buy impossible because not enough cash')

        if action == 'sell':
            position_allowed = 10
            if self.position - position_allowed >= 0:  # -position_allowed??
                logging.info(f'{str(price_update["Datetime"])} '
                             f'send sell order for 10 shares price={price_update["Close"]}')
                self.position -= position_allowed
                self.cash -= -position_allowed * price_update['Close'] * (1 + self.commission)  # commission
            else:
                logging.info('buy impossible because not enough cash')

        self.holdings = self.position * price_update['Close']
        self.total = (self.holdings + self.cash)
        # print('%s total=%d, holding=%d, cash=%d' %
        #       (str(price_update['date']),self.total, self.holdings, self.cash))

        self.list_position.append(self.position)
        self.list_cash.append(self.cash)
        self.list_holdings.append(self.holdings)
        self.list_total.append(self.holdings + self.cash)
