# ai_analysis.py
import openai
from typing import List
from models import CryptoMarketData
from pydantic import BaseModel

try:
    from pydantic_ai.core import AIModel
except ImportError:
    # Fallback : définir une classe AIModel vide pour permettre le fonctionnement de l'application
    class AIModel:
        pass

class MarketPrediction(BaseModel, AIModel):
    summary: str
    prediction: str

    class Config:
        ai_prompt_template = (
            "Analyze the following crypto market data and provide a summary of the market trends "
            "and a prediction indicating whether the market is bullish or bearish. "
            "The answer must be a valid JSON object with two keys: 'summary' and 'prediction'.\n\n"
            "Crypto data:\n{data_summary}"
        )

def analyze_market(data: List[CryptoMarketData]) -> MarketPrediction:
    data_summary = "\n".join(
        [f"{crypto.name} ({crypto.symbol}): Price={crypto.current_price}" for crypto in data]
    )
    prompt = MarketPrediction.Config.ai_prompt_template.format(data_summary=data_summary)
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a crypto market analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    ai_output = response.choices[0].message.content
    try:
        prediction = MarketPrediction.parse_raw(ai_output)
        return prediction
    except Exception as e:
        print("Erreur lors de l'analyse AI des données du marché :", e)
        return MarketPrediction(summary="Aucune analyse disponible", prediction="neutral")
