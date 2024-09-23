import requests
import pandas as pd
import json
import math
import re
import datetime
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse


class Helper:
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

    niftyindices_headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'DNT': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        'Content-Type': 'application/json; charset=UTF-8',
        'Origin': 'https://niftyindices.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://niftyindices.com/reports/historical-data',
        'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
    }

    @staticmethod
    def fetch_data_from_nse(payload):
        try:
            result = requests.get(payload, headers=Helper.headers).json()
        except ValueError:
            session = requests.Session()
            result = session.get("http://nseindia.com", headers=Helper.headers)
            result = session.get(payload, headers=Helper.headers).json()
        return result

    @staticmethod
    def convert_dataframe_to_dict(df):
        df_dict = df.to_dict(orient='records')
        for record in df_dict:
            for key, value in record.items():
                if isinstance(value, float):
                    if pd.notna(value) and math.isfinite(value):
                        record[key] = round(value, 2)
                    else:
                        record[key] = str(value)
        return df_dict

    @staticmethod
    def transform_financial_year(financial_year):
        from datetime import datetime
        start_year, end_year = map(int, financial_year.split('-'))

        start_date = datetime(start_year, 4, 1)
        end_date = datetime(end_year + 1, 3, 31) 

        from_date_str = start_date.strftime("%b-%Y")
        to_date_str = end_date.strftime("%b-%Y")

        return from_date_str, to_date_str

    @staticmethod
    def process_vix_data(historical_data):
        rounded_data = Helper.convert_dataframe_to_dict(historical_data)
        processed_data = []
        for entry in rounded_data:
            processed_entry = {
                "date": entry["EOD_TIMESTAMP"],
                "index_name": entry["EOD_INDEX_NAME"],
                "open_value": entry["EOD_OPEN_INDEX_VAL"],
                "close_value": entry["EOD_CLOSE_INDEX_VAL"],
                "high_value": entry["EOD_HIGH_INDEX_VAL"],
                "low_value": entry["EOD_LOW_INDEX_VAL"],
                "previous_close": entry["EOD_PREV_CLOSE"],
                "points_change": entry["VIX_PTS_CHG"],
                "percentage_change": entry["VIX_PERC_CHG"]
            }
            processed_data.append(processed_entry)
        return processed_data

    @staticmethod
    def process_security_wise_archive_data(historical_data):
        rounded_data = Helper.convert_dataframe_to_dict(historical_data)
        processed_data = []
        for entry in rounded_data:
            processed_entry = {
                "date": entry["CH_TIMESTAMP"],
                "symbol": entry["CH_SYMBOL"],
                "series": entry["CH_SERIES"],
                "high_price": entry["CH_TRADE_HIGH_PRICE"],
                "low_price": entry["CH_TRADE_LOW_PRICE"],
                "opening_price": entry["CH_OPENING_PRICE"],
                "closing_price": entry["CH_CLOSING_PRICE"],
                "last_traded_price": entry["CH_LAST_TRADED_PRICE"],
                "previous_close": entry["CH_PREVIOUS_CLS_PRICE"],
                "total_traded_qty": entry["CH_TOT_TRADED_QTY"],
                "total_traded_val": entry["CH_TOT_TRADED_VAL"],
                "52_week_high_price": entry["CH_52WEEK_HIGH_PRICE"],
                "52_week_low_price": entry["CH_52WEEK_LOW_PRICE"],
                "total_trades": entry["CH_TOTAL_TRADES"]
            }
            processed_data.append(processed_entry)
        return processed_data

    @staticmethod
    def process_bulk_block_deal_archive_data(historical_data):
        rounded_data = Helper.convert_dataframe_to_dict(historical_data)
        processed_data = []
        for entry in rounded_data:
            processed_entry = {
                "date": entry["BD_DT_DATE"],
                "symbol": entry["BD_SYMBOL"],
                "script_name": entry["BD_SCRIP_NAME"],
                "client_name": entry["BD_CLIENT_NAME"],
                "transaction_type": entry["BD_BUY_SELL"],
                "quantity": entry["BD_QTY_TRD"],
                "Trade Price/Weighted Average Trade Price": entry["BD_TP_WATP"],
            }
            processed_data.append(processed_entry)
        return processed_data

    @staticmethod
    def process_short_selling_archives_data(historical_data):
        rounded_data = Helper.convert_dataframe_to_dict(historical_data)
        processed_data = []
        for entry in rounded_data:
            processed_entry = {
                "date": entry["SS_DATE"],
                "name": entry["SS_NAME"],
                "symbol": entry["SS_SYMBOL"],
                "quantity": entry["SS_QTY"],
            }
            processed_data.append(processed_entry)
        return processed_data

    @staticmethod
    def process_corporate_actions_data(data):
        rounded_data = Helper.convert_dataframe_to_dict(data)
        processed_data = []
        for entry in rounded_data:
            processed_entry = {
                "symbol": entry["symbol"],
                "series": entry["series"],
                "industry": entry["ind"],
                "face_value": entry["faceVal"],
                "subject": entry["subject"],
                "ex_date": entry["exDate"],
                "record_date": entry["recDate"],
                "bc_start_date": entry["bcStartDate"],
                "bc_end_date": entry["bcEndDate"],
                "company": entry["comp"],
            }
            processed_data.append(processed_entry)
        return processed_data

    @staticmethod
    def process_most_active_securities_data(data):
        rounded_data = Helper.convert_dataframe_to_dict(data)
        processed_data = []
        for entry in rounded_data:
            processed_entry = {
                "symbol": entry["symbol"],
                "last_price": entry["lastPrice"],
                "percentage_change": entry["pChange"],
                "total_traded_volume": entry["totalTradedVolume"],
                "traded_quantity": entry["quantityTraded"],
                "total_traded_value": entry["totalTradedValue"],
                "previous_close": entry["previousClose"],
                "ex_date": entry["exDate"],
                "purpose": entry["purpose"],
                "year_high": entry["yearHigh"],
                "year_low": entry["yearLow"]
            }
            processed_data.append(processed_entry)
        return processed_data

    @staticmethod
    def process_monthly_advances_declines_data(data):
        rounded_data = Helper.convert_dataframe_to_dict(data)
        processed_data = []
        for entry in rounded_data:
            processed_entry = {
                "record_type": entry["ADM_REC_TY"],
                "month": entry["ADM_MONTH_YEAR_STRING"],
                "advances": entry["ADM_ADVANCES"],
                "declines": entry["ADM_DECLINES"],
                "advances_declines_ratio": entry["ADM_ADV_DCLN_RATIO"]
            }
            processed_data.append(processed_entry)
        return processed_data

    @staticmethod
    def process_capital_market_monthly_settlement_stats(data):
        rounded_data = Helper.convert_dataframe_to_dict(data)
        processed_data = []
        for entry in rounded_data:
            processed_entry = {
                "start_date": entry["ST_DATE"],
                "delivered_quantity_lacs": entry["ST_DELIVERED_QTY_LACS"],
                "delivered_value_crores": entry["ST_DELIVERED_VALUE_CRORES"],
                "funds_payin_crores": entry["ST_FUNDS_PAYIN_CRORES"],
                "number_of_trades_lacs": entry["ST_NO_OF_TRADES_LACS"],
                "percentage_delivered_to_traded_quantity": entry["ST_PERC_DLVRD_TO_TRADED_QTY"],
                "percentage_delivered_value_to_turnover": entry["ST_PERC_DLVRD_VAL_TO_TURNOVER"],
                "percentage_short_delivery_to_delivery": entry["ST_PERC_SHORT_DLVRY_TO_DLVRY"],
                "percentage_short_delivery_value_delivery": entry["ST_PERC_SHORT_DLVRY_VAL_DLVRY"],
                "settlement_number": entry["ST_SETTLEMENT_NO"],
                "short_delivery_auc_quantity_lacs": entry["ST_SHORT_DLVRY_AUC_QTY_LACS"],
                "short_delivery_value": entry["ST_SHORT_DLVRY_VALUE"],
                "traded_quantity_lacs": entry["ST_TRADED_QTY_LACS"],
                "turnover_crores": entry["ST_TURNOVER_CRORES"]
            }
            processed_data.append(processed_entry)
        return processed_data

    @staticmethod
    def process_fno_monthly_settlement_stats(data):
        rounded_data = Helper.convert_dataframe_to_dict(data)
        processed_data = []
        for entry in rounded_data:
            processed_entry = {
                "start_date": entry["st_date"],
                "mtm": entry["st_Mtm"],
                "final": entry["st_Final"],
                "premium": entry["st_Premium"],
                "exercise": entry["st_Excercise"],
                "total": entry["st_Total"]
            }
            processed_data.append(processed_entry)
        return processed_data

    @staticmethod
    def process_board_meetings_data(data):
        rounded_data = Helper.convert_dataframe_to_dict(data)
        processed_data = []
        for entry in rounded_data:
            processed_entry = {
                "start_date": entry["bm_date"],
                "symbol": entry["bm_symbol"],
                "purpose": entry["bm_purpose"],
                "description": entry["bm_desc"],
                "company_name": entry["sm_name"],
            }
            processed_data.append(processed_entry)
        return processed_data

    @staticmethod
    def process_insider_trading_data(data):
        rounded_data = Helper.convert_dataframe_to_dict(data)
        processed_data = []
        for entry in rounded_data:
            processed_entry = {
                "symbol": entry["symbol"],
                "company": entry["company"],
                "acquirer": entry["acqName"],
                "broadcast_date": entry["date"],
                "security_type": entry["secType"],
                "transaction_type": entry["tdpTransactionType"],
                "acquirer_category": entry["personCategory"],
                "no_of_securities": entry["secAcq"]
            }
            processed_data.append(processed_entry)
        return processed_data

    @staticmethod
    def process_shareholding_patterns_data(data):
        rounded_data = Helper.convert_dataframe_to_dict(data)
        processed_data = []
        for entry in rounded_data:
            processed_entry = {
                "symbol": entry["symbol"],
                "company": entry["name"],
                "as_on_date": entry["date"],
                "promoter_and_promoter_group": entry["pr_and_prgrp"],
                "public": entry["public_val"],
                "employee_trusts": entry["employeeTrusts"],
                "submission_date": entry["submissionDate"]
            }
            processed_data.append(processed_entry)
        return processed_data

    @staticmethod
    def process_annual_reports_data(data):
        rounded_data = Helper.convert_dataframe_to_dict(data)
        processed_data = []
        for entry in rounded_data:
            processed_entry = {
                "company": entry["companyName"],
                "from_year": entry["fromYr"],
                "to_year": entry["toYr"],
                "attachment": entry["fileName"],
            }
            processed_data.append(processed_entry)
        return processed_data

    @staticmethod
    def process_index_data(data):
        data_json = data.to_json(orient="records")

        try:
            data = json.loads(data_json)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON data"}

        processed_data = []
        for entry in data:
            processed_entry = {
                "index_name": entry["indexCloseOnlineRecords"]["EOD_INDEX_NAME"],
                "open_value": entry["indexCloseOnlineRecords"]["EOD_OPEN_INDEX_VAL"],
                "high_value": entry["indexCloseOnlineRecords"]["EOD_HIGH_INDEX_VAL"],
                "close_value": entry["indexCloseOnlineRecords"]["EOD_CLOSE_INDEX_VAL"],
                "low_value": entry["indexCloseOnlineRecords"]["EOD_LOW_INDEX_VAL"],
                "timestamp": entry["indexCloseOnlineRecords"]["EOD_TIMESTAMP"],
                "traded_quantity": entry["indexTurnoverRecords"]["HIT_TRADED_QTY"],
                "turnover": entry["indexTurnoverRecords"]["HIT_TURN_OVER"]
            }
            processed_data.append(processed_entry)
        return processed_data
    
    @staticmethod
    def process_index_ratios(historical_data):
        rounded_data = Helper.convert_dataframe_to_dict(historical_data)
        processed_data = []
        for entry in rounded_data:
            processed_entry = {
                "index_name": entry["INDEX_NAME"],
                "date": entry["HistoricalDate"],
                "open": entry["OPEN"],
                "high": entry["HIGH"],
                "low": entry["LOW"],
                "close": entry["CLOSE"],
            }
            processed_data.append(processed_entry)   
        return processed_data
    

