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
    

def shareholding_pattern(company_code):
    url = f"https://www.screener.in/company/{company_code}/#shareholding"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('section', {'id': 'shareholding'})
        headers = [th.text.strip() for th in table.find('thead').find_all('th')]
        rows = table.find('tbody').find_all('tr')
        data = [{header: td.text.strip() for header, td in zip(headers, row.find_all('td'))} for row in rows]
        return {'symbol': company_code, 'shareholding_pattern': data}
    elif response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    else:
        raise HTTPException(status_code=500, detail=f"Failed to load the URL. Status code: {response.status_code}")


#Example usage: http://localhost:8000/screener-equities/shareholding-pattern?symbol=vedl
@router.get("/screener-equities/shareholding-pattern", tags=["Screener Equities"])
def get_shareholding_pattern(
    symbol: str = Query(..., title="Symbol", description="Stock Symbol")
):
    try:
        data = shareholding_pattern(symbol)
        if data is not None:
            processed_data = process_shareholding_pattern_data(data)
            return JSONResponse(content=processed_data)
        else:
            return JSONResponse(content={"error": "Failed to fetch data from URL"}, status_code=500)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching shareholding pattern data: {e}")
    

def cash_flow_statement(company_code):
    url = f"https://www.screener.in/company/{company_code}/#cash-flow"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('section', {'id': 'cash-flow'})
        headers = [th.text.strip() for th in table.find('thead').find_all('th')]
        rows = table.find('tbody').find_all('tr')
        data = [{header: td.text.strip() for header, td in zip(headers, row.find_all('td'))} for row in rows]
        return {'symbol': company_code, 'cash_flow_statement': data}
    elif response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    else:
        raise HTTPException(status_code=500, detail=f"Failed to load the URL. Status code: {response.status_code}")


#Example usage: http://localhost:8000/screener-equities/cash-flow?symbol=vedl
@router.get("/screener-equities/cash-flow", tags=["Screener Equities"])
def get_cash_flow_statement(
    symbol: str = Query(..., title="Symbol", description="Stock Symbol")
):
    try:
        data = cash_flow_statement(symbol)
        if data is not None:
            processed_data = process_cash_flow_data(data)
            return JSONResponse(content=processed_data)
        else:
            return JSONResponse(content={"error": "Failed to fetch data from URL"}, status_code=500)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching cash flow data: {e}")
    

def balance_sheet(company_code):
    url = f"https://www.screener.in/company/{company_code}/#balance-sheet"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('section', {'id': 'balance-sheet'})
        headers = [th.text.strip() for th in table.find('thead').find_all('th')]
        rows = table.find('tbody').find_all('tr')
        data = [{header: td.text.strip() for header, td in zip(headers, row.find_all('td'))} for row in rows]
        return {'symbol': company_code, 'balance_sheet': data}
    elif response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    else:
        raise HTTPException(status_code=500, detail=f"Failed to load the URL. Status code: {response.status_code}")


#Example usage: http://localhost:8000/screener-equities/balance-sheet?symbol=vedl
@router.get("/screener-equities/balance-sheet", tags=["Screener Equities"])
def get_balance_sheet(
    symbol: str = Query(..., title="Symbol", description="Stock Symbol")
):
    try:
        data = balance_sheet(symbol)
        if data is not None:
            processed_data = process_balance_sheet_data(data)
            return JSONResponse(content=processed_data)
        else:
            return JSONResponse(content={"error": "Failed to fetch data from URL"}, status_code=500)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching balance sheet data: {e}")
    

def annual_profit_and_loss_statement(company_code):
    url = f"https://www.screener.in/company/{company_code}/#profit-loss"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('section', {'id': 'profit-loss'})
        headers = [th.text.strip() for th in table.find('thead').find_all('th')]
        rows = table.find('tbody').find_all('tr')
        data = [{header: td.text.strip() for header, td in zip(headers, row.find_all('td'))} for row in rows]
        return {'symbol': company_code, 'profit_loss_statement': data}
    elif response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    else:
        raise HTTPException(status_code=500, detail=f"Failed to load the URL. Status code: {response.status_code}")


#Example usage: http://localhost:8000/screener-equities/annual-profit-loss?symbol=vedl
@router.get("/screener-equities/annual-profit-loss", tags=["Screener Equities"])
def get_annual_profit_and_loss_statement(
    symbol: str = Query(..., title="Symbol", description="Stock Symbol")
):
    try:
        data = annual_profit_and_loss_statement(symbol)
        if data is not None:
            processed_data = process_profit_loss_data(data)
            return JSONResponse(content=processed_data)
        else: 
            return JSONResponse(content={"error": "Failed to fetch data from URL"}, status_code=500)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching annual profit and loss data: {e}")
    

def ratios(company_code):
    url = f"https://www.screener.in/company/{company_code}/#ratios"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('section', {'id': 'ratios'})
        headers = [th.text.strip() for th in table.find('thead').find_all('th')]
        rows = table.find('tbody').find_all('tr')
        data = [{header: td.text.strip() for header, td in zip(headers, row.find_all('td'))} for row in rows]
        return {'symbol': company_code, 'ratios': data}
    elif response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    else:
        raise HTTPException(status_code=500, detail=f"Failed to load the URL. Status code: {response.status_code}")


#Example usage: http://localhost:8000/screener-equities/ratios?symbol=vedl
@router.get("/screener-equities/ratios", tags=["Screener Equities"])
def get_ratios(
    symbol: str = Query(..., title="Symbol", description="Stock Symbol")
):
    try:
        data = ratios(symbol)
        if data is not None:
            processed_data = process_ratios_data(data)
            return JSONResponse(content=processed_data)
        else: 
            return JSONResponse(content={"error": "Failed to fetch data from URL"}, status_code=500)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching ratios data: {e}")


def key_metrics(company_code):
    url = f"https://www.screener.in/company/{company_code}/#top"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    ratios = soup.find('div', {'class': 'company-ratios'})
    ul_elements = ratios.find_all('ul')

    if response.status_code == 200:
        data = {}
        for ul in ul_elements:
            for li in ul.find_all('li'):
                name = li.find('span', {'class': 'name'}).text.strip()
                value = process_key_metrics_data(li.find('span', {'class': 'value'}).text.strip())
                data[name] = value
        current_price = float(data['Current Price'])
        book_value = float(data['Book Value'])
        data['Price to book'] = str(round(current_price / book_value, 2))
        return {'symbol': company_code, 'key_metrics': data}
    elif response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    else:
        raise HTTPException(status_code=500, detail=f"Failed to load the URL. Status code: {response.status_code}")


#Example usage: http://localhost:8000/screener-equities/key-metrics?symbol=vedl
@router.get("/screener-equities/key-metrics", tags=["Screener Equities"])
def get_key_metrics(
    symbol: str = Query(..., title="Symbol", description="Stock Symbol")
):
    try:
        data = key_metrics(symbol)
        if data is not None:
            return JSONResponse(content=data)
        else:
            return JSONResponse(content={"error": "Failed to fetch data from URL"}, status_code=500)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching key metrics data: {e}")