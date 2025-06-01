from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from ..data_toolkit.screener.screener_equities import ScreenerEquities
import math
import json

class ValuationEngine:
    def __init__(self):
        self.router = APIRouter(tags=["Valuations"])
        self.screener = ScreenerEquities()
    
    def register_routes(self, app):
        self.router.add_api_route("/valuations/graham-number", self.get_valuation_by_graham_model, methods=["GET"], tags=["Valuations"])
        self.router.add_api_route("/valuations/earnings", self.get_valuation_by_earnings, methods=["GET"], tags=["Valuations"])
        self.router.add_api_route("/valuations/get-valuation-verdict", self.get_valuation_verdict, methods=["GET"], tags=["Valuations"])
        app.include_router(self.router)

    def compute_graham_number(self, company_code):
        response = self.screener.get_key_metrics(company_code)
        data = json.loads(response.body)
        key_metrics = data.get("key_metrics", {})

        book_value = float(key_metrics.get("Book Value", 0))
        eps_ttm = float(key_metrics.get("EPS (TTM)", 0))

        if book_value <= 0 or eps_ttm <= 0:
            return -1
        return round(math.sqrt(22.5 * eps_ttm * book_value), 2)

    def get_valuation_by_graham_model(self, symbol: str = Query(..., title="Symbol", description="Stock symbol")):
        try:
            graham_number = self.compute_graham_number(symbol)

            return JSONResponse(content={
                "symbol": symbol,
                "graham_number": graham_number
            })
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error calculating Graham Number: {e}")
        
    def compute_earnings_valuation(self, company_code):
        response = self.screener.get_key_metrics(company_code)
        data = json.loads(response.body)
        key_metrics = data.get("key_metrics", {})

        eps_ttm = float(key_metrics.get("EPS (TTM)", 0))
        most_recent_eps = float(key_metrics.get("EPS (Q4)", 0))
        current_price = float(key_metrics.get("Current Price", 0))

        if eps_ttm <= 0:
            value_as_per_earnings = -1
            return value_as_per_earnings, -1, current_price
        
        if most_recent_eps <= 0:
            value_as_per_earnings = 15 * eps_ttm
            return value_as_per_earnings, -1, current_price

        val_earnings_q4, value_as_per_earnings = 15 * 4 * most_recent_eps, 15 * eps_ttm
        return value_as_per_earnings, val_earnings_q4, current_price
    
    def get_valuation_by_earnings(self, symbol: str = Query(..., title="Symbol", description="Stock symbol")):
        try:
            value_as_per_earnings, value_earnings_q4, ltp = self.compute_earnings_valuation(symbol)
            bull_case_valuation = round(max(value_as_per_earnings, value_earnings_q4), 2) 
            base_case_valuation = round(min(value_as_per_earnings, value_earnings_q4), 2)

            if bull_case_valuation == -1:
                return JSONResponse(content={
                    "symbol": symbol,
                    "valuation_as_per_earnings": base_case_valuation,
                    "current_price": ltp
                })
            
            if base_case_valuation == -1:
                return JSONResponse(content={
                    "symbol": symbol,
                    "valuation_as_per_earnings": bull_case_valuation,
                    "current_price": ltp
                })
            
            return JSONResponse(content={
                    "symbol": symbol,
                    "bull_case_value": bull_case_valuation,
                    "base_case_value": base_case_valuation,
                    "current_price": ltp
                })
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error calculating valuation as per earnings: {e}")
    
    def get_valuation_verdict(self, symbol: str = Query(..., title="Symbol", description="Stock Symbol")):
        try:
            response = self.get_valuation_by_earnings(symbol)
            data = json.loads(response.body)
            earnings_valuation_bull = data.get("bull_case_value", 0)
            earnings_valuation_base = data.get("base_case_value", 0)
            valuation_as_per_earnings = round(data.get("valuation_as_per_earnings", 0), 2)
            current_price = data.get("current_price", 0)
            symbol = data.get("symbol", "")

            if valuation_as_per_earnings:
                ltp_premium = current_price * 1.2
                ltp_discount = current_price * 0.95
                if ltp_discount < valuation_as_per_earnings:
                    return JSONResponse(content={
                    "symbol": symbol,
                    "valuation_as_per_earnings": valuation_as_per_earnings,
                    "current_price": current_price,
                    "verdict": "undervalued"
                })
                if ltp_premium > valuation_as_per_earnings:
                    return JSONResponse(content={
                        "symbol": symbol,
                        "valuation_as_per_earnings": valuation_as_per_earnings,
                        "current_price": current_price,
                        "verdict": "overvalued"
                    })
                return JSONResponse(content={
                        "symbol": symbol,
                        "valuation_as_per_earnings": valuation_as_per_earnings,
                        "current_price": current_price,
                        "verdict": "fairly valued"
                    })

            if earnings_valuation_base and earnings_valuation_bull and current_price:
                if current_price < earnings_valuation_base:
                    return JSONResponse(content={
                        "symbol": symbol,
                        "bull_case_value": earnings_valuation_bull,
                        "base_case_value": earnings_valuation_base,
                        "current_price": current_price,
                        "verdict": "undervalued"
                    })
                if current_price > earnings_valuation_bull:
                    return JSONResponse(content={
                        "symbol": symbol,
                        "bull_case_value": earnings_valuation_bull,
                        "base_case_value": earnings_valuation_base,
                        "current_price": current_price,
                        "verdict": "overvalued"
                    })
                return JSONResponse(content={
                        "symbol": symbol,
                        "bull_case_value": earnings_valuation_bull,
                        "base_case_value": earnings_valuation_base,
                        "current_price": current_price,
                        "verdict": "fairly valued"
                    })
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving valuation verdict: {e}")