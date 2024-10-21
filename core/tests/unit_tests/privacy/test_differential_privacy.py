# differential_privacy.py
import unittest
from unittest.mock import patch
from privacy.differential_privacy import DifferentialPrivacy

class TestDifferentialPrivacy(unittest.TestCase):
    def setUp(self):
        self.dp = DifferentialPrivacy()

    @patch('privacy.differential_privacy.add_noise')
    def test_add_noise_to_gradients(self, mock_add_noise):
        mock_add_noise.return_value = 0.5
        noisy_value = self.dp.add_noise(1.0, epsilon=0.1)
        self.assertAlmostEqual(noisy_value, 0.5, delta=0.1)  # Verify noise is added to gradients

    def test_epsilon_delta_configuration(self):
        epsilon, delta = self.dp.configure_privacy_params(epsilon=1.0, delta=1e-5)
        self.assertEqual(epsilon, 1.0)
        self.assertEqual(delta, 1e-5)  # Verify epsilon and delta configurations are set correctly

if __name__ == '__main__':
    unittest.main()
