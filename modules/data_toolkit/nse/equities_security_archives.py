from fastapi import APIRouter, HTTPException, Query
import requests
import pandas as pd
from fastapi.responses import JSONResponse

router = APIRouter()

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
}


def fetch_data_from_nse(payload):
    try:
        result = requests.get(payload, headers=headers).json()
    except ValueError:
        session = requests.Session()
        result = session.get("http://nseindia.com", headers=headers)
        result = session.get(payload, headers=headers).json()
        print(result)
    return result

    
def security_wise_archive(symbol, start_date, end_date, series="ALL"):   
    base_url = "https://www.nseindia.com/api/historical/securityArchives"
    customized_request_url = f"{base_url}?from={start_date}&to={end_date}&symbol={symbol.upper()}&dataType=priceVolumeDeliverable&series={series.upper()}"
    response = fetch_data_from_nse(customized_request_url)
    
    payload = response.get('data', [])
    
    if not payload:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    
    return pd.DataFrame(payload)


# Convert DataFrame to dictionary with special handling for float values
def convert_dataframe_to_dict(df):
    df_dict = df.to_dict(orient='records')
    for record in df_dict:
        for key, value in record.items():
            if isinstance(value, float) and pd.notna(value):
                record[key] = round(value, 2) 
    return df_dict


# Example usage - http://localhost:8000/equities/security-archives?symbol=TCS&start_date=04-01-2024&end_date=14-01-2024&series=ALL
@router.get("/equities/security-archives")
def get_security_wise_archive(
    symbol: str = Query(..., title="Symbol", description="Stock symbol"),
    start_date: str = Query(..., title="From Date", description="Start date for historical data"),
    end_date: str = Query(..., title="To Date", description="End date for historical data"),
    series: str = Query("ALL", title="Series", description="Stock series")
):
    try:
        historical_data = security_wise_archive(symbol, start_date, end_date, series)
        rounded_data = convert_dataframe_to_dict(historical_data)
        return JSONResponse(content={"data": rounded_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching security-wise archive data: {e}")
 