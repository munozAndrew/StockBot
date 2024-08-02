from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime

from config import API_SECRET, API_KEY

#API_KEY = ""
#API_SECRET = ""
BASE_URL = ""

ALPACA_CREDS = {
    
    "API_KEY":API_KEY,
    "API_SECRET":API_SECRET,
    "PAPER": True
}