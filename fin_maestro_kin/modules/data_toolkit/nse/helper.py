import requests
import pandas as pd
import math
from datetime import datetime

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


def fetch_data_from_nse(payload):
    try:
        result = requests.get(payload, headers=headers).json()
    except ValueError:
        session = requests.Session()
        result = session.get("http://nseindia.com", headers=headers)
        result = session.get(payload, headers=headers).json()
    return result


# Convert DataFrame to dictionary with special handling for float values
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


def transform_financial_year(financial_year):
    start_year, end_year = map(int, financial_year.split('-'))

    start_date = datetime(start_year, 4, 1)
    end_date = datetime(end_year + 1, 3, 31) 

    from_date_str = start_date.strftime("%b-%Y")
    to_date_str = end_date.strftime("%b-%Y")

    return from_date_str, to_date_str


def process_vix_data(historical_data):
    rounded_data = convert_dataframe_to_dict(historical_data)
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


def process_security_wise_archive_data(historical_data):
    rounded_data = convert_dataframe_to_dict(historical_data)
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

    
def process_bulk_block_deal_archive_data(historical_data):
    rounded_data = convert_dataframe_to_dict(historical_data)
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


def process_short_selling_archives_data(historical_data):
    rounded_data = convert_dataframe_to_dict(historical_data)
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


def process_corporate_actions_data(data):
    rounded_data = convert_dataframe_to_dict(data)
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


def process_most_active_securities_data(data):
    rounded_data = convert_dataframe_to_dict(data)
    processed_data = []
    for entry in rounded_data:
        processed_entry = {
            "security": entry["ASM_SECURITY"],
            "average_daily_turnover": entry["ASM_AVG_DLY_TURNOVER"],
            "number_of_trades": entry["ASM_NO_OF_TRADES"],
            "share_in_total_turnover": entry["ASM_SHARE_IN_TOTAL_TURNOVER"],
            "traded_quantity": entry["ASM_TRADED_QUANTITY"],
            "turnover": entry["ASM_TURNOVER"],
            "timestamp": entry["TIMESTAMP"]
        }
        processed_data.append(processed_entry)
    return processed_data


def process_monthly_advances_declines_data(data):
    rounded_data = convert_dataframe_to_dict(data)
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


def process_capital_market_monthly_settlement_stats(data):
    rounded_data = convert_dataframe_to_dict(data)
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


def process_fno_monthly_settlement_stats(data):
    rounded_data = convert_dataframe_to_dict(data)
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


def process_board_meetings_data(data):
    rounded_data = convert_dataframe_to_dict(data)
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


def process_insider_trading_data(data):
    rounded_data = convert_dataframe_to_dict(data)
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


def process_shareholding_patterns_data(data):
    rounded_data = convert_dataframe_to_dict(data)
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


def process_annual_reports_data(data):
    rounded_data = convert_dataframe_to_dict(data)
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


import json

import json

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


