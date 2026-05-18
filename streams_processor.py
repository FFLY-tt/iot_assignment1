# streams_processor.py
import faust
import joblib
import certifi
from aiokafka.helpers import create_ssl_context
import config

print("Loading pre-trained ML model...")
model = joblib.load('bike_model.joblib')

broker_credentials = faust.SASLCredentials(
    mechanism=faust.types.auth.SASLMechanism.PLAIN,
    ssl_context=create_ssl_context(cafile=certifi.where()),
    username=config.API_KEY,
    password=config.API_SECRET
)

# 3. Initialize Faust Application
app = faust.App(
    'bike-sharing-stream-processor',
    broker=f'kafka://{config.BOOTSTRAP_SERVER}',
    broker_credentials=broker_credentials,
    topic_replication_factor=3,  
)

class BikeRecord(faust.Record, serializer='json'):
    season: int
    yr: int
    mnth: int
    hr: int
    holiday: int
    weekday: int
    workingday: int
    weathersit: int
    temp: float
    atemp: float
    hum: float
    windspeed: float

raw_topic = app.topic(config.RAW_TOPIC, value_type=BikeRecord)
predictions_topic = app.topic(config.PREDICTIONS_TOPIC, value_serializer='json')

@app.agent(raw_topic)
async def process_stream(records):
    async for record in records:
        features = [
            record.season, record.yr, record.mnth, record.hr,
            record.holiday, record.weekday, record.workingday,
            record.weathersit, record.temp, record.atemp,
            record.hum, record.windspeed
        ]
        
        prediction_code = int(model.predict([features])[0])
        demand_status = "High Demand (>150 bikes)" if prediction_code == 1 else "Low Demand (<=150 bikes)"
        
        output_payload = {
            "target_hour": record.hr,
            "weather_situation": record.weathersit,
            "temperature_normalized": record.temp,
            "predicted_demand_class": demand_status
        }
        
        print(f"Processed event for hour {record.hr}: Inference -> {demand_status}")
        await predictions_topic.send(value=output_payload)

if __name__ == '__main__':
    app.main()