import csv
import json
import os
import time
from google.cloud import pubsub_v1

# 1. AUTHENTICATION
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Auth.json"

# 2. CONFIGURATION
project_id = "sofe4630u-ms1"  # <--- MAKE SURE THIS IS YOUR ACTUAL ID
topic_id = "designTopic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# FIXED LINE 17: Added quotes around the text
print(f"Reading from Labels.csv and publishing to {topic_id}...")

# FIXED LINE 20: Added the colon ':' after try
try:
    with open('Labels.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            # Serialize
            message_json = json.dumps(row)
            message_bytes = message_json.encode('utf-8')
            
            # Publish
            print(f"Publishing: {row}")
            publish_future = publisher.publish(topic_path, message_bytes)
            publish_future.result() 
            
            time.sleep(1) 
            
    print("All records published.")
    
except FileNotFoundError:
    print("Error: Labels.csv not found. Make sure it is in this folder.")