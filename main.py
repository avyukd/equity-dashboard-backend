#create hello world fastapi app
from macro_data import *
from fastapi import FastAPI, Query, Depends, HTTPException
from utils import *
from typing import Optional
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import SessionLocal, engine
from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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

@app.post("/watchlist/", response_model=schemas.WatchList)
def add_watchlist_entry(watchlistEntry: schemas.WatchListCreate, db: Session = Depends(get_db)):
    return crud.add_to_watchlist(db=db, watchlist_entry=watchlistEntry)

@app.get("/watchlist/", response_model=List[schemas.WatchList])
def get_watchlist(limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tickers(db=db, limit=limit)

@app.delete("/watchlist/{ticker}")
def delete_watchlist_entry(ticker: str, db: Session = Depends(get_db)):
    return crud.delete_from_watchlist(db=db, ticker=ticker)

@app.get("/equities/quote")
async def quote(ticker: str, columns: Optional[List[str]] = Query(["marketCap","regularMarketPrice"])):
    return_dict = {}
    ticker_data = get_data(ticker)
    for col in columns:
        return_dict[col] = ticker_data[col]
    return return_dict

@app.get("/equities/valuation/commodities/{commodity}")
async def valuation(commodity: str, ticker: str, commodity_price: float, multiple: float = 1.0, 
                    discount_rate: float = 0.08, capex_mult: float = 1.0, ebitda_mult: float =3.0):
    commodity = commodity.lower()
    print("received multiplier:",capex_mult)
    if commodity == "uranium":
        return {"value": multiple * get_uranium_miner_valuation(ticker, commodity_price, discount_rate, capex_mult)}
    elif commodity == "coal":
        return {"value": get_coal_miner_valuation(ticker, commodity_price, ebitda_mult)}
    elif commodity == "water":
        return {"value": get_vidler_water_valuation(LTSC_price=commodity_price)}
    else:
        return {"value":0}

@app.get("/equities/valuation/growth")
async def growth(ticker: str, cagr: float, discount_rate: float = 0.08, 
                terminal_growth: float = 0.03, speed_of_convergence: float = 2.5):
    return {"value": get_growth_valuation(ticker, cagr, discount_rate, terminal_growth, speed_of_convergence)}

@app.get("/sput")
async def sput():
    return scrape_SPUT()

@app.get("/data/uranium/supply")
async def uranium_supply(long_term_underfeeding: float = 16.0, globalFlag: bool = False, 
                        mcarthurFlag: bool = False, paladinFlag: bool = False,
                        sputYr: float = 0
):
    return get_supply_data(long_term_underfeeding, mcarthurFlag=mcarthurFlag, 
                        paladinFlag=paladinFlag, globalFlag=globalFlag, sputYr=sputYr) 

@app.get("/data/uranium/demand")
async def uranium_demand(growth_rate: float = 0.00):
    return get_demand_data(growth_rate)

'''@app.get("data/berkshire/cash")
async def berk_cash():
    return
'''
@app.get("/data/cape")
async def get_shiller_PE():
    return get_shiller_PE_data()

@app.get("/data/feargreed")
async def get_feargreed_index():
    return {"url":get_fear_greed_index()}

@app.get("/data/getindices")
async def getindices():
    return get_indices()

@app.get("/data/margin")
async def margin():
    return get_margin_debt_data()

@app.get("/search")
async def search(q: str):
    return openai_semantic_search(q)

class Notes(BaseModel):
    notes: str

@app.post("/notes/{ticker}")
async def notes(ticker: str, notes: Notes):
    jsonNotes = json.loads(notes.notes)
    print(jsonNotes)
    return "working"
    
'''@app.get("/data/insider")
async def insider_html():
    return {"html":get_insider_html()}'''