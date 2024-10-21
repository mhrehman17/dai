import logging
from threading import Thread
from core.agents.training_agent import TrainingAgent
from core.orchestrator.decentralized_orchestrator import DecentralizedOrchestrator
from core.data.mnist_data_loader import MNISTDataLoader
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DecentralizedMNISTPipeline")

# Constants
AGENT_IDS = ["agent_1", "agent_2", "agent_3", "agent_4"]
EPOCHS = 5
BATCH_SIZE = 32

# Function to simulate decentralized agent training
def agent_training(agent_id, train_loader, test_loader, orchestrator):
    agent = TrainingAgent(agent_id, orchestrator)
    logger.info(f"Starting training for agent: {agent_id}")
    for epoch in range(EPOCHS):
        agent.train(train_loader)
        accuracy = agent.evaluate(test_loader)
        logger.info(f"Agent: {agent_id}, Epoch: {epoch + 1}, Accuracy: {accuracy:.2f}%")
    orchestrator.report_training_completion(agent_id)

# Main function to run the decentralized MNIST training pipeline
def run_decentralized_mnist_pipeline():
    logger.info("Loading MNIST data...")
    train_loader, test_loader = MNISTDataLoader(batch_size=BATCH_SIZE)
    logger.info("MNIST data loaded successfully.")

    orchestrator = DecentralizedOrchestrator()
    threads = []

    # Start training for each agent in a separate thread
    for agent_id in AGENT_IDS:
        thread = Thread(target=agent_training, args=(agent_id, train_loader, test_loader, orchestrator))
        thread.daemon = True
        thread.start()
        threads.append(thread)

    # Keep the main thread alive until all agents have completed training
    try:
        while any(thread.is_alive() for thread in threads):
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Decentralized MNIST training pipeline interrupted by user.")

    logger.info("Decentralized MNIST training pipeline completed successfully.")

if __name__ == "__main__":
    run_decentralized_mnist_pipeline()