class NSEIndices(Helper):
    def __init__(self):
        self.router = APIRouter(tags=["NSE Indices"])
    
    def register_routes(self, app):
        self.router.add_api_route("/nseindices/history", self.get_nse_index_history, methods=["GET"], tags=["NSE Indices"])
        self.router.add_api_route("/nseindices/ratios", self.get_nse_indices_ratios, methods=["GET"], tags=["NSE Indices"])
        self.router.add_api_route("/nseindices/returns", self.get_nse_indices_returns, methods=["GET"], tags=["NSE Indices"])
        self.router.add_api_route("/nseindices/indice-pcr", self.get_pcr, methods=["GET"], tags=["NSE Indices"])
        self.router.add_api_route("/nseindices/india-vix", self.get_india_vix_history, methods=["GET"], tags=["NSE Indices"])
        self.router.add_api_route("/nseindices/index-symbols", self.get_index_symbols, methods=["GET"], tags=["NSE Indices"])
        app.include_router(self.router)
        
    def index_history(self, symbol, start_date, end_date):
        base_url="https://www.nseindia.com/api/historical/indicesHistory"
        customized_request_url = f"{base_url}?indexType={symbol}&from={start_date}&to={end_date}"
        response=self.fetch_data_from_nse(customized_request_url)
        
        payload = response.get('data', [])
        
        if not payload:
            raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
        
        return pd.DataFrame(payload)

    def get_nse_index_history(
        self,
        symbol: str = Query(..., title="Symbol", description="NSE indices symbol"),
        start_date: str = Query(..., title="Start Date", description="Start date for historical data in dd-mm-yyyy format"),
        end_date: str = Query(..., title="End Date", description="End date for historical data in dd-mm-yyyy format")
    ):
        try:
            history_data = self.index_history(symbol, start_date, end_date)
            processed_data = self.process_index_data(history_data)
            return JSONResponse(content={"index_historical_data": processed_data})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching historical data: {e}")
        
    def index_pe_pb_div(self, symbol, start_date, end_date, index_name):
        start_date = datetime.datetime.strptime(start_date, "%d-%b-%Y").strftime("%d %b %Y")
        end_date = datetime.datetime.strptime(end_date, "%d-%b-%Y").strftime("%d %b %Y")
        
        data = {"cinfo": f"{{'name':'{symbol}','startDate':'{start_date}','endDate':'{end_date}','indexName':'{index_name}'}}"}
        payload = requests.post('https://niftyindices.com/Backpage.aspx/getHistoricaldatatabletoString', headers=self.niftyindices_headers, json=data).json()
        payload = json.loads(payload["d"])
        
        if not payload:
            raise HTTPException(status_code=404, detail="No historical data found.")
        
        payload=pd.DataFrame.from_records(payload)
        return payload

    def get_nse_indices_ratios(
        self,
        symbol: str = Query(..., title="Symbol", description="Nifty indices symbol"),
        start_date: str = Query(..., title="Start Date", description="Start date for historical data in dd-mmm-yyyy format"),
        end_date: str = Query(..., title="End Date", description="End date for historical data in dd-mmm-yyyy format"),
        index_name: str = Query(..., title="Index Name", description="Nifty index name")
    ):
        try:
            historical_ratios_data = self.index_pe_pb_div(symbol, start_date, end_date, index_name)
            processed_data = self.process_index_ratios(historical_ratios_data)
            return processed_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching historical ratios data: {e}")
        
    def index_total_returns(self, symbol,start_date,end_date, index_name):
        start_date = datetime.datetime.strptime(start_date, "%d-%b-%Y").strftime("%d %b %Y")
        end_date = datetime.datetime.strptime(end_date, "%d-%b-%Y").strftime("%d %b %Y")
        
        data = {"cinfo": f"{{'name':'{symbol}','startDate':'{start_date}','endDate':'{end_date}','indexName':'{index_name}'}}"}
        payload = requests.post('https://niftyindices.com/Backpage.aspx/getTotalReturnIndexString', headers=self.niftyindices_headers, json=data).json()
        payload = json.loads(payload["d"])
        
        if not payload:
            raise HTTPException(status_code=404, detail="No historical data found.")
        
        payload=pd.DataFrame.from_records(payload)
        return payload

    def get_nse_indices_returns(
        self,
        symbol: str = Query(..., title="Symbol", description="Nifty indices symbol"),
        start_date: str = Query(..., title="Start Date", description="Start date for historical data in dd-mmm-yyyy format"),
        end_date: str = Query(..., title="End Date", description="End date for historical data in dd-mmm-yyyy format"),
        index_name: str = Query(..., title="Index Name", description="Nifty index name")
    ):
        try:
            historical_returns_data = self.index_total_returns(symbol, start_date, end_date, index_name)
            return historical_returns_data.to_dict(orient='records')
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching historical ratios data: {e}")
        
    def get_pcr(
        self,
        symbol: str = Query(..., title="Symbol", description="Indice symbol")
    ):
        pcr_value = self.pcr_indice_scraper(symbol)
        return {"symbol": symbol, "pcr_value": pcr_value}

    def pcr_indice_scraper(self, symbol):
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

    def india_vix_history(self, start_date, end_date):
        base_url="https://www.nseindia.com/api/historical/vixhistory"
        customized_request_url = f"{base_url}?from={start_date}&to={end_date}"
        response = self.fetch_data_from_nse(customized_request_url)
        
        payload = response.get('data', [])
        
        if not payload:
            raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
        
        return pd.DataFrame(payload)

    def get_india_vix_history(
        self,
        start_date: str = Query(..., title="From Date", description="Start date for historical data in dd-mm-yyyy format"),
        end_date: str = Query(..., title="To Date", description="End date for historical data in dd-mm-yyyy format"),  
    ):
        try:
            historical_data = self.india_vix_history(start_date, end_date)
            processed_data = self.process_vix_data(historical_data)
            return JSONResponse(content={"vix_data": processed_data})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching India Vix historical data: {e}")
        
    def fetch_index_symbols(self):
        url = 'https://nseindia.com/api/allIndices'
        try:
            response = self.fetch_data_from_nse(url) 
            data = response.get('data', [])
            index_symbols = [entry['indexSymbol'] for entry in data]
            return index_symbols
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching index symbols: {e}")

    def get_index_symbols(self):
        return {"index_symbols": self.fetch_index_symbols()}


