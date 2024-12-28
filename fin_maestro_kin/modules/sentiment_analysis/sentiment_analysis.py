import requests
import json
from datetime import datetime, time
from fastapi import APIRouter, Query

class PCR():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'
    }

    @staticmethod
    def fetch_data(url, symbol):
        try:
            session = requests.Session()
            session.get("https://www.nseindia.com", headers=PCR.headers, timeout=10)
            cookies = session.cookies

            response = session.get(url, headers=PCR.headers, cookies=cookies, timeout=10)

            if response.headers.get("Content-Type") != "application/json; charset=utf-8":
                raise ValueError(f"Unexpected content type: {response.headers.get('Content-Type')}")

            return json.loads(response.content.decode('utf-8', errors='replace'))
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None
        
    @staticmethod
    def pcr_indice_scraper(symbol):
        url = f'https://www.nseindia.com/api/option-chain-indices?symbol={symbol}'
        data = PCR.fetch_data(url, symbol)
        if not data:
            return {"error": f"Failed to fetch PCR data for {symbol}"}

        try:
            totCE = data['filtered']['CE']['totOI']
            totPE = data['filtered']['PE']['totOI']
            pcr = round(totPE / totCE, 3)
            return pcr
        except KeyError as e:
            print(f"KeyError for {symbol}: {e}")
            return {"error": f"Data structure error for {symbol}"}

    @staticmethod
    def pcr_stocks_scraper(symbol):
        url = f'https://www.nseindia.com/api/option-chain-equities?symbol={symbol}'
        data = PCR.fetch_data(url, symbol)
        if not data:
            return {"error": f"Failed to fetch PCR data for {symbol}"}

        try:
            totCE = data['filtered']['CE']['totOI']
            totPE = data['filtered']['PE']['totOI']
            pcr = round(totPE / totCE, 3)
            return pcr
        except KeyError as e:
            print(f"KeyError for {symbol}: {e}")
            return {"error": f"Data structure error for {symbol}"}


class SentimentAnalyzer(PCR):
    def __init__(self):
        self.router = APIRouter(tags=["Sentiment"])

    def register_routes(self, app):
        self.router.add_api_route("/sentiment/pcr-indice-analysis", self.analyze_indices, methods=["GET"])
        self.router.add_api_route("/sentiment/pcr-stocks-analysis", self.analyze_stock, methods=["GET"])
        app.include_router(self.router)

    def analyze_indices(self):
        try:
            pcr_anal_result = self.pcr_indice_analysis()
            return pcr_anal_result
        except Exception as e:
            return {"error": f"An error occurred during PCR analysis: {e}"}

    def analyze_stock(self, symbol: str = Query(..., title="Symbol", description="Stock symbol")):
        try:
            pcr_anal_result = self.pcr_stocks_analysis(symbol)
            return pcr_anal_result
        except Exception as e:
            return {"error": f"An error occurred during PCR analysis for {symbol}: {e}"}

    @staticmethod
    def pcr_indice_analysis():
        pcr_anal_result = {}
        indices = ["NIFTY", "BANKNIFTY"]

        for symbol in indices:
            try:
                pcr_value = PCR.pcr_indice_scraper(symbol)
            except Exception as e:
                print(f"Error fetching PCR for {symbol}: {e}")
                return {"error": f"Failed to fetch PCR for {symbol}"}

            state = SentimentAnalyzer.get_state(pcr_value, [1.4, 1.19, 1, 0.91, 0.6])
            pcr_anal_result[symbol] = [state, pcr_value]

        return pcr_anal_result

    @staticmethod
    def pcr_stocks_analysis(symbol):
        try:
            pcr_anal_result = {}
            pcr_value = PCR.pcr_stocks_scraper(symbol)
        except Exception as e:
            print(f"Error fetching PCR for {symbol}: {e}")
            return {"error": f"Failed to fetch PCR for {symbol}"}

        state = SentimentAnalyzer.get_state(pcr_value, [1, 0.75, 0.50, 0.4])
        pcr_anal_result[symbol] = [state, pcr_value]

        return pcr_anal_result

    @staticmethod
    def get_state(pcr_value, thresholds):
        for threshold, label in zip(thresholds, ["Overbought", "Slightly overbought", "Neutral", "Slightly oversold"]):
            if pcr_value >= threshold:
                return label
        return "Oversold"
