from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime

from config import API_SECRET, API_KEY

#API_KEY = ""
#API_SECRET = ""
BASE_URL = "https://paper-api.alpaca.markets/v2"

ALPACA_CREDS = {
    
    "API_KEY":API_KEY,
    "API_SECRET":API_SECRET,
    "PAPER": True
}


class MLTrader(Strategy):
    #runs once when bot is started up
    def initialize(self, symbol:str="SPY", cash_at_risk:float=.5):
        self.symbol = symbol
        self.sleeptime = "24H"
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        
    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price,0)
        return cash, last_price, quantity
        
    
    #runs after everytick (new data from data source is recieved)
    def on_trading_iteration(self):
        
        cash, last_price, quantity = self.position_sizing()
        
        if cash > last_price:
            
            if self.last_trade == None:
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "buy",
                    type="bracket",
                    take_profit_price=last_price*1.10,
                    stop_loss_price=last_price*.95
                )
                self.submit_order(order)
                self.last_trade = "buy"
        return super().on_trading_iteration()


start_date = datetime(2023, 12, 10)
end_date = datetime(2023, 12, 15)

#creates instancce of alpaca, interacts with API for trading - 
# placing orders, viewing market data, checking account details
broker = Alpaca(ALPACA_CREDS)

strategy = MLTrader(name='mlstrat', broker=broker, 
                    parameters={"symbol":"SPY", "cash_at_risk":.5})

#how well it runs based on historic data
strategy.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters={"symbol":"SPY", "cash_at_risk":.5}
)
