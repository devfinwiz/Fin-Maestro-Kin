from fastapi import APIRouter, HTTPException, Query
import requests
import json
from pydantic import BaseModel

router = APIRouter()

#Example Usgae - http://127.0.0.1:8000/indice_pcr?symbol=NIFTY
@router.get("/indice_pcr")
def get_pcr(symbol: str = Query(..., title="Symbol", description="Indice symbol")):
    pcr_value = pcr_indice_scraper(symbol)
    return {"symbol": symbol, "pcr_value": pcr_value}


#Example usage - http://127.0.0.1:8000/stock_pcr?symbol=RELIANCE
@router.get("/stock_pcr")
def get_pcr(symbol: str = Query(..., title="Symbol", description="Stock symbol")):
    pcr_value = pcr_stocks_scraper(symbol)
    return {"symbol": symbol, "pcr_value": pcr_value}


def pcr_indice_scraper(symbol):
    url = 'https://www.nseindia.com/api/option-chain-indices?symbol='+ symbol
    headers = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'accept-encoding' : 'gzip, deflate, br',
        'accept-language' : 'en-US,en;q=0.9'
    }
    request = requests.get("https://www.nseindia.com", timeout=10, headers=headers)
    cookies = dict(request.cookies)
    response = requests.get(url, headers=headers, cookies=cookies).content
    data = json.loads(response.decode('utf-8'))
    totCE = data['filtered']['CE']['totOI']
    totPE = data['filtered']['PE']['totOI']

    pcr = totPE / totCE
    return round(pcr, 3)


def pcr_stocks_scraper(symbol):
    url = 'https://www.nseindia.com/api/option-chain-equities?symbol=' + symbol
    headers = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'accept-encoding' : 'gzip, deflate, br',
        'accept-language' : 'en-US,en;q=0.9'
    }
    request = requests.get("https://www.nseindia.com", timeout=10, headers=headers)
    cookies = dict(request.cookies)
    response = requests.get(url, headers=headers, cookies= cookies).content
    
    data = json.loads(response.decode('utf-8'))
    totCE = data['filtered']['CE']['totOI']
    totPE = data['filtered']['PE']['totOI']

    pcr= totPE/totCE
    return round(pcr,3)