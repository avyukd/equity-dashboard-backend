import yfinance as yf
from uranium_miner_valuations import *
from growth_valuations import *
import requests
from bs4 import BeautifulSoup

def get_data(ticker):
    s = yf.Ticker(ticker)
    return s.info

def get_growth_valuation(ticker, cagr, discount_rate, terminal_growth_rate, speed_of_convergence):
    ticker = ticker.upper()
    if ticker == "PLTR":
        return get_pltr_valuation(cagr, discount_rate, terminal_growth_rate, speed_of_convergence)
    else:
        return 0
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

def parse_SPUT_format(s):
    s = s.split(" ")[0]
    s = s.replace("$US", "")
    s = s.replace("%", "")
    s = s.replace(",", "")
    #cast to double rounded to 2 decimal places
    return round(float(s), 2)
def scrape_SPUT():
    url = "https://www.sprott.com/investment-strategies/physical-commodity-funds/uranium/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    #find all classes with class=fundHeader_title
    all_info = soup.find_all(class_="cell small-6 large-3 fundHeader_data")
    market_price = 0
    nav = 0
    premium = 0 
    total_lbs = 0
    total_nav = 0
    for info in all_info:
        t = info.find(class_="fundHeader_title").text
        d = " ".join(info.find(class_="fundHeader_value").text.split())
        if t == "Market Price":
            market_price = parse_SPUT_format(d)
        elif t == "NAV":
            nav = parse_SPUT_format(d)
        elif t == "Premium/Discount":
            premium = parse_SPUT_format(d)
        elif t == "Total Net Asset Value":
            total_nav = parse_SPUT_format(d)
        elif t == "Total lbs of U3O8":
            total_lbs = parse_SPUT_format(d)
    return {
        "market_price": market_price,
        "nav": nav,
        "premium": premium,
        "total_nav": total_nav,
        "total_lbs": total_lbs
    }

def parse_WNA_table():
    URL = "https://world-nuclear.org/information-library/facts-and-figures/uranium-production-figures.aspx"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find({"table"})
    table_head = table.find("thead")
    table_body = table.find("tbody")
    rows = table_body.find_all("tr")
    data = []
    for row in rows:
        heading = row.find("th").text
        cols = row.find_all("td")
        cols = [ele.text.strip().replace(",","") for ele in cols]
        data.append((heading, [ele for ele in cols if ele]))
    print(data)

parse_WNA_table()