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
        url = f"https://www.screener.in/company/{company_code}/consolidated/#quarters"
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
        url = f"https://www.screener.in/company/{company_code}/consolidated"
        response = requests.get(url)
        return self.handle_key_metrics_response(response, company_code)

    def get_key_metrics(self, symbol: str = Query(..., title="Symbol", description="Stock Symbol")):
        try:
            response = self.key_metrics(symbol)
            if response is None:
                return JSONResponse(content={"error": "Failed to fetch key metrics data"}, status_code=500)
            processed_data = response

            #-----------------------------------------------------
            # Add last 4 quarter's eps and ttm eps in key metrics
            # Add last 4 quarter's OPM % in key metrics
            #-----------------------------------------------------
            quarterly_data = self.quarterly_results(symbol)
            quarters_data = self.process_data(quarterly_data, 'quarters')
            hold = quarters_data.get("quarters", {})
            eps_dict = hold.get("EPS in Rs", {})

            if eps_dict:
                eps_values = [eps_dict[q] for q in list(eps_dict.keys())[-4:] if eps_dict[q] not in ["", "-", None]]
                eps_values_float = []

                for v in eps_values:
                    try:
                        eps_values_float.append(float(v))
                    except Exception:
                        pass 

                for i, eps_val in enumerate(eps_values_float, start=1):
                    processed_data["key_metrics"][f"EPS (Q{i})"] = str(eps_val)

                ttm_eps = round(sum(eps_values_float), 2) if eps_values_float else None
                if ttm_eps is not None:
                    processed_data["key_metrics"]["EPS (TTM)"] = str(ttm_eps)

            opm_percentage = hold.get("OPM %", {})
            if opm_percentage:
                opm_percentage = [opm_percentage[q] for q in list(opm_percentage.keys())[-4:] if opm_percentage[q] not in ["", "-", None]]
                
                for i, opm_val in enumerate(opm_percentage, start=1):
                    processed_data["key_metrics"][f"OPM% (Q{i})"] = opm_val

            #-----------------------------------------------------
            # Add last 4 quarter's promoter holding in key metrics
            # Add change in promoter holding in key metrics
            #-----------------------------------------------------
            shareholding_pattern = self.shareholding_pattern(symbol)
            shareholding_data = self.process_data(shareholding_pattern, 'shareholding')
            hold = shareholding_data.get("shareholding", {})
            promoter_holding = hold.get("Promoters", {})

            if promoter_holding:
                promoter_holding = [promoter_holding[q] for q in list(promoter_holding.keys())[-4:] if promoter_holding[q] not in ["", "-", None]]
                change_in_promoter_holding = round(float(promoter_holding[0]) - float(promoter_holding[3]), 2)

                for i, promoter_value in enumerate(promoter_holding, start=1):
                    processed_data["key_metrics"][f"Promoters (Q{i})"] = promoter_value
                processed_data["key_metrics"][f"Change in promoter holding"] = str(change_in_promoter_holding)
            
            #-----------------------------------------------------
            # Add P/S ratio in key metrics
            #-----------------------------------------------------
            hold = quarters_data.get("quarters", {})
            sales_data = hold.get("Sales", {})

            if sales_data:
                sales_data = [sales_data[q] for q in list(sales_data.keys())[-4:] if sales_data[q] not in ["", "-", None]]
                sales_values_float = []

                for v in sales_data:
                    try:
                        sales_values_float.append(float(v))
                    except Exception:
                        pass 
            
                ttm_sales = round(sum(sales_values_float), 2) if sales_values_float else None
                if ttm_sales is not None:
                    processed_data["key_metrics"]["Sales (TTM)"] = str(ttm_sales)
            
                mcap = processed_data["key_metrics"]["Market Cap"]
                price_to_sales = round(float(mcap) / ttm_sales, 2)
                processed_data["key_metrics"]["Price/Sales"] = str(price_to_sales)

            return JSONResponse(content=processed_data)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching key metrics data: {e}")
