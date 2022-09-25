import logging


class DIRECTION:
    BUY = 1
    SELL = -1
    HOLD = 0


class BackTester:
    def __init__(self, strategy=None, cash=20000, commission=0.00025):
        self.commission = commission  # default two sides commissions
        self.position = 0
        self.cash = cash
        self.total = 0
        self.holdings = 0
        self.size = 100  # default size 100 shares per order

        self.list_position = []
        self.list_cash = []
        self.list_holdings = []
        self.list_total = []

        self.strategy = strategy

    def order_instruction(self, price_update):
        if self.strategy:
            predicted_value = self.strategy.events(price_update)
        else:
            predicted_value = DIRECTION.HOLD

        if predicted_value == DIRECTION.BUY:
            return 'buy'
        elif predicted_value == DIRECTION.SELL:
            return 'sell'
        else:
            return 'hold'

    def order_execution(self, price_update, action):
        if action == 'buy':
            # default 100 shares per order
            cash_needed = self.size * price_update['Close'] * (1 + self.commission)  # commission
            if self.cash - cash_needed >= 0:
                logging.info(f"""{str(price_update["Date"])} send buy order 
                    for {self.size} shares price={price_update["Close"]} """)
                self.position += self.size
                self.cash -= cash_needed
            else:
                logging.info('buy impossible because not enough cash')
                raise Exception('buy impossible because not enough cash')

        if action == 'sell':
            position_allowed = self.size
            if self.position - position_allowed >= 0:
                logging.info(f""" {str(price_update["Date"])} send sell order 
                    for {self.size} shares price={price_update["Close"]} """)
                self.position -= position_allowed
                self.cash += position_allowed * price_update['Close'] * (1 - self.commission)
            else:
                logging.info('sell impossible because not enough positions')
                raise Exception('buy impossible because not enough cash')

        self.holdings = self.position * price_update['Close']
        self.total = self.holdings + self.cash

        self.list_position.append(self.position)
        self.list_cash.append(self.cash)
        self.list_holdings.append(self.holdings)
        self.list_total.append(self.total)
