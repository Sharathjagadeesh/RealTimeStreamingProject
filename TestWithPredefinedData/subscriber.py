from google.cloud import pubsub_v1
import os
import time

service_account = r"D:\file_path\file_name.json"

input_subscriber_name = "your/pubsub/subscriber_name"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account

def callback(message):
    data = message.data.decode("utf-8")
    print(data)
    message.ack()

subscriber = pubsub_v1.SubscriberClient()
subscriber = subscriber.subscribe(input_subscriber_name, callback=callback)

while (1):
    time.sleep(60)