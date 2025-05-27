import yfinance as yf
import time
from ast import literal_eval
from datetime import datetime, date
import pendulum
import math

nse_top_15_tickers = [
    "RELIANCE.NS",
    "TCS.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "HINDUNILVR.NS",
    "INFY.NS",
    "SBIN.NS",
    "BHARTIARTL.NS",
    "SUNPHARMA.NS",
    "ITC.NS",
    "BAJFINANCE.NS",
    "KOTAKBANK.NS",
    "LT.NS",
    "AXISBANK.NS",
    "ASIANPAINT.NS"
]


output_file_path = r"D:\file_path\file_name.txt"

cnt_eleven_mins_seconds = 660
intial = 1

with open(output_file_path, "w") as file_write:

    while (intial<=cnt_eleven_mins_seconds):

        for ticker_name in nse_top_15_tickers:

            ticker = yf.Ticker(ticker_name)
            data = ticker.history(period="1d", interval="1m")  # 1 day, 1 min interval
            latest_row = data.tail(1)

            if not latest_row.empty:
                json_data = latest_row.to_json(orient="records", date_format="iso")
                data_eval = literal_eval(json_data)
                data_eval = data_eval[0]
                data_eval['source'] = ticker_name
                data_eval['processed_timestamp'] = math.floor(datetime.now().timestamp())
                print(data_eval)
                file_write.write(str(data_eval)+"\n")
                print(intial)
        
        time.sleep(60)
        intial+=60
