from bs4 import BeautifulSoup
import requests
from datetime import datetime
'''def get_berkshire_cash_over_time():
    brk = yf.Ticker("BRK-B")
    qbs = brk.quarterly_balance_sheet
    #get cash row of qbs dataframe
    cash_row = qbs.loc['Cash']
    #transpose the cash_row
    cash_row = cash_row.transpose()
    print(cash_row[:10])'''

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
print(get_shiller_PE_data())