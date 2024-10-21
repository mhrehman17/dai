# metric_utils.py
import unittest
from utilities.metric_utils import MetricUtils

class TestMetricUtils(unittest.TestCase):
    def setUp(self):
        self.metric_utils = MetricUtils()

    def test_accuracy_calculation(self):
        y_true = [1, 0, 1, 1]
        y_pred = [1, 0, 1, 0]
        accuracy = self.metric_utils.calculate_accuracy(y_true, y_pred)
        self.assertEqual(accuracy, 0.75)  # Verify accuracy calculation

    def test_precision_calculation(self):
        y_true = [1, 0, 1, 1]
        y_pred = [1, 0, 1, 0]
        precision = self.metric_utils.calculate_precision(y_true, y_pred)
        self.assertEqual(precision, 1.0)  # Verify precision calculation

    def test_recall_calculation(self):
        y_true = [1, 0, 1, 1]
        y_pred = [1, 0, 1, 0]
        recall = self.metric_utils.calculate_recall(y_true, y_pred)
        self.assertEqual(recall, 0.6666666666666666)  # Verify recall calculation

if __name__ == '__main__':
    unittest.main()

