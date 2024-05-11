from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup
from typing import Dict


class Helper:
    @staticmethod
    def process_data(data, key):
        stock_name = data.get('symbol', '')
        reports = data.get(key, [])
        formatted_reports = {}
        for report in reports:
            label = report.get("")
            if label:
                formatted_label = label.replace('+', '').strip()
                formatted_reports[formatted_label] = {key: value.replace('%','').replace(',','') for key, value in report.items() if key != ""}
                print(formatted_reports[formatted_label])
        return {'symbol': stock_name, key: formatted_reports}
    
    @staticmethod
    def process_key_metrics_data(value):
        return value.replace('\n', '').replace('\u20b9', '').replace('          ', '').replace('         ', '').replace('       ','').replace(' ','').replace(',','').replace('Cr.','').replace('%','')
    
    @staticmethod
    def handle_key_metrics_response(response, company_code):
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            ratios = soup.find('div', {'class': 'company-ratios'})
            ul_elements = ratios.find_all('ul')

            data = {}
            for ul in ul_elements:
                for li in ul.find_all('li'):
                    name = li.find('span', {'class': 'name'}).text.strip()
                    value = Helper.process_key_metrics_data(li.find('span', {'class': 'value'}).text.strip())
                    data[name] = value

            current_price = float(data['Current Price'])
            book_value = float(data['Book Value'])
            data['Price to book'] = str(round(current_price / book_value, 2))
            return {'symbol': company_code, 'key_metrics': data}
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to load the URL. Status code: {response.status_code}")
        
    @staticmethod
    def handle_response(response, company_code, data_key):
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('section', {'id': data_key})
            if table:
                headers = [th.text.strip() for th in table.find('thead').find_all('th')]
                rows = table.find('tbody').find_all('tr')
                data = [{header: td.text.strip() for header, td in zip(headers, row.find_all('td'))} for row in rows]
                return {'symbol': company_code, data_key: data}
            else:
                raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to load the URL. Status code: {response.status_code}")


class ScreenerEquities(Helper):
    def __init__(self):
        self.router = APIRouter(tags=["Screener Equities"])

    def register_routes(self, app):
        self.router.add_api_route("/screener-equities/quarterly-result", self.get_quarterly_results, methods=["GET"], tags=["Screener Equities"])
        self.router.add_api_route("/screener-equities/shareholding-pattern", self.get_shareholding_pattern, methods=["GET"], tags=["Screener Equities"])
        self.router.add_api_route("/screener-equities/cash-flow", self.get_cash_flow_statement, methods=["GET"], tags=["Screener Equities"])
        self.router.add_api_route("/screener-equities/balance-sheet", self.get_balance_sheet, methods=["GET"], tags=["Screener Equities"])
        self.router.add_api_route("/screener-equities/annual-profit-loss", self.get_annual_profit_and_loss_statement, methods=["GET"], tags=["Screener Equities"])
        self.router.add_api_route("/screener-equities/ratios", self.get_ratios, methods=["GET"], tags=["Screener Equities"])
        self.router.add_api_route("/screener-equities/key-metrics", self.get_key_metrics, methods=["GET"], tags=["Screener Equities"])
        app.include_router(self.router)

    def quarterly_results(self, company_code):
        url = f"https://www.screener.in/company/{company_code}/#quarters"
        response = requests.get(url)
        return self.handle_response(response, company_code, 'quarters')

    def get_quarterly_results(
        self,
        symbol: str = Query(..., title="Symbol", description="Stock Symbol")
    ):
        try:
            data = self.quarterly_results(symbol)
            processed_data = self.process_data(data, 'quarters')
            return JSONResponse(content=processed_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching quarterly reports data: {e}")
        
    def shareholding_pattern(self, company_code):
        url = f"https://www.screener.in/company/{company_code}/#shareholding"
        response = requests.get(url)
        return self.handle_response(response, company_code, 'shareholding')

    def get_shareholding_pattern(self, symbol: str = Query(..., title="Symbol", description="Stock Symbol")):
        try:
            data = self.shareholding_pattern(symbol)
            processed_data = self.process_data(data, 'shareholding')
            return JSONResponse(content=processed_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching shareholding pattern data: {e}")

    def cash_flow_statement(self, company_code):
        url = f"https://www.screener.in/company/{company_code}/#cash-flow"
        response = requests.get(url)
        return self.handle_response(response, company_code, 'cash-flow')

    def get_cash_flow_statement(self, symbol: str = Query(..., title="Symbol", description="Stock Symbol")):
        try:
            data = self.cash_flow_statement(symbol)
            processed_data = self.process_data(data, 'cash-flow')
            return JSONResponse(content=processed_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching cash flow data: {e}")

    def balance_sheet(self, company_code):
        url = f"https://www.screener.in/company/{company_code}/#balance-sheet"
        response = requests.get(url)
        return self.handle_response(response, company_code, 'balance-sheet')

    def get_balance_sheet(self, symbol: str = Query(..., title="Symbol", description="Stock Symbol")):
        try:
            data = self.balance_sheet(symbol)
            processed_data = self.process_data(data, 'balance-sheet')
            return JSONResponse(content=processed_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching balance sheet data: {e}")

    def annual_profit_and_loss_statement(self, company_code):
        url = f"https://www.screener.in/company/{company_code}/#profit-loss"
        response = requests.get(url)
        return self.handle_response(response, company_code, 'profit-loss')

    def get_annual_profit_and_loss_statement(self, symbol: str = Query(..., title="Symbol", description="Stock Symbol")):
        try:
            data = self.annual_profit_and_loss_statement(symbol)
            processed_data = self.process_data(data, 'profit-loss')
            return JSONResponse(content=processed_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching annual profit and loss data: {e}")

    def ratios(self, company_code):
        url = f"https://www.screener.in/company/{company_code}/#ratios"
        response = requests.get(url)
        return self.handle_response(response, company_code, 'ratios')

    def get_ratios(self, symbol: str = Query(..., title="Symbol", description="Stock Symbol")):
        try:
            data = self.ratios(symbol)
            processed_data = self.process_data(data, 'ratios')
            return JSONResponse(content=processed_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching ratios data: {e}")

    def key_metrics(self, company_code):
        url = f"https://www.screener.in/company/{company_code}/#top"
        response = requests.get(url)
        return self.handle_key_metrics_response(response, company_code)

    def get_key_metrics(self, symbol: str = Query(..., title="Symbol", description="Stock Symbol")):
        try:
            response = self.key_metrics(symbol)
            if response is not None:
                processed_data = response
                return JSONResponse(content=processed_data)
            else:
                return JSONResponse(content={"error": "Failed to fetch data from URL"}, status_code=500)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching key metrics data: {e}")
