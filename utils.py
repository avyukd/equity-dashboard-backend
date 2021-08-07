import yfinance as yf
from uranium_miner_valuations import *
from growth_valuations import *
import requests
from bs4 import BeautifulSoup
import pickle 
import json



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

def get_supply_data(long_term_underfeeding,
    paladinFlag=False,globalFlag=False,mcarthurFlag=False):
    #open pickle
    with open("uranium_supply_demand.json", "r") as f:
        data = json.load(f)
    years = range(2016, 2031)
    toret = []
    supplyData = []
    for y in years:
        supplyData.append({'year':y, 'supply':6})
    toret.append({"source":"MOX", "supplyData": supplyData})
    supplyData = []
    for y in years:
        if y <= 2020:
            s = data['supply_historical']["Underfeeding"][str(y)]
            supplyData.append({"year": y, "supply": s})
        else:
            supplyData.append({"year":y, "supply": long_term_underfeeding})
    toret.append({"source":"Underfeeding", "supplyData": supplyData})
    supplyData = []
    for y in years:
        s = data['supply_historical']["Mined Supply"][str(y)]
        if y > 2020:
            if paladinFlag:
                s += data["paladin_production"][str(y)]
            if globalFlag:
                s += data["global_production"][str(y)]
            if mcarthurFlag:
                s += data["mcarthur_production"][str(y)]
        supplyData.append({"year": y, "supply": s})
    toret.append({"source":"Mined Supply", "supplyData": supplyData})
    return toret

def get_demand_data(growth_rate):
    #open uranium_supply_demand.json
    with open("uranium_supply_demand.json", "r") as f:
        data = json.load(f)
    years = range(2016, 2031)
    toret = []
    lastyr_demand = 0
    for y in years:
        if y <= 2020:
            demand = data['demand'][str(y)]
            toret.append({"year": y, "demand": demand})
            lastyr_demand = demand
        else:
            demand = lastyr_demand * (1 + growth_rate)
            toret.append({"year": y, "demand": demand})
            lastyr_demand = demand
    return toret

'''
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
    retobj = []
    for line in data[:2]:
        country_name = line[0]
        country_data = line[1]
        cnt = 0
        country_obj = {}
        fd = []
        for year in range(2010, 2020, 1):
            tonnes_U = float(country_data[cnt])
            pounds_U = 2204.6 * tonnes_U
            Mlbs_U = pounds_U / 1000000
            fd.append({"year": year, "supply" : Mlbs_U})
            cnt+=1
        country_obj["country"] = country_name
        country_obj["supplyData"] = fd
        retobj.append(country_obj)

    yearly_totals = {}
    for line in data[2:-3]:
        country_data = line[1]
        cnt = 0
        for year in range(2010, 2020, 1):
            tonnes_U = float(country_data[cnt])
            pounds_U = 2204.6 * tonnes_U
            Mlbs_U = pounds_U / 1000000
            if year not in yearly_totals:
                yearly_totals[year] = Mlbs_U
            else:
                yearly_totals[year] += Mlbs_U
            cnt+=1
    ows = []
    for year in range(2010, 2020, 1):
        ows.append({"year":year, "supply":yearly_totals[year]})
    other_nations_obj = {}
    other_nations_obj["country"] = "Other Nations"
    other_nations_obj["supplyData"] = ows
    retobj.append(other_nations_obj)
    tmd = [] 
    for total_mined_demand in data[-2][1]:
        total_mined_demand_tonnes_U = float(total_mined_demand)
        total_mined_demand_pounds_U = 2204.6 * total_mined_demand_tonnes_U
        total_mined_demand_Mlbs_U = total_mined_demand_pounds_U / 1000000
        tmd.append(total_mined_demand_Mlbs_U)   
    ''''''pwd = []
    for percent_world_demand in data[-1][1]:
        percent_world_demand = float(percent_world_demand.replace("%", ""))/100
        pwd.append(percent_world_demand)
    total_demand = []
    for i in range(len(pwd)):
        total_demand.append(tms[i] / pwd[i])''''''
    print(data[-2][1])
    td = []
    cnt = 0
    for year in range(2010, 2020, 1):
        td.append({"year": year, "demand" : tmd[cnt]})
        cnt+=1
    print(td)
    #save retobj with pickle
    with open("wna_supply_data.pkl", "wb") as f:
        pickle.dump(retobj, f)
    #save td with pickle
    with open("wna_demand_data.pkl", "wb") as f:
        pickle.dump(td, f)
'''

#parse_WNA_table()
print(get_supply_data(10))
