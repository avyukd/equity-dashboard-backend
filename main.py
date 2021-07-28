#create hello world fastapi app
from fastapi import FastAPI, Query
from utils import *
from typing import Optional
from typing import List

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the Server!"}

@app.get("/equities/quote")
async def quote(ticker: str, columns: Optional[List[str]] = Query(["marketCap"])):
    return_dict = {}
    ticker_data = get_data(ticker)
    for col in columns:
        return_dict[col] = ticker_data[col]
    return return_dict

@app.get("/equities/valuation/uranium")
async def valuation(ticker: str, uranium_price: float):
    return {"value": get_uranium_miner_valuation(ticker, uranium_price)}
