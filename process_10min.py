import os
import time
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from apache_beam.transforms.window import FixedWindows, TimestampedValue
from apache_beam.transforms.trigger import AfterProcessingTime, AfterWatermark, AfterCount, AccumulationMode
from ast import literal_eval


service_account = r"D:\file_path\file_name.json"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account

output_topic_name = "your/pubsub/topic_name"
input_subscriber_name = "your/pubsub/subscriber_name"


def strip_row(element):
    element = element.strip()
    element = literal_eval(element)
    temp_list = []
    for key in element:
        temp_list.append(element[key])
    return temp_list


def printing(element):
    print(element)
    return element

def extract_columns(element):
    open, high, low, close, volume, dividends, stock_splits, source, processed_timestamp = element
    if open is not None and high is not None and low is not None and close is not None and source is not None and processed_timestamp is not None:
        open = float(open)
        high = float(high)
        low = float(low)
        close = float(close)
        return [open, high, low, close, source, processed_timestamp]
    else:
        return None

def calculate_percentage_change(element):

    '''
    Sample data:
    ('ASIANPAINT.NS', 
    [
    [2330.1000976562, 2330.1000976562, 2330.1000976562, 2330.1000976562, 'ASIANPAINT.NS', 1748252425], 
    [2330.1000976562, 2330.1000976562, 2330.1000976562, 2330.1000976562, 'ASIANPAINT.NS', 1748252426]
    ]
    )
    [open, high, low, close, source, processed_timestamp]
    '''

    source = element[0]
    gain=False
    value_list = sorted(element[1], key=lambda x : x[5])
    first_open = value_list[0][0]
    last_closed = value_list[-1][3]
    percentage_change = ( (last_closed - first_open) * 100 ) / first_open
    
    if percentage_change > 0:
        gain = True
    
    max_high = []
    min_low = []
    for list in value_list:
        high = list[1]
        low = list[2]
        max_high.append(high)
        min_low.append(low)
    
    if max_high:
        all_time_high = max(max_high)
    else:
        all_time_high = None

    if min_low:
        all_time_low = min(min_low)
    else:
        min_low = None

    return [source, percentage_change, gain ,first_open, last_closed, all_time_high, all_time_low]

def add_event_timestamp(element):
    timestamp = element[5]  # assuming processed_timestamp is at index 5
    return beam.window.TimestampedValue(element, timestamp)


options = PipelineOptions(auto_unique_labels=True)
options.view_as(StandardOptions).streaming = True

# Sechema for the input row received: [open, high, low, close, volume, dividends, stock_splits, source, processed_timestamp]

pipeline = beam.Pipeline(options=options)

read_data = (
    pipeline
    | "Read data from file" >> beam.io.ReadFromPubSub(subscription=input_subscriber_name)
    | "Decode" >> beam.Map(lambda x : x.decode())
    | "Strip and apply literal evaluate" >> beam.Map(strip_row)
      # [1581.0999755859, 1581.0999755859, 1581.0999755859, 1581.0999755859, 0, 0.0, 0.0, 'INFY.NS', 1748252423]
    | "extract only required columns" >> beam.Map(extract_columns)
    | "Filter out None values" >> beam.Filter(lambda x : x is not None)
)

process_data = (
    read_data
    | "Filter out rows where open or high is 0" >> beam.Filter(lambda x : x[0] !=0 and x[1]!=0)
     # [1581.0999755859, 1581.0999755859, 1581.0999755859, 1581.0999755859, 'INFY.NS', 1748252423]
    | "Add timestamp" >> beam.Map(add_event_timestamp)  
    | beam.Map(lambda x : (x[-2], x))
    | "Apply window for 10 minutes" >> beam.WindowInto(FixedWindows(60 * 10), trigger= AfterWatermark(), accumulation_mode=AccumulationMode.DISCARDING, allowed_lateness=0)
    | beam.GroupByKey()
    # | "print" >> beam.Map(printing) # for debug
    | "Caluclate the percentage change over the past 10 minutes" >> beam.Map(calculate_percentage_change)
    | "print" >> beam.Map(printing)
)

res = pipeline.run()
res.wait_until_finish()
