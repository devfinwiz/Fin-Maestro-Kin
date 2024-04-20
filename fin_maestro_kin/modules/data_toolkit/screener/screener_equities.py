from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
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
                value = li.find('span', {'class': 'value'}).text.strip()
                value = value.replace('\n', '').replace('\u20b9', '').replace('          ', '').replace('         ', '').replace('       ','').replace(' ','').replace(',','').replace('Cr.','Cr')
                data[name] = value
        current_price = float(data['Current Price'])
        book_value = float(data['Book Value'])
        data['Price to book'] = str(round(current_price / book_value, 2))
        return {'symbol': company_code, 'key_metrics': data}
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