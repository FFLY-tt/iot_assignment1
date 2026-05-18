# producer.py
import time
import json
import pandas as pd
from confluent_kafka import Producer
import config

def delivery_report(err, msg):
    """ Called once for each message success or failure. """
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def main():
    producer_config = {
        'bootstrap.servers': config.BOOTSTRAP_SERVER,
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': config.API_KEY,
        'sasl.password': config.API_SECRET
    }
    
    producer = Producer(producer_config)
    
    print("Reading dataset for streaming...")
    df = pd.read_csv('hour.csv')
    
    features = ['season', 'yr', 'mnth', 'hr', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed']
    df_features = df[features]

    print("Starting data streaming pipeline to Kafka. Press Ctrl+C to stop.")
    for index, row in df_features.iterrows():
        message_data = row.to_dict()
        message_json = json.dumps(message_data)
        
        producer.produce(
            topic=config.RAW_TOPIC, 
            value=message_json, 
            callback=delivery_report
        )
        producer.poll(0)
        time.sleep(1.0)

if __name__ == '__main__':
    main()