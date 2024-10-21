class PrivacyBudgetManager:
    def __init__(self, epsilon: float = 1.0, delta: float = 1e-5, max_budget: float = 10.0):
        """
        Initializes the PrivacyBudgetManager, which keeps track of privacy budget during federated learning.
        :param epsilon: The epsilon value for differential privacy.
        :param delta: The delta value for differential privacy.
        :param max_budget: The maximum allowable privacy budget.
        """
        self.epsilon = epsilon
        self.delta = delta
        self.max_budget = max_budget
        self.current_budget = 0.0

    def consume_privacy_budget(self, epsilon_consumed: float):
        """
        Consumes a specified amount of the privacy budget.
        :param epsilon_consumed: The amount of epsilon to consume.
        :raises ValueError: If the consumed budget exceeds the max budget.
        """
        if self.current_budget + epsilon_consumed > self.max_budget:
            raise ValueError("Privacy budget exceeded. Training cannot proceed further without violating privacy guarantees.")
        self.current_budget += epsilon_consumed
        print(f"Consumed privacy budget: {epsilon_consumed}. Current budget: {self.current_budget}/{self.max_budget}")

    def reset_privacy_budget(self):
        """
        Resets the privacy budget to zero.
        """
        self.current_budget = 0.0
        print("Privacy budget reset to zero.")

    def get_remaining_budget(self) -> float:
        """
        Returns the remaining privacy budget.
        :return: The remaining privacy budget.
        """
        return self.max_budget - self.current_budget

    def is_budget_available(self, epsilon_needed: float) -> bool:
        """
        Checks if there is enough privacy budget available for a given consumption.
        :param epsilon_needed: The amount of epsilon needed for the next step.
        :return: True if enough budget is available, False otherwise.
        """
        return self.current_budget + epsilon_needed <= self.max_budget

# Example usage
if __name__ == "__main__":
    # Initialize PrivacyBudgetManager with max budget of 5.0
    pb_manager = PrivacyBudgetManager(epsilon=0.5, max_budget=5.0)

    # Simulate consuming privacy budget in federated learning
    try:
        pb_manager.consume_privacy_budget(0.5)  # Consume 0.5 of privacy budget
        pb_manager.consume_privacy_budget(1.0)  # Consume 1.0 of privacy budget
        pb_manager.consume_privacy_budget(3.0)  # Consume 3.0 of privacy budget
        # Attempting to consume more budget than available
        pb_manager.consume_privacy_budget(1.0)  # This should raise an error
    except ValueError as e:
        print(e)

    # Get remaining budget
    remaining_budget = pb_manager.get_remaining_budget()
    print(f"Remaining privacy budget: {remaining_budget}")

    # Reset the privacy budget
    pb_manager.reset_privacy_budget()
