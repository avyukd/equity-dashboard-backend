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

@app.get("/equities/valuation/{commodity}")
async def valuation(commodity: str, ticker: str, commodity_price: float, multiple: float = 1.0, 
                    discount_rate: float = 0.08):
    commodity = commodity.lower()
    if commodity == "uranium":
        return {"value": multiple * get_uranium_miner_valuation(ticker, commodity_price, discount_rate)}
    else:
        return {"value":0}
