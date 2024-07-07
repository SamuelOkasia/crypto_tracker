# backend/main.py
from fastapi import FastAPI, HTTPException
import pandas as pd

from Historic_Crypto import LiveCryptoData
from typing import List, Dict

app = FastAPI()




def Symbol_Info(symbol):
    try:
        live_data = LiveCryptoData(f'{symbol}-USD', False).return_data()
        ask = live_data.iloc[0]['ask']
        bid = live_data.iloc[0]['bid']
        volume = live_data.iloc[0]['rfq_volume']

        return { 'name' : symbol, 'ask' : ask, 'bid' : bid, 'volume' : volume }

    except Exception as e:
        return { 'name' : 'N/A', 'ask' : 'N/A', 'bid' : 'N/A', 'volume' : 'N/A' }


@app.get("/top_crypto")
async def top_crypto():
    try:
        top_crypto_symbols = ["BTC", "SOL", "ETH", "MANA", "XRP"]
        data = [Symbol_Info(symbol) for symbol in top_crypto_symbols]

        print(data)
        return data

    except Exception as e:
        return { 'error' : e}


@app.get("/cryptonews")
async def get_crypto_news() -> List[Dict]:
    df = pd.read_csv("cryptonews.csv")

    news_list = df.to_dict(orient="records")

    return news_list


@app.get("/historical_data/")
async def get_historical_data():
    # Adjust the path to your CSV file as necessary
    df = pd.read_csv("btc_2015_2024.csv")
    return df.to_dict(orient="records")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
