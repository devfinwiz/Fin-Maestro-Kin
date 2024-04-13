from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup
from modules.data_toolkit.screener.helper import *

router = APIRouter(tags=["Screener Equities"])


def quarterly_results(company_code):
    url = f"https://www.screener.in/company/{company_code}/#quarters"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('section', {'id': 'quarters'})
        headers = [th.text.strip() for th in table.find('thead').find_all('th')]
        rows = table.find('tbody').find_all('tr')
        data = [{header: td.text.strip() for header, td in zip(headers, row.find_all('td'))} for row in rows]
        return {'symbol': company_code, 'quarterly_reports': data}
    elif response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    else:
        raise HTTPException(status_code=500, detail=f"Failed to load the URL. Status code: {response.status_code}")


#Example usage: http://localhost:8000/screener-equities/quarterly-result?symbol=vedl
@router.get("/screener-equities/quarterly-result", tags=["Screener Equities"])
def get_quarterly_results(
    symbol: str = Query(..., title="Symbol", description="Stock Symbol")
):
    try:
        data = quarterly_results(symbol)
        if data is not None:
            processed_data = process_quarterly_reports_data(data)
            return JSONResponse(content=processed_data)
        else:
            return JSONResponse(content={"error": "Failed to fetch data from URL"}, status_code=500)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching quarterly reports data: {e}")
