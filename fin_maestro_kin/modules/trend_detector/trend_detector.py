from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib
import io
import datetime as dt
import warnings
import redis

warnings.filterwarnings("ignore")


class Helper():
    
    @staticmethod
    def calculate_cache_expiration():
        next_update_time = dt.datetime.combine(dt.date.today(), dt.time(hour=17, minute=0))  

        current_time = dt.datetime.now()
        time_until_update = (next_update_time - current_time).total_seconds()

        expiration_time = max(1, time_until_update) 
        return expiration_time


class TrendDetector(Helper):
    def __init__(self):
        self.router = APIRouter(tags=["Trend Detector"])
        matplotlib.use('Agg')
        plt.style.use('dark_background')
        
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def register_routes(self, app):
        self.router.add_api_route("/generate_plot", self.generate_plot, methods=["GET"])
        app.include_router(self.router)

    @staticmethod
    def signals_generator(ticker, num_of_signals):
        yf.pdr_override()
        initial, end = dt.date.today() - dt.timedelta(days=374), dt.date.today()
        df = yf.download(ticker, initial, end) 
        closes = sorted(df.Close.tolist())
        low, high = closes[num_of_signals], closes[-num_of_signals]

        df['Signal'] = 0

        df.loc[df['Adj Close'] > high, 'Signal'] = -1
        df.loc[df['Adj Close'] < low, 'Signal'] = 1

        long = df.loc[df['Signal'] == 1]
        short = df.loc[df['Signal'] == -1]

        fig = plt.figure()
        fig.set_figwidth(12)
        plt.plot(df.index, df['Adj Close'], color='white', label='Close Price')
        plt.plot(long.index, df.loc[long.index]['Adj Close'], '^', markersize=10, color='g', label='Long/Buy')
        plt.plot(short.index, df.loc[short.index]['Adj Close'], 'v', markersize=10, color='r', label='Short/Sell')
        plt.ylabel('Closing Price')
        plt.xlabel('Date')
        plt.title(ticker)
        plt.legend(loc='best')

        return fig

    async def generate_plot(
        self, 
        ticker: str = Query(..., title="Ticker", description="Stock ticker symbol"),
        num_of_signals: int = Query(10, title="Num of Signals", description="Number of buy/sell signals to be plotted")
        ):
        
        cached_image = self.redis_client.get(f"plot_{ticker}")

        if cached_image:
            try:
                cached_image_decoded = io.BytesIO(cached_image)
                return StreamingResponse(content=cached_image_decoded, media_type="image/png")
            except Exception as e:
                print(f"Error decoding cached image: {e}")

        fig = self.signals_generator(ticker, num_of_signals)

        image_stream = io.BytesIO()
        fig.savefig(image_stream, format="png")
        image_stream.seek(0) 

        self.redis_client.set(f"plot_{ticker}", image_stream.getvalue(), int(Helper.calculate_cache_expiration()))
        image_stream.seek(0) 
        
        return StreamingResponse(content=image_stream, media_type="image/png")
