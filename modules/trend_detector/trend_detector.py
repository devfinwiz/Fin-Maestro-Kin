from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib
import io
import datetime as dt
import warnings

warnings.filterwarnings("ignore")
initial, end = dt.date.today() - dt.timedelta(days=374), dt.date.today()

router = APIRouter()


#Example usage - http://127.0.0.1:8000/generate_plot?ticker=BSE.NS
def signals_generator(ticker, num_of_signals):
    matplotlib.use('Agg')
    yf.pdr_override()
    plt.style.use('dark_background')  # dark theme for plot

    df = yf.download(ticker, initial, end)  # dataframe from yfinance for a specific ticker

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


@router.get("/generate_plot")
async def generate_plot(ticker: str = Query(..., title="Ticker", description="Stock ticker symbol"),
                        num_of_signals: int = Query(10, title="Num of Signals", description="Number of buy/sell signals to be plotted")):
    fig = signals_generator(ticker, num_of_signals)

    # Convert the matplotlib figure to a PNG image
    image_stream = io.BytesIO()
    fig.savefig(image_stream, format="png")
    image_stream.seek(0)

    return StreamingResponse(content=image_stream, media_type="image/png")
