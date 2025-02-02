# main.py
from crypto_agent import fetch_crypto_data

if __name__ == "__main__":
    data = fetch_crypto_data()
    for crypto in data:
        print(crypto)
