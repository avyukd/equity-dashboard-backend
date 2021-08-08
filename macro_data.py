from bs4 import BeautifulSoup
import requests
from datetime import datetime
import yfinance as yf
import pandas as pd
def get_fear_greed_index():
    response = requests.get("https://money.cnn.com/data/fear-and-greed/")
    soup = BeautifulSoup(response.text, "html.parser")
    html_text = str(soup.find("div", {"id":"needleChart"}))
    img_url = html_text.split("'")[1]
    return img_url

def get_indices():
    nasdaq = yf.Ticker("^IXIC").info
    sp500 = yf.Ticker("^GSPC").info
    dow = yf.Ticker("^DJI").info
    vix = yf.Ticker("^VIX").info
    nasdaq_pct_change = (nasdaq["regularMarketPrice"] - nasdaq["previousClose"])/nasdaq["previousClose"] * 100
    sp500_pct_change = (sp500["regularMarketPrice"] - sp500["previousClose"])/sp500["previousClose"] * 100
    dow_pct_change = (dow["regularMarketPrice"] - dow["previousClose"])/dow["previousClose"] * 100
    vix_pct_change = (vix["regularMarketPrice"] - vix["previousClose"])/vix["previousClose"] * 100
    return {"nasdaq":nasdaq_pct_change, "sp500":sp500_pct_change, "dow":dow_pct_change, "vix":vix_pct_change}
def date_helper(s):
    date_to_num = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
    #replace string
    s = s.replace(s[:3],str(date_to_num[s[:3]]))
    return s
def get_shiller_PE_data():
    url = "https://www.multpl.com/shiller-pe/table/by-month"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", {"id": "datatable"})
    rows = table.findAll("tr")
    data = []
    for row in rows:
        date = row.find("td", {"class":"left"})
        if date is not None:
            date = date.text
        pe = row.find("td", {"class":"right"})
        if pe is not None:
            pe = pe.text
        if date is not None and date != "":
            #turn date into a datetime object
            date = date_helper(date)
            date = datetime.strptime(date, "%m %d, %Y")
            data.append({"date":date, "cape":float(pe.replace("\n",""))})
    #reverse data
    data = data[::-1]
    return data

def date_helper_margin(s):
    date_to_num = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"June":6,"Jul":7,"Aug":8,
                "Sept":9,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
    month = date_to_num[s.split("-")[0]]
    day = 1
    raw_year = s.split("-")[1]
    if "9" == raw_year[0]:
        year = "19"+raw_year
    else:
        year = "20"+raw_year
    return datetime.strptime(str(month)+" "+str(day)+", "+str(year), "%m %d, %Y")
def get_margin_debt_data():
    url = "https://www.finra.org/investors/learn-to-invest/advanced-investing/margin-statistics"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    tables = soup.findAll("table", {"class": "rwd-table width100"})
    data = []
    for table in tables:
        rows = table.findAll("tr")
        eoy_debt = rows[-1]
        cols = eoy_debt.findAll("td")
        if len(cols) == 1:
            eoy_debt = rows[-2]
            cols = eoy_debt.findAll("td")
        if len(cols) >= 2:
            date = date_helper_margin(cols[0].text)
            debt = int(cols[1].text.replace(",",""))
            data.append({"date":date, "debt":debt})
    data = data[::-1]
    #turn data into dataframe and get percent change
    df = pd.DataFrame(data)
    df["debt_pct_change"] = df["debt"].pct_change()
    #remove first row of df
    df = df[1:]
    #turn df into array of dicts
    df = df.to_dict("records")
    return df
#print(get_indices())
print(get_margin_debt_data())