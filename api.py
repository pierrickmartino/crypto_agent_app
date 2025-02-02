# api.py
from fastapi import FastAPI, HTTPException
from typing import List
from crypto_agent import fetch_crypto_data, fetch_single_crypto_data
from models import CryptoMarketData
from ai_analysis import analyze_market, MarketPrediction

app = FastAPI(
    title="API Crypto Agent",
    description="API REST pour exposer les données de marché des crypto-monnaies et leur analyse AI."
)

@app.get("/", tags=["Root"])
def root():
    return {"message": "Bienvenue sur l'API de Crypto Agent"}

@app.get("/cryptodata", response_model=List[CryptoMarketData], tags=["Crypto Data"])
def get_crypto_data():
    data = fetch_crypto_data()
    if not data:
        raise HTTPException(status_code=404, detail="Aucune donnée de crypto-monnaies disponible.")
    return data

@app.get("/cryptodata/{token_id}", response_model=CryptoMarketData, tags=["Crypto Data"])
def get_single_crypto_data(token_id: str):
    crypto = fetch_single_crypto_data(token_id)
    if not crypto:
        raise HTTPException(status_code=404, detail=f"Aucune donnée disponible pour le token '{token_id}'.")
    return crypto

@app.get("/cryptoanalysis", response_model=MarketPrediction, tags=["Crypto Analysis"])
def get_crypto_analysis():
    data = fetch_crypto_data()
    if not data:
        raise HTTPException(status_code=404, detail="Aucune donnée de crypto-monnaies disponible pour l'analyse.")
    analysis = analyze_market(data)
    return analysis
