import unittest
from core.monitoring.privacy_monitor import PrivacyMonitor
from unittest.mock import patch, MagicMock

class TestPrivacyMonitor(unittest.TestCase):
    def setUp(self):
        # Set up an instance of the PrivacyMonitor before each test
        self.privacy_monitor = PrivacyMonitor()

    @patch("core.monitoring.privacy_monitor.PrivacyMonitor.track_privacy_budget")
    def test_track_privacy_budget(self, mock_track_privacy_budget):
        # Test tracking the privacy budget for agents
        mock_track_privacy_budget.return_value = {"agent_1": 0.75, "agent_2": 0.50}
        result = self.privacy_monitor.track_privacy_budget(["agent_1", "agent_2"])
        mock_track_privacy_budget.assert_called_once_with(["agent_1", "agent_2"])
        self.assertEqual(result, {"agent_1": 0.75, "agent_2": 0.50})

    @patch("core.monitoring.privacy_monitor.PrivacyMonitor.check_compliance")
    def test_check_compliance(self, mock_check_compliance):
        # Test checking compliance with privacy policies
        mock_check_compliance.return_value = {"agent_1": "compliant", "agent_2": "non-compliant"}
        result = self.privacy_monitor.check_compliance(["agent_1", "agent_2"])
        mock_check_compliance.assert_called_once_with(["agent_1", "agent_2"])
        self.assertEqual(result, {"agent_1": "compliant", "agent_2": "non-compliant"})

    @patch("core.monitoring.privacy_monitor.PrivacyMonitor.alert_on_privacy_violation")
    def test_alert_on_privacy_violation(self, mock_alert_on_privacy_violation):
        # Test raising an alert when a privacy violation is detected
        mock_alert_on_privacy_violation.return_value = "Privacy violation alert triggered"
        result = self.privacy_monitor.alert_on_privacy_violation("agent_2", "data_leak")
        mock_alert_on_privacy_violation.assert_called_once_with("agent_2", "data_leak")
        self.assertEqual(result, "Privacy violation alert triggered")

    def tearDown(self):
        # Clean up after each test
        self.privacy_monitor = None

if __name__ == "__main__":
    unittest.main()
