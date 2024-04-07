from fastapi import APIRouter, HTTPException, Query
from modules.data_toolkit.nse.helper import *
from fastapi.responses import JSONResponse
import requests
import json
import pandas as pd
import datetime

router = APIRouter(tags=["NSE Indices"])
    

def index_history(symbol, start_date, end_date):
    base_url="https://www.nseindia.com/api/historical/indicesHistory"
    customized_request_url = f"{base_url}?indexType={symbol}&from={start_date}&to={end_date}"
    response=fetch_data_from_nse(customized_request_url)
    
    payload = response.get('data', [])
    
    if not payload:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    
    return pd.DataFrame(payload)


#Example usage - 127.0.0.1:8000/nseindices/history?symbol=NIFTY 50&start_date=10-01-2024&end_date=12-02-2024
@router.get("/nseindices/history",tags=["NSE Indices"])
def get_nse_index_history(
    symbol: str = Query(..., title="Symbol", description="NSE indices symbol"),
    start_date: str = Query(..., title="Start Date", description="Start date for historical data in dd-mm-yyyy format"),
    end_date: str = Query(..., title="End Date", description="End date for historical data in dd-mm-yyyy format")
):
    try:
        history_data = index_history(symbol, start_date, end_date)
        processed_data = process_index_data(history_data)
        return JSONResponse(content={"index_historical_data": processed_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching historical data: {e}")
    

def index_pe_pb_div(symbol, start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, "%d-%b-%Y").strftime("%d %b %Y")
    end_date = datetime.datetime.strptime(end_date, "%d-%b-%Y").strftime("%d %b %Y")
    
    data = {"cinfo": f"{{'name':'{symbol}','startDate':'{start_date}','endDate':'{end_date}'}}"}
    payload = requests.post('https://niftyindices.com/Backpage.aspx/getpepbHistoricaldataDBtoString', headers=niftyindices_headers,  json=data).json()
    payload = json.loads(payload["d"])
    
    if not payload:
        raise HTTPException(status_code=404, detail="No historical data found.")
    
    payload=pd.DataFrame.from_records(payload)
    return payload


#Example usage - #Example usage - 127.0.0.1:8000/nseindices/ratios?symbol=NIFTY 50&start_date=10-Jan-2024&end_date=12-Jan-2024
@router.get("/nseindices/ratios",tags=["NSE Indices"])
def get_nse_indices_ratios(
    symbol: str = Query(..., title="Symbol", description="Nifty indices symbol"),
    start_date: str = Query(..., title="Start Date", description="Start date for historical data in dd-mmm-yyyy format"),
    end_date: str = Query(..., title="End Date", description="End date for historical data in dd-mmm-yyyy format")
):
    try:
        historical_ratios_data = index_pe_pb_div(symbol, start_date, end_date)
        return historical_ratios_data.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching historical ratios data: {e}")
    

def index_total_returns(symbol,start_date,end_date):
    start_date = datetime.datetime.strptime(start_date, "%d-%b-%Y").strftime("%d %b %Y")
    end_date = datetime.datetime.strptime(end_date, "%d-%b-%Y").strftime("%d %b %Y")
    
    data = {"cinfo": f"{{'name':'{symbol}','startDate':'{start_date}','endDate':'{end_date}'}}"}
    payload = requests.post('https://niftyindices.com/Backpage.aspx/getTotalReturnIndexString', headers=niftyindices_headers,  json=data).json()
    payload = json.loads(payload["d"])
    
    if not payload:
        raise HTTPException(status_code=404, detail="No historical data found.")
    
    payload=pd.DataFrame.from_records(payload)
    return payload


#Example usage - 127.0.0.1:8000/nseindices/returns?symbol=NIFTY 50&start_date=10-Jan-2024&end_date=12-Jan-2024
@router.get("/nseindices/returns",tags=["NSE Indices"])
def get_nse_indices_returns(
    symbol: str = Query(..., title="Symbol", description="Nifty indices symbol"),
    start_date: str = Query(..., title="Start Date", description="Start date for historical data in dd-mmm-yyyy format"),
    end_date: str = Query(..., title="End Date", description="End date for historical data in dd-mmm-yyyy format")
):
    try:
        historical_returns_data = index_total_returns(symbol, start_date, end_date)
        return historical_returns_data.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching historical ratios data: {e}")
    
    
#Example Usgae - http://127.0.0.1:8000/nseindices/indice-pcr?symbol=NIFTY
@router.get("/nseindices/indice-pcr",tags=["NSE Indices"])
def get_pcr(
    symbol: str = Query(..., title="Symbol", description="Indice symbol")
):
    pcr_value = pcr_indice_scraper(symbol)
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


def india_vix_history(start_date, end_date):
    base_url="https://www.nseindia.com/api/historical/vixhistory"
    customized_request_url = f"{base_url}?from={start_date}&to={end_date}"
    response=fetch_data_from_nse(customized_request_url)
    
    payload = response.get('data', [])
    
    if not payload:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    
    return pd.DataFrame(payload)


# Example usage - http://localhost:8000/nseindices/india-vix?start_date=28-01-2024&end_date=04-02-2024
@router.get("/nseindices/india-vix",tags=["NSE Indices"])
def get_india_vix_history(
    start_date: str = Query(..., title="From Date", description="Start date for historical data in dd-mm-yyyy format"),
    end_date: str = Query(..., title="To Date", description="End date for historical data in dd-mm-yyyy format"),  
):
    try:
        historical_data = india_vix_history(start_date, end_date)
        processed_data = process_vix_data(historical_data)
        return JSONResponse(content={"vix_data": processed_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching India Vix historical data: {e}")
    
    
def fetch_index_symbols():
    url = 'https://nseindia.com/api/allIndices'
    try:
        response = fetch_data_from_nse(url) 
        data = response.get('data', [])
        index_symbols = [entry['indexSymbol'] for entry in data]
        return index_symbols
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching index symbols: {e}")


# Example usage - http://localhost:8000/nseindices/index-symbols
@router.get("/nseindices/index-symbols", tags=["NSE Indices"])
def get_index_symbols():
    return {"index_symbols": fetch_index_symbols()}