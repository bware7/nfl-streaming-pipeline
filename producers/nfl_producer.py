import csv
import time
import json
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.utils_kafka import create_kafka_producer
from utils.utils_logger import setup_logger

# Configuration
TOPIC = 'nfl_events'
DATA_FILE = Path('data/ravens_bills_week1.csv')  # Changed from sample_game.csv
DELAY_SECONDS = 1.5  # Time between plays

def main():
    """Stream NFL play-by-play data to Kafka."""
    logger = setup_logger('nfl_producer')
    
    # Create producer
    try:
        producer = create_kafka_producer()
        logger.info(f"Producer connected. Streaming to topic: {TOPIC}")
    except Exception as e:
        logger.error(f"Failed to connect to Kafka: {e}")
        return
    
    # Check if data file exists
    if not DATA_FILE.exists():
        logger.error(f"Data file not found: {DATA_FILE}")
        return
    
    # Stream data
    play_count = 0
    try:
        with open(DATA_FILE, 'r') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Build message
                message = {
                    'timestamp': row['timestamp'],
                    'game_id': row['game_id'],
                    'quarter': int(row['quarter']),
                    'time_remaining': row['time_remaining'],
                    'team': row['team'],
                    'play_type': row['play_type'],
                    'points_scored': int(row['points_scored']),
                    'player_name': row['player_name'],
                    'home_score': int(row['home_score']),
                    'away_score': int(row['away_score'])
                }
                
                # Send to Kafka
                producer.send(TOPIC, value=message)
                play_count += 1
                
                logger.info(f"Play {play_count}: {message['team']} - {message['play_type']} | Score: {message['home_score']}-{message['away_score']}")
                
                # Delay to simulate real-time
                time.sleep(DELAY_SECONDS)
        
        producer.flush()
        logger.info(f"Streaming complete. Sent {play_count} plays.")
        
    except Exception as e:
        logger.error(f"Error during streaming: {e}")
    finally:
        producer.close()
        logger.info("Producer closed.")

if __name__ == "__main__":
    main()