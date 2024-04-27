from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib
import io
import datetime as dt
import warnings

warnings.filterwarnings("ignore")


class TrendDetector:
    def __init__(self):
        self.router = APIRouter(tags=["Trend Detector"])
        matplotlib.use('Agg')
        plt.style.use('dark_background')

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

    async def generate_plot(self, ticker: str = Query(..., title="Ticker", description="Stock ticker symbol"),
                            num_of_signals: int = Query(10, title="Num of Signals",
                                                        description="Number of buy/sell signals to be plotted")):
        fig = self.signals_generator(ticker, num_of_signals)

        image_stream = io.BytesIO()
        fig.savefig(image_stream, format="png")
        image_stream.seek(0)

        return StreamingResponse(content=image_stream, media_type="image/png")
