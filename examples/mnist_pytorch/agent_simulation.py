import random
import time
import logging
import requests
from threading import Thread

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AgentSimulation")

# Constants for the metrics API endpoint
METRICS_API_URL = "http://localhost:8000/metric"
AGENT_IDS = ["agent_1", "agent_2", "agent_3", "agent_4"]
SIMULATION_INTERVAL = 5  # Interval in seconds for metric updates

# Function to simulate metrics and send them to the API
def simulate_agent_metrics(agent_id):
    while True:
        # Simulate random metrics for the agent
        metrics = {
            "cpu_usage": round(random.uniform(10.0, 90.0), 2),
            "memory_usage": round(random.uniform(10.0, 80.0), 2),
            "training_loss": round(random.uniform(0.05, 0.5), 4)
        }
        
        # Send metrics to the API
        try:
            response = requests.put(f"{METRICS_API_URL}/{agent_id}", json=metrics)
            response.raise_for_status()
            logger.info(f"Metrics for {agent_id} updated successfully: {metrics}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update metrics for {agent_id}: {e}")
        
        # Wait before the next update
        time.sleep(SIMULATION_INTERVAL)

# Main function to run multiple agent simulations
def run_simulation():
    logger.info("Starting agent simulations...")
    threads = []
    for agent_id in AGENT_IDS:
        thread = Thread(target=simulate_agent_metrics, args=(agent_id,))
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Simulation stopped by user.")

if __name__ == "__main__":
    run_simulation()
