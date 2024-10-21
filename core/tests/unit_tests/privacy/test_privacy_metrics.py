# privacy_metrics.py
import unittest
from privacy.privacy_metrics import PrivacyMetrics

class TestPrivacyMetrics(unittest.TestCase):
    def setUp(self):
        self.metrics = PrivacyMetrics()

    def test_privacy_metrics_calculation(self):
        metrics = self.metrics.calculate_metrics(noise_level=0.1, data_points=100)
        self.assertIn('epsilon', metrics)  # Verify metrics include epsilon value
        self.assertIn('delta', metrics)  # Verify metrics include delta value

    def test_utility_loss_tradeoff(self):
        utility_loss = self.metrics.calculate_utility_loss(noise_level=0.1)
        self.assertGreaterEqual(utility_loss, 0)  # Verify utility loss tradeoff is non-negative

if __name__ == '__main__':
    unittest.main()
