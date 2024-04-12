from fastapi import APIRouter, HTTPException, Query
from modules.data_toolkit.nse.helper import *
from fastapi.responses import JSONResponse
import requests
import pandas as pd
import re
import json

router = APIRouter(tags=["NSE Equities"])

    
def security_wise_archive(symbol, start_date, end_date, series="ALL"):   
    base_url = "https://www.nseindia.com/api/historical/securityArchives"
    customized_request_url = f"{base_url}?from={start_date}&to={end_date}&symbol={symbol.upper()}&dataType=priceVolumeDeliverable&series={series.upper()}"
    response = fetch_data_from_nse(customized_request_url)
    
    payload = response.get('data', [])
    
    if not payload:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    
    return pd.DataFrame(payload)


# Example usage - http://localhost:8000/equities/security-archives?symbol=TCS&start_date=04-01-2024&end_date=14-01-2024&series=ALL
@router.get("/equities/security-archives",tags=["NSE Equities"])
def get_security_wise_archive(
    symbol: str = Query(..., title="Symbol", description="Stock symbol"),
    start_date: str = Query(..., title="From Date", description="Start date for historical data in dd-mm-yyyy format"),
    end_date: str = Query(..., title="To Date", description="End date for historical data in dd-mm-yyyy format"),
    series: str = Query("ALL", title="Series", description="Stock series")
):
    try:
        historical_data = security_wise_archive(symbol, start_date, end_date, series)
        processed_data = process_security_wise_archive_data(historical_data)
        return JSONResponse(content={"stock_data": processed_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching security-wise archive data: {e}")
    
    
def bulk_deals_archives(start_date, end_date):
    base_url="https://www.nseindia.com/api/historical/bulk-deals"
    customized_request_url = f"{base_url}?from={start_date}&to={end_date}"
    response=fetch_data_from_nse(customized_request_url)
    
    payload = response.get('data', [])
    
    if not payload:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    
    return pd.DataFrame(payload)


# Example usage - http://localhost:8000/equities/bulk-deals-archives?start_date=28-01-2024&end_date=04-02-2024
@router.get("/equities/bulk-deals-archives",tags=["NSE Equities"])
def get_bulk_deals_archives(
    start_date: str = Query(..., title="From Date", description="Start date for historical data in dd-mm-yyyy format"),
    end_date: str = Query(..., title="To Date", description="End date for historical data in dd-mm-yyyy format"),  
):
    try:
        historical_data = bulk_deals_archives(start_date, end_date)
        processed_data = process_bulk_block_deal_archive_data(historical_data)
        return JSONResponse(content={"bulk_deal_archive_data": processed_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bulk-deals archive data: {e}")
    
    
def block_deals_archives(start_date, end_date):
    base_url="https://www.nseindia.com/api/historical/block-deals"
    customized_request_url = f"{base_url}?from={start_date}&to={end_date}"
    response=fetch_data_from_nse(customized_request_url)
    
    payload = response.get('data', [])
    
    if not payload:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    
    return pd.DataFrame(payload)


# Example usage - http://localhost:8000/equities/block-deals-archives?start_date=28-01-2024&end_date=04-02-2024
@router.get("/equities/block-deals-archives",tags=["NSE Equities"])
def get_block_deals_archives(
    start_date: str = Query(..., title="From Date", description="Start date for historical data in dd-mm-yyyy format"),
    end_date: str = Query(..., title="To Date", description="End date for historical data in dd-mm-yyyy format"),  
):
    try:
        historical_data = block_deals_archives(start_date, end_date)
        processed_data = process_bulk_block_deal_archive_data(historical_data)
        return JSONResponse(content={"block_deal_archive_data": processed_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching block deals archive data: {e}")
    

def short_selling_archives(start_date, end_date):
    base_url="https://www.nseindia.com/api/historical/short-selling"
    customized_request_url = f"{base_url}?from={start_date}&to={end_date}"
    response=fetch_data_from_nse(customized_request_url)
    
    payload = response.get('data', [])
    
    if not payload:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    
    return pd.DataFrame(payload)


#Example usage - http://localhost:8000/equities/short-selling-archives?start_date=28-01-2024&end_date=04-02-2024
@router.get("/equities/short-selling-archives",tags=["NSE Equities"])
def get_short_selling_archives(
    start_date: str = Query(..., title="From Date", description="Start date for historical data in dd-mm-yyyy format"),
    end_date: str = Query(..., title="To Date", description="End date for historical data in dd-mm-yyyy format"),  
):
    try:
        historical_data = short_selling_archives(start_date, end_date)
        processed_data = process_short_selling_archives_data(historical_data)
        return JSONResponse(content={"short_selling_archive_data": processed_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching short-selling archive data: {e}")
    

def corporate_actions(start_date, end_date):
    base_url = "https://www.nseindia.com/api/corporates-corporateActions"
    
    customized_request_url = f"{base_url}?index=equities&from={start_date}&to={end_date}"
    response = fetch_data_from_nse(customized_request_url)
    
    if not response:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    
    if isinstance(response, list):
        payload = response
    else:
        payload = response.get('data', [])
    
    return pd.DataFrame(payload)
    

# Example usage - http://localhost:8000/equities/corporate-actions?start_date=28-01-2024&end_date=04-02-2024
@router.get("/equities/corporate-actions",tags=["NSE Equities"])
def get_corporate_actions(
    start_date: str = Query(..., title="From Date", description="Start date for data in dd-mm-yyyy format"),
    end_date: str = Query(..., title="To Date", description="End date for data in dd-mm-yyyy format"),  
):
    try:
        data = corporate_actions(start_date, end_date)
        processed_data = process_corporate_actions_data(data)
        return JSONResponse(content={"corporate_actions_data": processed_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching corporate actions data: {e}")
    

def nse_monthly_most_active_securities():
    request_url = "https://www.nseindia.com/api/historical/most-active-securities-monthly"
    response = fetch_data_from_nse(request_url)
    payload = response.get('data', [])
    
    if not payload:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    
    return pd.DataFrame(payload)
    

# Example usage - http://localhost:8000/equities/most-active-securities
@router.get("/equities/most-active-securities",tags=["NSE Equities"])
def get_nse_monthly_most_active_securities():
    try:
        historical_data = nse_monthly_most_active_securities()
        processed_data = process_most_active_securities_data(historical_data)
        return JSONResponse(content={"most_active_securities_data": processed_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching monthly most active securities data: {e}")
    
    
def nse_monthly_advances_and_declines(year):
    base_url="https://www.nseindia.com/api/historical/advances-decline-monthly"
    customized_request_url = f"{base_url}?year={year}"
    response=fetch_data_from_nse(customized_request_url)
    
    payload = response.get('data', [])
    
    if not payload:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    
    return pd.DataFrame(payload)


#Example usage - http://localhost:8000/equities/advances-declines?year=2024
@router.get("/equities/advances-declines",tags=["NSE Equities"])
def get_nse_monthly_advances_and_declines(
    year: str = Query(..., title="Year", description="Year for historical data in format YYYY"), 
):
    if not re.match(r"\d{4}", year):
        raise HTTPException(status_code=422, detail="Invalid year format. Please use 'YYYY' format.")
    
    try:
        historical_data = nse_monthly_advances_and_declines(year)
        processed_data = process_monthly_advances_declines_data(historical_data)
        return JSONResponse(content={"monthly_advances_and_declines_data": processed_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching advances and declines data: {e}")
    
    
def nse_capital_market_monthly_settlement_stats(financial_year):
    base_url = "https://www.nseindia.com/api/historical/monthly-sett-stats-data"
    customized_request_url = f"{base_url}?finYear={financial_year}"
    response = fetch_data_from_nse(customized_request_url)
    payload = response.get('data', [])
    
    if not payload:
        raise HTTPException(status_code=404, detail=f"No capital market settlement statistics found.")
    
    return pd.DataFrame(payload)


#Example usage - http://localhost:8000/equities/monthly-settlement-stats/capital-market?financial_year=2022-2023
@router.get("/equities/monthly-settlement-stats/capital-market",tags=["NSE Equities"])
def get_nse_capital_market_monthly_settlement_stats(
    financial_year: str = Query(..., title="Year", description="Financial Year for historical data in format YYYY-YYYY"), 
):
    if not re.match(r"\d{4}-\d{4}", financial_year):
        raise HTTPException(status_code=422, detail="Invalid financial year format. Please use 'YYYY-YYYY' format.")
    
    try:
        historical_data = nse_capital_market_monthly_settlement_stats(financial_year)
        processed_data = process_capital_market_monthly_settlement_stats(historical_data)
        return JSONResponse(content={"capital_market_monthly_settlement_stats_data": processed_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching monthly settlement statistics for capital market: {e}")


def nse_fno_monthly_settlement_stats(financial_year):
    from_date, to_date = transform_financial_year(financial_year)
    base_url = "https://www.nseindia.com/api/financial-monthlyStats"
    customized_request_url = f"{base_url}?from_date={from_date}&to_date={to_date}"
    response = fetch_data_from_nse(customized_request_url)
    payload = response 
    
    if not payload:
        raise HTTPException(status_code=404, detail="No monthly settlement statistics found.")
    
    return pd.DataFrame(payload)


#Example usage - http://localhost:8000/equities/monthly-settlement-stats/fno?financial_year=2022-2023
@router.get("/equities/monthly-settlement-stats/fno",tags=["NSE Equities"])
def get_nse_fno_monthly_settlement_stats(
    financial_year: str = Query(..., title="Year", description="Financial Year for historical data in format YYYY-YYYY"), 
):
    if not re.match(r"\d{4}-\d{4}", financial_year):
        raise HTTPException(status_code=422, detail="Invalid financial year format. Please use 'YYYY-YYYY' format.")
    
    try:
        historical_data = nse_fno_monthly_settlement_stats(financial_year)
        
        if not isinstance(historical_data, pd.DataFrame):
            raise HTTPException(status_code=404, detail="No data found.")
        
        processed_data = process_fno_monthly_settlement_stats(historical_data)
        return JSONResponse(content={"fno_monthly_settlement_stats_data": processed_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching monthly settlement statistics for future & options: {e}")
    

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


#Example usage - http://127.0.0.1:8000/equities/stock-pcr?symbol=RELIANCE
@router.get("/equities/stock-pcr",tags=["NSE Equities"])
def get_pcr(symbol: str = Query(..., title="Symbol", description="Stock symbol")):
    pcr_value = pcr_stocks_scraper(symbol)
    return {"symbol": symbol, "pcr_value": pcr_value}


def nse_equity_tickers():
    try:
        symbols = pd.read_csv('https://archives.nseindia.com/content/equities/EQUITY_L.csv')
        tickers = symbols['SYMBOL'].tolist()
        return tickers
    except Exception as e:
        return f"Error fetching equity tickers: {e}"


#Example usage - http://localhost:8000/equities/equity-tickers
@router.get("/equities/equity-tickers", tags=["NSE Equities"])
def get_nse_equity_tickers():
    return {"equity_tickers": nse_equity_tickers()}


def board_meetings(start_date, end_date):
    base_url = "https://www.nseindia.com/api/corporate-board-meetings"
    
    customized_request_url = f"{base_url}?index=equities&from={start_date}&to={end_date}"
    response = fetch_data_from_nse(customized_request_url)
    
    if not response:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    
    if isinstance(response, list):
        payload = response
    else:
        payload = response.get('data', [])
    
    return pd.DataFrame(payload)
    

# Example usage - http://localhost:8000/equities/board-meetings?start_date=28-01-2024&end_date=04-02-2024
@router.get("/equities/board-meetings",tags=["NSE Equities"])
def get_board_meetings(
    start_date: str = Query(..., title="From Date", description="Start date for data in dd-mm-yyyy format"),
    end_date: str = Query(..., title="To Date", description="End date for data in dd-mm-yyyy format"),  
):
    try:
        data = board_meetings(start_date, end_date)
        processed_data = process_board_meetings_data(data)
        return JSONResponse(content={"board_meetings_data": processed_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching board meetings data: {e}")
    
    
def insider_trading(start_date, end_date):
    base_url = "https://www.nseindia.com/api/corporates-pit"
    
    customized_request_url = f"{base_url}?index=equities&from={start_date}&to={end_date}"
    response = fetch_data_from_nse(customized_request_url)
    
    if not response:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    
    if isinstance(response, list):
        payload = response
    else:
        payload = response.get('data', [])
    
    return pd.DataFrame(payload)
    

# Example usage - http://localhost:8000/equities/insider-trading?start_date=28-01-2024&end_date=04-02-2024
@router.get("/equities/insider-trading",tags=["NSE Equities"])
def get_insider_trading(
    start_date: str = Query(..., title="From Date", description="Start date for data in dd-mm-yyyy format"),
    end_date: str = Query(..., title="To Date", description="End date for data in dd-mm-yyyy format"),  
):
    try:
        data = insider_trading(start_date, end_date)
        processed_data = process_insider_trading_data(data)
        return JSONResponse(content={"insider_trading_data": processed_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching insider_trading data: {e}")
    

def shareholding_patterns(symbol):
    base_url = "https://www.nseindia.com/api/corporate-share-holdings-master"
    
    customized_request_url = f"{base_url}?index=equities&symbol={symbol}"
    response = fetch_data_from_nse(customized_request_url)
    
    if not response:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    
    if isinstance(response, list):
        payload = response
    else:
        payload = response.get('data', [])
    return pd.DataFrame(payload)
    

# Example usage - http://localhost:8000/equities/shareholding-patterns?symbol=BAJAJCON
@router.get("/equities/shareholding-patterns",tags=["NSE Equities"])
def get_shareholding_patterns(
    symbol: str = Query(..., title="Symbol", description="Stock Symbol")
):
    try:
        data = shareholding_patterns(symbol)
        processed_data = process_shareholding_patterns_data(data)
        return JSONResponse(content={"shareholding_patterns_data": processed_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching shareholding patterns data: {e}")
    
    
def annual_reports(symbol):
    base_url = "https://www.nseindia.com/api/annual-reports"
    
    customized_request_url = f"{base_url}?index=equities&symbol={symbol}"
    response = fetch_data_from_nse(customized_request_url)
    
    if not response:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    
    if isinstance(response, list):
        payload = response
    else:
        payload = response.get('data', [])
    return pd.DataFrame(payload)
    

# Example usage - http://localhost:8000/equities/annual-reports?symbol=BAJAJCON
@router.get("/equities/annual-reports",tags=["NSE Equities"])
def get_annual_reports(
    symbol: str = Query(..., title="Symbol", description="Stock Symbol")
):
    try:
        data = annual_reports(symbol)
        processed_data = process_annual_reports_data(data)
        return JSONResponse(content={"annual_reports_data": processed_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching annual reports data: {e}")