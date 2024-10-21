# personalized_model.py
import unittest
from models.personalized_model import PersonalizedModel

class TestPersonalizedModel(unittest.TestCase):
    def setUp(self):
        self.model = PersonalizedModel()

    def test_model_personalization(self):
        user_data = [0.5, 0.6, 0.7]  # Sample user-specific data
        result = self.model.personalize(user_data)
        self.assertTrue(result)  # Verify model personalization is successful

    def test_metrics_calculation(self):
        metrics = self.model.calculate_metrics()
        self.assertIn('accuracy', metrics)  # Verify metrics include accuracy
        self.assertIn('loss', metrics)  # Verify metrics include loss

if __name__ == '__main__':
    unittest.main()
