import numpy as np
import random

class DifferentialPrivacy:
    def __init__(self, epsilon: float, delta: float = 1e-5):
        """
        Initializes the Differential Privacy mechanism with given parameters.
        :param epsilon: Privacy budget parameter that determines the level of privacy.
        :param delta: Additional parameter to provide stronger privacy guarantees.
        """
        self.epsilon = epsilon
        self.delta = delta

    def laplace_mechanism(self, value: float, sensitivity: float) -> float:
        """
        Applies the Laplace mechanism to introduce noise to the given value.
        :param value: The original value to add noise to.
        :param sensitivity: The sensitivity of the value, representing the maximum change.
        :return: The noisy value.
        """
        scale = sensitivity / self.epsilon
        noise = np.random.laplace(0, scale)
        noisy_value = value + noise
        print(f"Laplace mechanism applied: original value = {value}, noise = {noise:.4f}, noisy value = {noisy_value:.4f}")
        return noisy_value

    def gaussian_mechanism(self, value: float, sensitivity: float) -> float:
        """
        Applies the Gaussian mechanism to introduce noise to the given value.
        :param value: The original value to add noise to.
        :param sensitivity: The sensitivity of the value, representing the maximum change.
        :return: The noisy value.
        """
        sigma = sensitivity * np.sqrt(2 * np.log(1.25 / self.delta)) / self.epsilon
        noise = random.gauss(0, sigma)
        noisy_value = value + noise
        print(f"Gaussian mechanism applied: original value = {value}, noise = {noise:.4f}, noisy value = {noisy_value:.4f}")
        return noisy_value

    def apply_noise_to_dataset(self, dataset: np.ndarray, sensitivity: float, mechanism: str = 'laplace') -> np.ndarray:
        """
        Applies the specified differential privacy mechanism to each value in the dataset.
        :param dataset: The original dataset.
        :param sensitivity: The sensitivity of the dataset values.
        :param mechanism: The type of mechanism to use: 'laplace' or 'gaussian'.
        :return: The dataset with added noise.
        """
        noisy_dataset = np.zeros_like(dataset)
        for i in range(len(dataset)):
            if mechanism == 'laplace':
                noisy_dataset[i] = self.laplace_mechanism(dataset[i], sensitivity)
            elif mechanism == 'gaussian':
                noisy_dataset[i] = self.gaussian_mechanism(dataset[i], sensitivity)
            else:
                raise ValueError("Invalid mechanism type. Choose either 'laplace' or 'gaussian'.")
        return noisy_dataset

# Example usage
if __name__ == "__main__":
    privacy = DifferentialPrivacy(epsilon=0.5)
    original_value = 42.0
    sensitivity = 1.0

    # Apply Laplace mechanism to the value
    noisy_value_laplace = privacy.laplace_mechanism(original_value, sensitivity)
    
    # Apply Gaussian mechanism to the value
    noisy_value_gaussian = privacy.gaussian_mechanism(original_value, sensitivity)

    # Apply noise to a dataset
    dataset = np.array([10, 20, 30, 40, 50])
    noisy_dataset = privacy.apply_noise_to_dataset(dataset, sensitivity, mechanism='laplace')
    print(f"Original dataset: {dataset}")
    print(f"Noisy dataset: {noisy_dataset}")