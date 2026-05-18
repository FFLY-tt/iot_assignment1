Add-Content README.md @"

## How to Run

Open **three terminals** side by side and run in this order:

**Terminal 1 — Start Streams Processor (Faust Worker):**
``````bash
conda activate bike_streaming
faust -A streams_processor worker -l info
``````

**Terminal 2 — Start Output Consumer:**
``````bash
conda activate bike_streaming
python output_consumer.py
``````

**Terminal 3 — Start Producer:**
``````bash
conda activate bike_streaming
python producer.py
``````

Wait for the Faust worker to initialize before starting the consumer and producer.

## Video Demo

[Watch the live demo here](https://drive.google.com/file/d/1CKz-_NV3X0sCu-xEz84UwjbiYedMUWr5/view?usp=sharing)

> Demo shows all three terminals running simultaneously with real-time predictions printing live.
"@