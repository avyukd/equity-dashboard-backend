import yfinance as yf
from uranium_miner_valuations import *

def get_data(ticker):
    s = yf.Ticker(ticker)
    return s.info

def get_uranium_miner_valuation(ticker, price, discount_rate=0.08,capex_mult=1.0):
    ticker = ticker.upper()
    if ticker == "GLATF":
        return get_global_atomic_valuation(price, discount_rate, capex_mult)
    elif ticker == "BNNLF":
        return get_bannerman_energy_valuation(price, discount_rate, capex_mult)
    elif ticker == "PALAF":
        return get_paladin_energy_valuation(price, discount_rate, capex_mult)
    elif ticker == "DNN":
        return get_denison_mines_valuation(price, discount_rate, capex_mult)
    elif ticker == "URG":
        return get_ur_energy_valuation(price, discount_rate, capex_mult)
    elif ticker == "AZZUF":
        return get_azarga_valuation(price, discount_rate, capex_mult)
    else:
        return 0