class NSEEquities(Helper):
    def __init__(self):
        self.router = APIRouter(tags=["NSE Equities"])
        
    def register_routes(self, app):
        self.router.add_api_route("/equities/security-archives", self.get_security_wise_archive, methods=["GET"], tags=["NSE Equities"])
        self.router.add_api_route("/equities/bulk-deals-archives", self.get_bulk_deals_archives, methods=["GET"], tags=["NSE Equities"])
        self.router.add_api_route("/equities/block-deals-archives", self.get_block_deals_archives, methods=["GET"], tags=["NSE Equities"])
        self.router.add_api_route("/equities/short-selling-archives", self.get_short_selling_archives, methods=["GET"], tags=["NSE Equities"])
        self.router.add_api_route("/equities/corporate-actions", self.get_corporate_actions, methods=["GET"], tags=["NSE Equities"])
        self.router.add_api_route("/equities/most-active-securities", self.get_nse_monthly_most_active_securities, methods=["GET"], tags=["NSE Equities"])
        self.router.add_api_route("/equities/advances-declines", self.get_nse_monthly_advances_and_declines, methods=["GET"], tags=["NSE Equities"])
        self.router.add_api_route("/equities/monthly-settlement-stats/capital-market", self.get_nse_capital_market_monthly_settlement_stats, methods=["GET"], tags=["NSE Equities"])
        self.router.add_api_route("/equities/monthly-settlement-stats/fno", self.get_nse_fno_monthly_settlement_stats, methods=["GET"], tags=["NSE Equities"])
        self.router.add_api_route("/equities/stock-pcr", self.get_pcr, methods=["GET"], tags=["NSE Equities"])
        self.router.add_api_route("/equities/equity-tickers", self.get_nse_equity_tickers, methods=["GET"], tags=["NSE Equities"])
        self.router.add_api_route("/equities/board-meetings", self.get_board_meetings, methods=["GET"], tags=["NSE Equities"])
        self.router.add_api_route("/equities/insider-trading", self.get_insider_trading, methods=["GET"], tags=["NSE Equities"])
        self.router.add_api_route("/equities/shareholding-patterns", self.get_shareholding_patterns, methods=["GET"], tags=["NSE Equities"])
        self.router.add_api_route("/equities/annual-reports", self.get_annual_reports, methods=["GET"], tags=["NSE Equities"])
        app.include_router(self.router)
    
    def security_wise_archive(self, symbol, start_date, end_date, series="ALL"):   
        base_url = "https://www.nseindia.com/api/historical/securityArchives"
        customized_request_url = f"{base_url}?from={start_date}&to={end_date}&symbol={symbol.upper()}&dataType=priceVolumeDeliverable&series={series.upper()}"
        response = self.fetch_data_from_nse(customized_request_url)
        
        payload = response.get('data', [])
        
        if not payload:
            raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
        
        return pd.DataFrame(payload)

    def get_security_wise_archive(
        self,
        symbol: str = Query(..., title="Symbol", description="Stock symbol"),
        start_date: str = Query(..., title="From Date", description="Start date for historical data in dd-mm-yyyy format"),
        end_date: str = Query(..., title="To Date", description="End date for historical data in dd-mm-yyyy format"),
        series: str = Query("ALL", title="Series", description="Stock series")
    ):
        try:
            historical_data = self.security_wise_archive(symbol, start_date, end_date, series)
            processed_data = self.process_security_wise_archive_data(historical_data)
            return JSONResponse(content={"stock_data": processed_data})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching security-wise archive data: {e}")
        
    def bulk_deals_archives(self, start_date, end_date):
        base_url = "https://www.nseindia.com/api/historical/bulk-deals"
        customized_request_url = f"{base_url}?from={start_date}&to={end_date}"
        response = self.fetch_data_from_nse(customized_request_url)
        
        payload = response.get('data', [])
        
        if not payload:
            raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
        
        return pd.DataFrame(payload)

    def get_bulk_deals_archives(
        self,
        start_date: str = Query(..., title="From Date", description="Start date for historical data in dd-mm-yyyy format"),
        end_date: str = Query(..., title="To Date", description="End date for historical data in dd-mm-yyyy format"),  
    ):
        try:
            historical_data = self.bulk_deals_archives(start_date, end_date)
            processed_data = self.process_bulk_block_deal_archive_data(historical_data)
            return JSONResponse(content={"bulk_deal_archive_data": processed_data})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching bulk-deals archive data: {e}")
        
    def block_deals_archives(self, start_date, end_date):
        base_url = "https://www.nseindia.com/api/historical/block-deals"
        customized_request_url = f"{base_url}?from={start_date}&to={end_date}"
        response = self.fetch_data_from_nse(customized_request_url)
        
        payload = response.get('data', [])
        
        if not payload:
            raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
        
        return pd.DataFrame(payload)

    def get_block_deals_archives(
        self,
        start_date: str = Query(..., title="From Date", description="Start date for historical data in dd-mm-yyyy format"),
        end_date: str = Query(..., title="To Date", description="End date for historical data in dd-mm-yyyy format"),  
    ):
        try:
            historical_data = self.block_deals_archives(start_date, end_date)
            processed_data = self.process_bulk_block_deal_archive_data(historical_data)
            return JSONResponse(content={"block_deal_archive_data": processed_data})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching block deals archive data: {e}")
        
    def short_selling_archives(self, start_date, end_date):
        base_url = "https://www.nseindia.com/api/historical/short-selling"
        customized_request_url = f"{base_url}?from={start_date}&to={end_date}"
        response = self.fetch_data_from_nse(customized_request_url)
        
        payload = response.get('data', [])
        
        if not payload:
            raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
        
        return pd.DataFrame(payload)

    def get_short_selling_archives(
        self,
        start_date: str = Query(..., title="From Date", description="Start date for historical data in dd-mm-yyyy format"),
        end_date: str = Query(..., title="To Date", description="End date for historical data in dd-mm-yyyy format"),  
    ):
        try:
            historical_data = self.short_selling_archives(start_date, end_date)
            processed_data = self.process_short_selling_archives_data(historical_data)
            return JSONResponse(content={"short_selling_archive_data": processed_data})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching short-selling archive data: {e}")

    def corporate_actions(self, start_date, end_date):
        base_url = "https://www.nseindia.com/api/corporates-corporateActions"
        
        customized_request_url = f"{base_url}?index=equities&from={start_date}&to={end_date}"
        response = self.fetch_data_from_nse(customized_request_url)
        
        if not response:
            raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
        
        if isinstance(response, list):
            payload = response
        else:
            payload = response.get('data', [])
        
        return pd.DataFrame(payload)
        
    def get_corporate_actions(
        self,
        start_date: str = Query(..., title="From Date", description="Start date for data in dd-mm-yyyy format"),
        end_date: str = Query(..., title="To Date", description="End date for data in dd-mm-yyyy format"),  
    ):
        try:
            data = self.corporate_actions(start_date, end_date)
            processed_data = self.process_corporate_actions_data(data)
            return JSONResponse(content={"corporate_actions_data": processed_data})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching corporate actions data: {e}")
        
    def nse_monthly_most_active_securities(self):
        request_url = "https://www.nseindia.com/api/live-analysis-most-active-securities?index=volume"
        response = self.fetch_data_from_nse(request_url)
        payload = response.get('data', [])
        
        if not payload:
            raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
        
        return pd.DataFrame(payload)
        
    def get_nse_monthly_most_active_securities(self):
        try:
            historical_data = self.nse_monthly_most_active_securities()
            processed_data = self.process_most_active_securities_data(historical_data)
            return JSONResponse(content={"most_active_securities_data": processed_data})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching monthly most active securities data: {e}")
        
    def nse_monthly_advances_and_declines(self, year):
        base_url="https://www.nseindia.com/api/historical/advances-decline-monthly"
        customized_request_url = f"{base_url}?year={year}"
        response = self.fetch_data_from_nse(customized_request_url)
        
        payload = response.get('data', [])
        
        if not payload:
            raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
        
        return pd.DataFrame(payload)

    def get_nse_monthly_advances_and_declines(
        self,
        year: str = Query(..., title="Year", description="Year for historical data in format YYYY"), 
    ):
        if not re.match(r"\d{4}", year):
            raise HTTPException(status_code=422, detail="Invalid year format. Please use 'YYYY' format.")
        
        try:
            historical_data = self.nse_monthly_advances_and_declines(year)
            processed_data = self.process_monthly_advances_declines_data(historical_data)
            return JSONResponse(content={"monthly_advances_and_declines_data": processed_data})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching advances and declines data: {e}")
        
    def nse_capital_market_monthly_settlement_stats(self, financial_year):
        base_url = "https://www.nseindia.com/api/historical/monthly-sett-stats-data"
        customized_request_url = f"{base_url}?finYear={financial_year}"
        response = self.fetch_data_from_nse(customized_request_url)
        payload = response.get('data', [])
        
        if not payload:
            raise HTTPException(status_code=404, detail=f"No capital market settlement statistics found.")
        
        return pd.DataFrame(payload)

    def get_nse_capital_market_monthly_settlement_stats(
        self,
        financial_year: str = Query(..., title="Year", description="Financial Year for historical data in format YYYY-YYYY"), 
    ):
        if not re.match(r"\d{4}-\d{4}", financial_year):
            raise HTTPException(status_code=422, detail="Invalid financial year format. Please use 'YYYY-YYYY' format.")
        
        try:
            historical_data = self.nse_capital_market_monthly_settlement_stats(financial_year)
            processed_data = self.process_capital_market_monthly_settlement_stats(historical_data)
            return JSONResponse(content={"capital_market_monthly_settlement_stats_data": processed_data})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching monthly settlement statistics for capital market: {e}")

    def nse_fno_monthly_settlement_stats(self, financial_year):
        from_date, to_date = self.transform_financial_year(financial_year)
        base_url = "https://www.nseindia.com/api/financial-monthlyStats"
        customized_request_url = f"{base_url}?from_date={from_date}&to_date={to_date}"
        response = self.fetch_data_from_nse(customized_request_url)
        payload = response 
        
        if not payload:
            raise HTTPException(status_code=404, detail="No monthly settlement statistics found.")
        
        return pd.DataFrame(payload)

    def get_nse_fno_monthly_settlement_stats(
        self,
        financial_year: str = Query(..., title="Year", description="Financial Year for historical data in format YYYY-YYYY"), 
    ):
        if not re.match(r"\d{4}-\d{4}", financial_year):
            raise HTTPException(status_code=422, detail="Invalid financial year format. Please use 'YYYY-YYYY' format.")
        
        try:
            historical_data = self.nse_fno_monthly_settlement_stats(financial_year)
            
            if not isinstance(historical_data, pd.DataFrame):
                raise HTTPException(status_code=404, detail="No data found.")
            
            processed_data = self.process_fno_monthly_settlement_stats(historical_data)
            return JSONResponse(content={"fno_monthly_settlement_stats_data": processed_data})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching monthly settlement statistics for future & options: {e}")
        
    def pcr_stocks_scraper(self, symbol):
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

    def get_pcr(self, symbol: str = Query(..., title="Symbol", description="Stock symbol")):
        pcr_value = self.pcr_stocks_scraper(symbol)
        return {"symbol": symbol, "pcr_value": pcr_value}

    def nse_equity_tickers(self):
        try:
            indices = ['NIFTY 50', 'NIFTY NEXT 50', 'NIFTY 500']
            base_url = 'https://www.nseindia.com/api/equity-stockIndices?index='
            
            tickers = []
            
            for index in indices:
                url = base_url + index.replace(' ', '%20')
                response = self.fetch_data_from_nse(url)
                response.raise_for_status()
                data = response.json()
                
                for stock in data['data']:
                    tickers.append(stock['symbol'])
            
            return list(set(tickers))
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching equity tickers: {e}")

    def get_nse_equity_tickers(self):
        return {"equity_tickers": self.nse_equity_tickers()}

    def board_meetings(self, start_date, end_date):
        base_url = "https://www.nseindia.com/api/corporate-board-meetings"
        
        customized_request_url = f"{base_url}?index=equities&from={start_date}&to={end_date}"
        response = self.fetch_data_from_nse(customized_request_url)
        
        if not response:
            raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
        
        if isinstance(response, list):
            payload = response
        else:
            payload = response.get('data', [])
        
        return pd.DataFrame(payload)
        
    def get_board_meetings(
        self,
        start_date: str = Query(..., title="From Date", description="Start date for data in dd-mm-yyyy format"),
        end_date: str = Query(..., title="To Date", description="End date for data in dd-mm-yyyy format"),  
    ):
        try:
            data = self.board_meetings(start_date, end_date)
            processed_data = self.process_board_meetings_data(data)
            return JSONResponse(content={"board_meetings_data": processed_data})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching board meetings data: {e}")
        
    def insider_trading(self, start_date, end_date):
        base_url = "https://www.nseindia.com/api/corporates-pit"
        
        customized_request_url = f"{base_url}?index=equities&from={start_date}&to={end_date}"
        response = self.fetch_data_from_nse(customized_request_url)
        
        if not response:
            raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
        
        if isinstance(response, list):
            payload = response
        else:
            payload = response.get('data', [])
        
        return pd.DataFrame(payload)
        
    def get_insider_trading(
        self,
        start_date: str = Query(..., title="From Date", description="Start date for data in dd-mm-yyyy format"),
        end_date: str = Query(..., title="To Date", description="End date for data in dd-mm-yyyy format"),  
    ):
        try:
            data = self.insider_trading(start_date, end_date)
            processed_data = self.process_insider_trading_data(data)
            return JSONResponse(content={"insider_trading_data": processed_data})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching insider_trading data: {e}")
        
    def shareholding_patterns(self, symbol):
        base_url = "https://www.nseindia.com/api/corporate-share-holdings-master"
        
        customized_request_url = f"{base_url}?index=equities&symbol={symbol}"
        response = self.fetch_data_from_nse(customized_request_url)
        
        if not response:
            raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
        
        if isinstance(response, list):
            payload = response
        else:
            payload = response.get('data', [])
        return pd.DataFrame(payload)
        
    def get_shareholding_patterns(
        self,
        symbol: str = Query(..., title="Symbol", description="Stock Symbol")
    ):
        try:
            data = self.shareholding_patterns(symbol)
            processed_data = self.process_shareholding_patterns_data(data)
            return JSONResponse(content={"shareholding_patterns_data": processed_data})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching shareholding patterns data: {e}")
         
    def annual_reports(self, symbol):
        base_url = "https://www.nseindia.com/api/annual-reports"
        
        customized_request_url = f"{base_url}?index=equities&symbol={symbol}"
        response = self.fetch_data_from_nse(customized_request_url)
        
        if not response:
            raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
        
        if isinstance(response, list):
            payload = response
        else:
            payload = response.get('data', [])
        return pd.DataFrame(payload)
        
    def get_annual_reports(
        self,
        symbol: str = Query(..., title="Symbol", description="Stock Symbol")
    ):
        try:
            data = self.annual_reports(symbol)
            processed_data = self.process_annual_reports_data(data)
            return JSONResponse(content={"annual_reports_data": processed_data})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching annual reports data: {e}")