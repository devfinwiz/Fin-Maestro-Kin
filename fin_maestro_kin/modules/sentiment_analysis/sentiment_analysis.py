from fastapi import APIRouter, Query
from .pcr_data import pcr_indice_scraper, pcr_stocks_scraper

router = APIRouter()

#Example usage - http://127.0.0.1:8000/sentiment/pcr-indice-analysis
@router.get("/sentiment/pcr-indice-analysis")
def analyze_indices():
    try:
        pcr_anal_result = pcr_indice_analysis()
        return pcr_anal_result
    except Exception as e:
        return {"error": f"An error occurred during PCR analysis: {e}"}


#Example usage - http://127.0.0.1:8000/sentiment/pcr-stocks-analysis?symbol=INFY
@router.get("/sentiment/pcr-stocks-analysis")
def analyze_stock(symbol: str = Query(..., title="Symbol", description="Stock symbol")):
    try:
        pcr_anal_result = pcr_stocks_analysis(symbol)
        return pcr_anal_result
    except Exception as e:
        return {"error": f"An error occurred during PCR analysis for {symbol}: {e}"}


def pcr_indice_analysis():
    pcr_anal_result = {}
    indices = ["NIFTY", "BANKNIFTY"]

    for symbol in indices:
        try:
            pcr_value = pcr_indice_scraper(symbol)
        except Exception as e:
            print(f"Error fetching PCR for {symbol}: {e}")
            return {"error": f"Failed to fetch PCR for {symbol}"}

        state = get_state(pcr_value, [1.4, 1.19, 1, 0.91, 0.6])
        pcr_anal_result[symbol] = [state, pcr_value]

    return pcr_anal_result


def pcr_stocks_analysis(symbol):
    try:
        pcr_anal_result = {}
        pcr_value = pcr_stocks_scraper(symbol)
    except Exception as e:
        print(f"Error fetching PCR for {symbol}: {e}")
        return {"error": f"Failed to fetch PCR for {symbol}"}

    state = get_state(pcr_value, [1, 0.75, 0.50, 0.4])
    pcr_anal_result[symbol] = [state, pcr_value]

    return pcr_anal_result


def get_state(pcr_value, thresholds):
    for threshold, label in zip(thresholds, ["Overbought", "Slightly overbought", "Neutral", "Slightly oversold"]):
        if pcr_value >= threshold:
            return label

    return "Oversold"
