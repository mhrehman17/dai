import random
import time
import platform
from core.agents.training_agent import TrainingAgent

class ARMTrainingAgent(TrainingAgent):
    def __init__(self, agent_id: str, description: str):
        """
        Initializes an ARM-based agent optimized for resource-constrained edge devices.
        :param agent_id: Unique identifier for the agent.
        :param description: Description of the agent.
        """
        super().__init__(agent_id, description)
        self.platform_type = platform.machine()
        if not self.is_arm_device():
            raise EnvironmentError(f"Agent {self.agent_id} must be run on an ARM-based device.")

    def is_arm_device(self) -> bool:
        """
        Checks if the agent is running on an ARM-based device.
        :return: True if the device is ARM-based, False otherwise.
        """
        return "arm" in self.platform_type.lower() or "aarch" in self.platform_type.lower()

    def optimize_training_for_arm(self):
        """
        Applies optimizations specific to ARM devices to enhance training efficiency.
        """
        print(f"Agent {self.agent_id} is applying ARM-specific optimizations for training.")
        # Placeholder: Implement optimizations like reduced precision, smaller batch size, etc.
        time.sleep(1.0)  # Simulate optimization adjustments

    def train(self, data: list = None):
        """
        Overrides the train method to include optimizations for ARM devices.
        :param data: Optional dataset to be used in training.
        """
        if not self.is_arm_device():
            raise EnvironmentError(f"Agent {self.agent_id} is not running on an ARM-based device.")

        self.status = "training"
        print(f"Agent {self.agent_id} is starting training on an ARM-based device...")
        self.optimize_training_for_arm()
        training_time = random.uniform(2.0, 6.0)  # Simulated longer training time due to lower resources
        time.sleep(training_time)
        print(f"Training complete for Agent {self.agent_id} on ARM-based device in {training_time:.2f} seconds.")
        self.status = "idle"

# Example usage
if __name__ == "__main__":
    try:
        arm_agent = ARMTrainingAgent(agent_id="arm_agent_1", description="ARM training agent for edge deployment")
        arm_agent.train()
        arm_agent.evaluate()
        print(f"Agent Status: {arm_agent.get_status()}")
    except EnvironmentError as e:
        print(str(e))
