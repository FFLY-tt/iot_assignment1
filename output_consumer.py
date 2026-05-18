# output_consumer.py
from confluent_kafka import Consumer, KafkaError
import json
import config

def main():
    consumer_config = {
        'bootstrap.servers': config.BOOTSTRAP_SERVER,
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': config.API_KEY,
        'sasl.password': config.API_SECRET,
        'group.id': 'bike-predictions-console-logger',
        'auto.offset.reset': 'latest'
    }

    consumer = Consumer(consumer_config)
    consumer.subscribe([config.PREDICTIONS_TOPIC])

    print("Successfully connected. Listening for live ML predictions... Press Ctrl+C to stop.")
    
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Consumer Error: {msg.error()}")
                    break
            
            payload = json.loads(msg.value().decode('utf-8'))
            
            print("\n" + "="*50)
            print("🚨 LIVE ML INFERENCE RECEIVED 🚨")
            print(f"Hour of Day     : {payload.get('target_hour')}:00")
            print(f"Weather Class   : {payload.get('weather_situation')}")
            print(f"Temp (Norm)     : {payload.get('temperature_normalized')}")
            print(f"👉 ML PREDICTION: {payload.get('predicted_demand_class')}")
            print("="*50)

    except KeyboardInterrupt:
        print("\nStopping consumer gracefully...")
    finally:
        consumer.close()

if __name__ == '__main__':
    main()