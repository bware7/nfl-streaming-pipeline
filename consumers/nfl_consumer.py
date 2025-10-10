import sys
from pathlib import Path
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.utils_kafka import create_kafka_consumer
from utils.utils_logger import setup_logger

# Configuration
TOPIC = 'nfl_events'
WINDOW_SIZE = 10  # Track last 10 plays for momentum

class NFLGameTracker:
    """Tracks NFL game statistics and momentum."""
    
    def __init__(self):
        self.logger = setup_logger('nfl_consumer')
        self.plays = []
        self.recent_plays = deque(maxlen=WINDOW_SIZE)
        self.home_scores = []
        self.away_scores = []
        self.play_numbers = []
        self.momentum = {'home': 0, 'away': 0}
        
    def process_message(self, message):
        """Process incoming play message."""
        play_num = len(self.plays) + 1
        
        # Store data
        self.plays.append(message)
        self.recent_plays.append(message)
        self.play_numbers.append(play_num)
        self.home_scores.append(message['home_score'])
        self.away_scores.append(message['away_score'])
        
        # Calculate momentum (points in last 10 plays)
        self.momentum['home'] = sum(
            p['points_scored'] for p in self.recent_plays 
            if p['team'] == 'BUF' and p['points_scored'] > 0
        )
        self.momentum['away'] = sum(
            p['points_scored'] for p in self.recent_plays 
            if p['team'] == 'BAL' and p['points_scored'] > 0
        )
        
        # Log
        self.logger.info(
            f"Play {play_num}: Q{message['quarter']} {message['time_remaining']} - "
            f"{message['team']} {message['play_type']} | "
            f"Score: KC {message['home_score']}-{message['away_score']} BAL | "
            f"Momentum: KC {self.momentum['home']}-{self.momentum['away']} BAL"
        )

def setup_visualization():
    """Setup matplotlib figure with subplots."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    fig.suptitle('NFL Game Tracker - BUF vs BAL (Week 1, 2025)', fontsize=16, fontweight='bold')
    
    # Score progression chart
    ax1.set_xlabel('Play Number')
    ax1.set_ylabel('Score')
    ax1.set_title('Score Progression')
    ax1.grid(True, alpha=0.3)
    ax1.legend(['KC (Home)', 'BAL (Away)'])
    
    # Momentum chart
    ax2.set_xlabel('Team')
    ax2.set_ylabel('Points (Last 10 Plays)')
    ax2.set_title('Recent Momentum')
    ax2.set_ylim(0, 21)
    
    return fig, ax1, ax2

def update_chart(frame, tracker, consumer, ax1, ax2, line1, line2):
    """Update charts with new data."""
    try:
        # Get new messages (non-blocking with timeout)
        messages = consumer.poll(timeout_ms=100)
        
        for topic_partition, records in messages.items():
            for record in records:
                tracker.process_message(record.value)
        
        # Update score line chart
        if tracker.play_numbers:
            line1.set_data(tracker.play_numbers, tracker.home_scores)
            line2.set_data(tracker.play_numbers, tracker.away_scores)
            ax1.relim()
            ax1.autoscale_view()
        
        # Update momentum bar chart
        ax2.clear()
        teams = ['BUF', 'BAL']
        momentum_values = [tracker.momentum['home'], tracker.momentum['away']]
        colors = ['#00338D', '#241773']  
        
        bars = ax2.bar(teams, momentum_values, color=colors, alpha=0.7)
        ax2.set_ylabel('Points (Last 10 Plays)')
        ax2.set_title('Recent Momentum')
        ax2.set_ylim(0, 21)
        
        # Add value labels on bars
        for bar, value in zip(bars, momentum_values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(value)}', ha='center', va='bottom', fontweight='bold')
        
    except Exception as e:
        tracker.logger.error(f"Error updating chart: {e}")
    
    return line1, line2

def main():
    """Main consumer with visualization."""
    tracker = NFLGameTracker()
    
    # Connect to Kafka
    try:
        consumer = create_kafka_consumer(TOPIC)
        tracker.logger.info(f"Consumer connected to topic: {TOPIC}")
    except Exception as e:
        tracker.logger.error(f"Failed to connect to Kafka: {e}")
        return
    
    # Setup visualization
    fig, ax1, ax2 = setup_visualization()
    line1, = ax1.plot([], [], 'o-', color='#00338D', linewidth=2, markersize=6, label='BUF (Home)')
    line2, = ax1.plot([], [], 'o-', color='#241773', linewidth=2, markersize=6, label='BAL (Away)')
    ax1.legend()
    
    # Start animation
    ani = animation.FuncAnimation(
        fig, update_chart, 
        fargs=(tracker, consumer, ax1, ax2, line1, line2),
        interval=500, blit=False, cache_frame_data=False
    )
    
    plt.tight_layout()
    tracker.logger.info("Visualization started. Close window to exit.")
    plt.show()
    
    consumer.close()
    tracker.logger.info("Consumer closed.")

if __name__ == "__main__":
    main()