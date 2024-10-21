import numpy as np
from typing import List

class SecureMPC:
    def __init__(self, num_parties: int = 3):
        """
        Initializes the Secure Multi-Party Computation (MPC) system.
        :param num_parties: Number of parties involved in the secure computation.
        """
        self.num_parties = num_parties

    def secret_share(self, value: float) -> List[float]:
        """
        Secret shares a value among multiple parties.
        :param value: The value to be secret shared.
        :return: A list of shares distributed to different parties.
        """
        shares = np.random.uniform(-value, value, self.num_parties - 1).tolist()
        final_share = value - sum(shares)
        shares.append(final_share)
        print(f"Secret shared value {value} into shares: {shares}")
        return shares

    def reconstruct_secret(self, shares: List[float]) -> float:
        """
        Reconstructs the original value from its shares.
        :param shares: List of shares from different parties.
        :return: The reconstructed value.
        """
        reconstructed_value = sum(shares)
        print(f"Reconstructed value from shares {shares}: {reconstructed_value}")
        return reconstructed_value

    def secure_sum(self, values: List[float]) -> float:
        """
        Computes the sum of secret shared values in a privacy-preserving manner.
        :param values: List of values to be summed securely.
        :return: The sum of all values.
        """
        shares_per_value = [self.secret_share(value) for value in values]
        summed_shares = [sum(share) for share in zip(*shares_per_value)]
        secure_sum_result = self.reconstruct_secret(summed_shares)
        print(f"Secure sum of values {values}: {secure_sum_result}")
        return secure_sum_result

# Example usage
if __name__ == "__main__":
    # Initialize SecureMPC with 3 parties
    secure_mpc = SecureMPC(num_parties=3)

    # Secret share a value
    value = 42.0
    shares = secure_mpc.secret_share(value)

    # Reconstruct the original value from shares
    reconstructed_value = secure_mpc.reconstruct_secret(shares)

    # Perform secure sum on a list of values
    values = [10.0, 20.0, 30.0]
    secure_sum_result = secure_mpc.secure_sum(values)
