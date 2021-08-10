from sqlalchemy.orm import Session
import models
import schemas

def get_ticker(db: Session, ticker: str):
    return db.query(models.Watchlist).filter(models.Watchlist.ticker == ticker).first()

def get_tickers(db: Session, limit: int = 100):
    return db.query(models.Watchlist).offset(0).limit(limit).all()

def add_to_watchlist(db: Session, watchlist_entry: schemas.WatchListCreate):
    db_watchlist_entry = models.Watchlist(ticker=watchlist_entry.ticker, 
        name=watchlist_entry.name)
    db.add(db_watchlist_entry)
    db.commit()
    db.refresh(db_watchlist_entry)
    return db_watchlist_entry

def delete_from_watchlist(db: Session, ticker: str):
    db.query(models.Watchlist).filter(models.Watchlist.ticker == ticker).delete()
    db.commit()
    