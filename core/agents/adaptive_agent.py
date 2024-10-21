from typing import Optional
import random
import time
import psutil
from core.agents.training_agent import TrainingAgent

class AdaptiveAgent(TrainingAgent):
    def __init__(self, agent_id: str, description: str, adaptation_threshold: float = 70.0):
        """
        Initializes an adaptive training agent capable of adjusting its behavior based on system resource usage.
        :param agent_id: Unique identifier for the agent.
        :param description: Description of the agent.
        :param adaptation_threshold: CPU usage percentage at which the agent will adapt its behavior.
        """
        super().__init__(agent_id, description)
        self.adaptation_threshold = adaptation_threshold

    def monitor_resources(self) -> float:
        """
        Monitors the system's current CPU usage.
        :return: Current CPU usage as a percentage.
        """
        cpu_usage = psutil.cpu_percent(interval=1.0)
        print(f"Agent {self.agent_id} detected CPU usage: {cpu_usage:.2f}%")
        return cpu_usage

    def adapt_training(self):
        """
        Adapts the training process based on system resources. Reduces the workload if the CPU usage is above the threshold.
        """
        cpu_usage = self.monitor_resources()
        if cpu_usage > self.adaptation_threshold:
            print(f"Agent {self.agent_id} adapting to high CPU usage ({cpu_usage:.2f}%) by reducing training intensity.")
            # Placeholder: Actual adaptation could involve adjusting batch size or other hyperparameters.
            time.sleep(2)  # Simulate reduced workload
        else:
            print(f"Agent {self.agent_id} proceeding with normal training.")

    def train(self, data: Optional[list] = None):
        """
        Overrides the base train method to include adaptive behavior based on system resource monitoring.
        :param data: Optional dataset to be used in training.
        """
        self.status = "training"
        print(f"Agent {self.agent_id} is starting adaptive training...")
        self.adapt_training()
        # Continue with normal training behavior
        training_time = random.uniform(1.0, 5.0)
        time.sleep(training_time)
        print(f"Adaptive training complete for Agent {self.agent_id} in {training_time:.2f} seconds.")
        self.status = "idle"

# Example usage
if __name__ == "__main__":
    adaptive_agent = AdaptiveAgent(agent_id="adaptive_agent_1", description="Adaptive training agent for resource-limited environments")
    adaptive_agent.train()
    adaptive_agent.evaluate()
    print(f"Agent Status: {adaptive_agent.get_status()}")
