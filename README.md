# Real-Time Streaming and Live Machine Learning Pipeline with Apache Kafka

## Project Overview
This application builds a real-time event streaming pipeline using Apache Kafka on Confluent Cloud. The system streams hourly records from the UCI Bike Sharing dataset, processes events on-the-fly using the Faust stream processing library, evaluates a pre-trained Machine Learning model, and publishes predicted demand states to an output topic for downstream visualization.

### Dataset Chosen
* **Dataset**: Bike Sharing Dataset (UCI)
* **Task Type**: Binary Classification (Predicting whether hourly rental demand is "High Demand" (>150 rentals) or "Low Demand" (<=150 rentals)) to compute and satisfy grading metrics.

## Machine Learning Model Performance
* **Model Type**: RandomForestClassifier
* **Model Accuracy**: 0.9258
* **Model F1-Score**: 0.9218

## Technology Stack & Libraries Used
* **Kafka Cluster**: Confluent Cloud (SaaS)
* **Stream Library**: Faust (Python equivalent of Kafka Streams)
* **Machine Learning**: Scikit-Learn, Joblib, Pandas
* **Kafka Client**: Confluent-Kafka Python Client

## Setup and Installation Instructions

1. Install dependencies listed in requirements file:
```bash
   pip install -r requirements.txt
```

2. Copy `config.example.py` to `config.py` and fill in your Confluent Cloud credentials:
```python
   BOOTSTRAP_SERVER = "your-confluent-bootstrap-server"
   API_KEY = "your-api-key"
   API_SECRET = "your-api-secret"
```

## How to Run

Open **three terminals** side by side and run in this order:

**Terminal 1 — Start Streams Processor (Faust Worker):**
```bash
conda activate bike_streaming
faust -A streams_processor worker -l info
```

**Terminal 2 — Start Output Consumer:**
```bash
conda activate bike_streaming
python output_consumer.py
```

**Terminal 3 — Start Producer:**
```bash
conda activate bike_streaming
python producer.py
```

Wait for the Faust worker to initialize before starting the consumer and producer.

## Video Demo

[Watch the live demo here](https://drive.google.com/file/d/1CKz-_NV3X0sCu-xEz84UwjbiYedMUWr5/view?usp=sharing)

> Demo shows all three terminals running simultaneously with real-time predictions printing live.