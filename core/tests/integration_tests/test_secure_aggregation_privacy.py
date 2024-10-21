import unittest
import numpy as np
from core.orchestrator.secure_aggregation import SecureAggregation
from core.privacy.differential_privacy import DifferentialPrivacy

class TestSecureAggregationPrivacyIntegration(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment for Secure Aggregation and Differential Privacy integration tests.
        """
        self.secure_agg = SecureAggregation()
        self.differential_privacy = DifferentialPrivacy(epsilon=0.5)

        # Simulating model updates from agents
        self.update_1 = np.array([1.0, 2.0, 3.0])
        self.update_2 = np.array([1.5, 2.5, 3.5])
        self.update_3 = np.array([0.5, 1.5, 2.5])

    def test_secure_aggregation_with_differential_privacy(self):
        """
        Test the integration of secure aggregation with differential privacy.
        """
        # Apply differential privacy noise to updates before adding them for aggregation
        noisy_update_1 = self.differential_privacy.laplace_mechanism(self.update_1, sensitivity=1.0)
        noisy_update_2 = self.differential_privacy.laplace_mechanism(self.update_2, sensitivity=1.0)
        noisy_update_3 = self.differential_privacy.laplace_mechanism(self.update_3, sensitivity=1.0)

        # Add noisy updates to secure aggregation
        self.secure_agg.add_update("agent_1", noisy_update_1)
        self.secure_agg.add_update("agent_2", noisy_update_2)
        self.secure_agg.add_update("agent_3", noisy_update_3)

        # Perform secure aggregation
        aggregated_update = self.secure_agg.aggregate_updates()

        # Verify the shape of the aggregated update
        self.assertEqual(aggregated_update.shape, self.update_1.shape, "Aggregated update should have the same shape as individual updates.")

    def test_privacy_level_impact_on_aggregation(self):
        """
        Test the impact of different privacy levels on the aggregated result.
        """
        # Apply differential privacy with varying epsilon values to see impact
        privacy_low = DifferentialPrivacy(epsilon=0.1)
        privacy_high = DifferentialPrivacy(epsilon=1.0)

        noisy_update_low_privacy = privacy_low.laplace_mechanism(self.update_1, sensitivity=1.0)
        noisy_update_high_privacy = privacy_high.laplace_mechanism(self.update_1, sensitivity=1.0)

        # Compare how different noise levels affect the update values
        difference_low_privacy = np.abs(self.update_1 - noisy_update_low_privacy).mean()
        difference_high_privacy = np.abs(self.update_1 - noisy_update_high_privacy).mean()

        # Expect that low privacy (high noise) should result in greater average difference
        self.assertGreater(difference_low_privacy, difference_high_privacy, "Lower epsilon should lead to higher noise and greater difference.")

if __name__ == "__main__":
    unittest.main()
