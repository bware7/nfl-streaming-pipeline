# NFL Streaming Pipeline

Real-time NFL game tracking system that streams play-by-play data through Kafka and processes scoring events.

## Project Overview
This project demonstrates streaming data analytics by simulating NFL game data flowing through a Kafka pipeline. A producer reads historical play-by-play data and streams it in real-time, while a consumer processes the events and tracks game progress.

## Current Status
- ✅ Basic producer streaming CSV data to Kafka
- ✅ Basic consumer reading and displaying events
- 🔄 Visualization with matplotlib (in progress)
- 🔄 Advanced analytics and momentum tracking (planned)

## Project Structure
```
nfl-streaming-pipeline/
├── producers/
│   └── nfl_producer.py          # Streams play-by-play data to Kafka
├── consumers/
│   └── nfl_consumer.py          # Processes events from Kafka
├── utils/
│   └── (utility modules TBD)
├── data/
│   └── sample_game.csv          # Sample NFL play data
├── scripts/
│   └── prepare_kafka.sh         # Kafka setup script
└── requirements.txt
```

## Setup Instructions

### 1. Clone and Setup Environment
```bash
git clone https://github.com/bware7/nfl-streaming-pipeline.git
cd nfl-streaming-pipeline
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Start Kafka (Windows WSL)
```bash
wsl
cd /mnt/c/Users/binya/NorthWest/STREAMING_DATA/nfl-streaming-pipeline
./scripts/prepare_kafka.sh
cd ~/kafka
bin/kafka-server-start.sh config/kraft/server.properties
```
Keep this terminal open - Kafka must stay running.

### 3. Run the Pipeline
Open two new PowerShell terminals with (.venv) activated:

**Terminal 1 - Start Consumer:**
```powershell
python consumers/nfl_consumer.py
```

**Terminal 2 - Start Producer:**
```powershell
python producers/nfl_producer.py
```

## Kafka Configuration
- **Topic:** `nfl_events`
- **Bootstrap Server:** `localhost:9092`
- **Message Format:** JSON

## Sample Message
```json
{
  "timestamp": "2024-09-15 13:05:23",
  "team": "BAL",
  "play_type": "touchdown",
  "points_scored": 7,
  "home_score": 0,
  "away_score": 7
}
```

## Next Steps
- Add matplotlib animation for live score visualization
- Implement momentum tracking analytics
- Add data structure for rolling statistics
- Optional: Email/SMS alerts for scoring events