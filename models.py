# models.py
from pydantic import BaseModel

class CryptoMarketData(BaseModel):
    id: str
    symbol: str
    name: str
    current_price: float
    market_cap: float
    total_volume: float
