import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import logging
import time
from core.monitoring.log_collector import LogCollector  # Assuming the class is in a file named log_collector.py


class TestLogCollector(unittest.TestCase):

    def setUp(self):
        # Example directories for testing
        self.log_directories = ["./core/logs/agents", "./logs/orchestrator", "./logs/blockchain"]
        # Create a mock logger
        self.logger = MagicMock(spec=logging.Logger)
        # Initialize LogCollector
        self.collector = LogCollector(log_directories=self.log_directories, collection_interval=5, logger=self.logger)

    @patch("os.path.exists")
    @patch("os.listdir")
    def test_process_directory_logs(self, mock_listdir, mock_exists):
        """Test processing of a valid directory with log files."""
        # Mock the directory to exist
        mock_exists.return_value = True
        # Return a valid .log file in the directory listing
        mock_listdir.return_value = ["test.log", "not_a_log.txt"]  # Simulate one valid log file and one invalid file

        with patch("builtins.open", mock_open(read_data="Test log line")) as mock_file:
            self.collector._process_directory("./core/logs/agents")

            # Ensure the log file was opened and processed
            mock_file.assert_any_call("./core/logs/agents/test.log", "r")
            self.logger.info.assert_any_call("[test.log] Test log line")
            # Ensure that the invalid file is skipped
            self.assertEqual(self.logger.info.call_count, 1)

    @patch("os.path.exists")
    def test_process_directory_non_existent(self, mock_exists):
        """Test processing of a non-existent directory."""
        # Mock the directory to not exist
        mock_exists.return_value = False

        self.collector._process_directory("./core/logs/agents")

        # Ensure a warning is logged for non-existent directory
        self.logger.warning.assert_called_with("Directory does not exist: ./logs/agents")

    @patch("os.listdir")
    @patch("os.path.exists")
    def test_process_log_file_exception(self, mock_exists, mock_listdir):
        """Test handling an exception when processing a log file."""
        # Mock the directory to exist
        mock_exists.return_value = True
        # Return one log file
        mock_listdir.return_value = ["test.log"]

        with patch("builtins.open", mock_open()) as mock_file:
            # Simulate an error when opening the file
            mock_file.side_effect = Exception("File read error")

            self.collector._process_directory("./core/logs/agents")

            # Ensure the error is logged
            self.logger.error.assert_any_call("Error while processing log file ./logs/agents/test.log: File read error")

    @patch("os.listdir")
    @patch("os.path.exists")
    def test_collect_logs_exception_handling(self, mock_exists, mock_listdir):
        """Test exception handling during log collection process."""
        # Mock an exception when os.path.exists is called
        mock_exists.side_effect = Exception("Unexpected error")

        # Run _collect_logs in a controlled environment to simulate one iteration
        with patch("time.sleep") as mock_sleep:
            self.collector._collect_logs()

            # Ensure the exception was caught and logged
            self.logger.error.assert_any_call("Error while collecting logs: Unexpected error")
            # Ensure sleep was called to continue the loop
            mock_sleep.assert_called()

    @patch("os.listdir")
    @patch("os.path.exists")
    def test_start_stop_collection(self, mock_exists, mock_listdir):
        """Test starting and stopping the log collection."""
        # Mock the directory to exist
        mock_exists.return_value = True
        mock_listdir.return_value = []

        with patch("time.sleep") as mock_sleep:
            # Start the log collection
            self.collector.start_collection()
            time.sleep(0.1)  # Let the thread run for a short time
            self.collector.stop_collection()

            # Ensure log messages are correct
            self.logger.info.assert_any_call("Log collection started.")
            self.logger.info.assert_any_call("Log collection stopped.")

            # Ensure sleep was called as part of the loop
            mock_sleep.assert_called()

    def test_process_directory_no_log_files(self):
        """Test that no log files are processed when there are none in the directory."""
        with patch("os.path.exists", return_value=True), \
             patch("os.listdir", return_value=["not_a_log.txt"]):  # No valid log files

            self.collector._process_directory("./core/logs/agents")
            # Ensure no logs were processed
            self.logger.info.assert_not_called()


if __name__ == "__main__":
    unittest.main()
