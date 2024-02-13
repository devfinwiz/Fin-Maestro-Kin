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