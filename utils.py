import yfinance as yf
from uranium_miner_valuations import *
def get_data(ticker):
    s = yf.Ticker(ticker)
    return s.info

def get_uranium_miner_valuation(ticker, price, discount_rate=0.08):
    ticker = ticker.upper()
    if ticker == "GLATF":
        return get_global_atomic_valuation(price, discount_rate)
    elif ticker == "BNNLF":
        return get_bannerman_energy_valuation(price, discount_rate)
    elif ticker == "PALAF":
        return get_paladin_energy_valuation(price, discount_rate)
    else:
        return 0
