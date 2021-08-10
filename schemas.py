from typing import List, Optional
from pydantic import BaseModel


class WatchListBase(BaseModel):
    ticker: str
    name: str

class WatchListCreate(WatchListBase):
    pass

class WatchList(WatchListBase):
    pass
    class Config:
        orm_mode = True
