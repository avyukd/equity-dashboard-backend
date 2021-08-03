#create hello world fastapi app
from fastapi import FastAPI, Query
from utils import *
from typing import Optional
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the Server!"}

@app.get("/equities/quote")
async def quote(ticker: str, columns: Optional[List[str]] = Query(["marketCap","regularMarketPrice"])):
    return_dict = {}
    ticker_data = get_data(ticker)
    for col in columns:
        return_dict[col] = ticker_data[col]
    return return_dict

@app.get("/equities/valuation/commodities/{commodity}")
async def valuation(commodity: str, ticker: str, commodity_price: float, multiple: float = 1.0, 
                    discount_rate: float = 0.08, capex_mult: float = 1.0):
    commodity = commodity.lower()
    print("received multiplier:",capex_mult)
    if commodity == "uranium":
        return {"value": multiple * get_uranium_miner_valuation(ticker, commodity_price, discount_rate, capex_mult)}
    else:
        return {"value":0}

@app.get("/equities/valuation/growth")
async def growth(ticker: str, cagr: float, discount_rate: float = 0.08, 
                terminal_growth: float = 0.03, speed_of_convergence: float = 2.5):
    return {"value": get_growth_valuation(ticker, cagr, discount_rate, terminal_growth, speed_of_convergence)}