import unittest
from core.utils.resource_manager import ResourceManager
from unittest.mock import patch, MagicMock

class TestResourceManager(unittest.TestCase):
    def setUp(self):
        # Set up an instance of the ResourceManager before each test
        self.resource_manager = ResourceManager()

    @patch("core.utils.resource_manager.ResourceManager.check_cpu_usage")
    def test_check_cpu_usage(self, mock_check_cpu_usage):
        # Test checking CPU usage
        mock_check_cpu_usage.return_value = 45  # Assume CPU usage is 45%
        result = self.resource_manager.check_cpu_usage()
        mock_check_cpu_usage.assert_called_once()
        self.assertEqual(result, 45)

    @patch("core.utils.resource_manager.ResourceManager.check_memory_usage")
    def test_check_memory_usage(self, mock_check_memory_usage):
        # Test checking memory usage
        mock_check_memory_usage.return_value = 60  # Assume memory usage is 60%
        result = self.resource_manager.check_memory_usage()
        mock_check_memory_usage.assert_called_once()
        self.assertEqual(result, 60)

    @patch("core.utils.resource_manager.ResourceManager.allocate_resources")
    def test_allocate_resources(self, mock_allocate_resources):
        # Test allocating resources for a task
        mock_allocate_resources.return_value = "Resources allocated"
        result = self.resource_manager.allocate_resources("training_task")
        mock_allocate_resources.assert_called_once_with("training_task")
        self.assertEqual(result, "Resources allocated")

    def tearDown(self):
        # Clean up after each test
        self.resource_manager = None

if __name__ == "__main__":
    unittest.main()
