from google.cloud import pubsub_v1
import os
import time
from ast import literal_eval
from datetime import datetime
import math
import yfinance as yf

service_account = r"D:\file_path\file_name.json"

output_topic_name = "your/pubsub/topic_name"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account

publisher = pubsub_v1.PublisherClient()


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


cnt_mins_seconds = 670 # Only tracks data upto 11 minutes and 10 seconds, please replace with the desired number of seconds or use while(1)
# Important note: Using while(1) could send multiple GET requests, which can be concerning. To simulate and test the data 670 seconds is more than enough in most of the cases. 
intial = 1


while (intial<=cnt_mins_seconds):

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
 
            data = str(data_eval).encode("utf-8")
            publisher.publish(topic=output_topic_name, data=data)
            print(f"Published message: {data}")

        
    intial+=60
    print(intial)
    time.sleep(60)

    
