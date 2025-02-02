# config.py
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "https://api.coingecko.com/api/v3/coins/markets")
API_URL_BACKUP = os.getenv("API_URL_BACKUP", "https://api.coinpaprika.com/v1/tickers")
SINGLE_API_URL = os.getenv("SINGLE_API_URL", "https://api.coingecko.com/api/v3/coins/")
SINGLE_API_URL_BACKUP = os.getenv("SINGLE_API_URL_BACKUP", "https://api.coinpaprika.com/v1/tickers/")
VS_CURRENCY = os.getenv("VS_CURRENCY", "usd")
PER_PAGE = int(os.getenv("PER_PAGE", "10"))
