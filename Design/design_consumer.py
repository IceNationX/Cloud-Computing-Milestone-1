import json
import os
from google.cloud import pubsub_v1

# 1. AUTHENTICATION
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Auth.json"

# 2. CONFIGURATION
project_id = "sofe4630u-ms1"   # <--- PASTE YOUR PROJECT ID HERE
subscription_id = "designTopic-sub"  # Make sure this matches your Cloud Console!

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message):
    # Deserialize: Bytes -> String -> Dictionary
    message_data = message.data.decode('utf-8')
    record_dict = json.loads(message_data)
    
    print(f"Received Dictionary: {record_dict}")
    message.ack()

print(f"Listening for CSV records on {subscription_id}...\n")
with subscriber:
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()