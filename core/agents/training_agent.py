from typing import Optional
import random
import time

class TrainingAgent:
    def __init__(self, agent_id: str, description: str):
        """
        Initializes a training agent with an ID and description.
        :param agent_id: Unique identifier for the agent.
        :param description: Description of the agent.
        """
        self.agent_id = agent_id
        self.description = description
        self.status = "initialized"
        self.model = None  # Placeholder for the model to be used by the agent

    def train(self, data: Optional[list] = None):
        """
        Simulates training of a model with the provided dataset.
        :param data: Optional dataset to be used in training.
        """
        self.status = "training"
        print(f"Agent {self.agent_id} is training on data...")
        # Simulate training time
        training_time = random.uniform(1.0, 5.0)
        time.sleep(training_time)
        # For actual model training, implement model fitting logic here.
        print(f"Training complete for Agent {self.agent_id} in {training_time:.2f} seconds.")
        self.status = "idle"

    def evaluate(self, data: Optional[list] = None):
        """
        Simulates evaluation of the trained model.
        """
        self.status = "evaluating"
        accuracy = random.uniform(0.5, 0.99)  # Simulate model accuracy after evaluation
        print(f"Agent {self.agent_id} evaluated the model with accuracy: {accuracy:.2f}")
        self.status = "idle"
        return accuracy

    def get_status(self) -> str:
        """
        Returns the current status of the agent.
        :return: Current status of the agent.
        """
        return self.status

# Example usage
if __name__ == "__main__":
    agent = TrainingAgent(agent_id="agent_1", description="Training agent for MNIST model")
    agent.train()
    agent.evaluate()
    print(f"Agent Status: {agent.get_status()}")
