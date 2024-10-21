import numpy as np
from typing import List, Dict

class SecureAggregation:
    def __init__(self):
        """
        Initializes the Secure Aggregation mechanism to securely aggregate model updates.
        """
        self.model_updates: Dict[str, List[np.ndarray]] = {}

    def add_update(self, agent_id: str, model_update: np.ndarray):
        """
        Adds an update from an agent for aggregation.
        :param agent_id: Unique identifier of the agent submitting the model update.
        :param model_update: The model update as a numpy array.
        """
        if agent_id not in self.model_updates:
            self.model_updates[agent_id] = []
        self.model_updates[agent_id].append(model_update)
        print(f"Added model update from agent {agent_id}.")

    def aggregate_updates(self) -> np.ndarray:
        """
        Aggregates the model updates from all agents securely.
        :return: The aggregated model update as a numpy array.
        """
        if not self.model_updates:
            raise ValueError("No model updates available for aggregation.")

        # Collect all model updates
        all_updates = []
        for agent_id, updates in self.model_updates.items():
            all_updates.extend(updates)

        # Aggregate by averaging
        aggregated_update = np.mean(all_updates, axis=0)
        print(f"Aggregated {len(all_updates)} model updates.")

        # Clear updates after aggregation
        self.model_updates.clear()
        return aggregated_update

    def secure_masking(self, model_update: np.ndarray, mask_value: float = 0.1) -> np.ndarray:
        """
        Applies secure masking to the model update to ensure privacy.
        :param model_update: The original model update.
        :param mask_value: The value to add for masking.
        :return: Masked model update.
        """
        mask = np.random.normal(0, mask_value, model_update.shape)
        masked_update = model_update + mask
        print(f"Applied secure masking to the model update.")
        return masked_update

    def unmask_update(self, masked_update: np.ndarray, mask_value: float = 0.1) -> np.ndarray:
        """
        Removes the secure masking from a model update.
        :param masked_update: The masked model update.
        :param mask_value: The value used to generate the masking.
        :return: The unmasked model update.
        """
        mask = np.random.normal(0, mask_value, masked_update.shape)
        unmasked_update = masked_update - mask
        print(f"Removed secure masking from the model update.")
        return unmasked_update

# Example usage
if __name__ == "__main__":
    secure_agg = SecureAggregation()
    
    # Simulating updates from agents
    update_1 = np.array([1.0, 2.0, 3.0])
    update_2 = np.array([1.5, 2.5, 3.5])
    update_3 = np.array([0.5, 1.5, 2.5])

    secure_agg.add_update("agent_1", update_1)
    secure_agg.add_update("agent_2", update_2)
    secure_agg.add_update("agent_3", update_3)

    # Aggregate updates
    aggregated_update = secure_agg.aggregate_updates()
    print(f"Aggregated Update: {aggregated_update}")

    # Secure masking and unmasking example
    masked_update = secure_agg.secure_masking(update_1)
    unmasked_update = secure_agg.unmask_update(masked_update)
    print(f"Original Update: {update_1}")
    print(f"Masked Update: {masked_update}")
    print(f"Unmasked Update: {unmasked_update}")
