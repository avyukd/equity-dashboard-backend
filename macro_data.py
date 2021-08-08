from bs4 import BeautifulSoup
import requests

def get_berkshire_cash_over_time():
    brk = yf.Ticker("BRK-B")
    qbs = brk.quarterly_balance_sheet
    #get cash row of qbs dataframe
    cash_row = qbs.loc['Cash']
    #transpose the cash_row
    cash_row = cash_row.transpose()
    print(cash_row[:10])

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
            data.append({"date":date, "cape":float(pe.replace("\n",""))})
    return data
print(get_shiller_PE_data())