# crypto_agent.py
import requests
from typing import List, Optional
from models import CryptoMarketData
import config
from pydantic import parse_obj_as, ValidationError

def fetch_crypto_data() -> List[CryptoMarketData]:
    params = {
        "vs_currency": config.VS_CURRENCY,
        "order": "market_cap_desc",
        "per_page": config.PER_PAGE,
        "page": 1,
        "sparkline": "false"
    }
    try:
        response = requests.get(config.API_URL, params=params)
        if response.status_code == 200:
            try:
                data = response.json()
                cryptos = parse_obj_as(List[CryptoMarketData], data)
                if cryptos:
                    return cryptos
                else:
                    print("Aucune donnée récupérée depuis le fournisseur principal. Passage au backup.")
                    return fetch_crypto_data_backup()
            except ValidationError as e:
                print("Erreur de validation des données du fournisseur principal :", e)
                return fetch_crypto_data_backup()
        else:
            print("Erreur HTTP du fournisseur principal :", response.status_code)
            return fetch_crypto_data_backup()
    except Exception as e:
        print("Exception lors de la récupération des données du fournisseur principal :", e)
        return fetch_crypto_data_backup()

def fetch_crypto_data_backup() -> List[CryptoMarketData]:
    response = requests.get(config.API_URL_BACKUP)
    if response.status_code == 200:
        try:
            data = response.json()
            filtered = [coin for coin in data if "USD" in coin.get("quotes", {})]
            sorted_coins = sorted(filtered, key=lambda coin: coin["quotes"]["USD"].get("market_cap", 0), reverse=True)
            top_coins = sorted_coins[:config.PER_PAGE]
            result = []
            for coin in top_coins:
                result.append(CryptoMarketData(
                    id=coin["id"],
                    symbol=coin["symbol"],
                    name=coin["name"],
                    current_price=coin["quotes"]["USD"]["price"],
                    market_cap=coin["quotes"]["USD"]["market_cap"],
                    total_volume=coin["quotes"]["USD"]["volume_24h"]
                ))
            return result
        except Exception as e:
            print("Erreur de traitement des données du fournisseur de secours :", e)
            return []
    else:
        print("Erreur HTTP du fournisseur de secours :", response.status_code)
        return []

def fetch_single_crypto_data(token_id: str) -> Optional[CryptoMarketData]:
    url = config.SINGLE_API_URL + token_id
    params = {
        "localization": "false",
        "tickers": "false",
        "market_data": "true",
        "community_data": "false",
        "developer_data": "false",
        "sparkline": "false"
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            crypto = CryptoMarketData(
                id=data["id"],
                symbol=data["symbol"],
                name=data["name"],
                current_price=data["market_data"]["current_price"]["usd"],
                market_cap=data["market_data"]["market_cap"]["usd"],
                total_volume=data["market_data"]["total_volume"]["usd"]
            )
            return crypto
        else:
            print("Erreur HTTP pour le token avec le fournisseur principal :", response.status_code)
            return fetch_single_crypto_data_backup(token_id)
    except Exception as e:
        print("Exception lors de la récupération du token avec le fournisseur principal :", e)
        return fetch_single_crypto_data_backup(token_id)

def fetch_single_crypto_data_backup(token_id: str) -> Optional[CryptoMarketData]:
    url = config.SINGLE_API_URL_BACKUP + token_id
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            crypto = CryptoMarketData(
                id=data["id"],
                symbol=data["symbol"],
                name=data["name"],
                current_price=data["quotes"]["USD"]["price"],
                market_cap=data["quotes"]["USD"]["market_cap"],
                total_volume=data["quotes"]["USD"]["volume_24h"]
            )
            return crypto
        else:
            print("Erreur HTTP pour le token avec le fournisseur de secours :", response.status_code)
            return None
    except Exception as e:
        print("Exception lors de la récupération du token avec le fournisseur de secours :", e)
        return None
