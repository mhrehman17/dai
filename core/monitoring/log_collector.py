import os
import logging
import time
import threading
from typing import List, Dict, Optional

class LogCollector:
    def __init__(self, log_directories: List[str], collection_interval: int = 10, logger: Optional[logging.Logger] = None):
        """
        Initializes the LogCollector for collecting logs from specified directories.
        :param log_directories: A list of directories where log files are located.
        :param collection_interval: The time interval (in seconds) between each collection.
        :param logger: Logger instance to log collection activities.
        """
        self.log_directories = log_directories
        self.collection_interval = collection_interval
        self.logger = logger or logging.getLogger(__name__)
        self.running = False

    def start_collection(self):
        """
        Starts the log collection process in a separate thread.
        """
        self.running = True
        threading.Thread(target=self._collect_logs, daemon=True).start()
        self.logger.info("Log collection started.")

    def stop_collection(self):
        """
        Stops the log collection process.
        """
        self.running = False
        self.logger.info("Log collection stopped.")

    def _collect_logs(self):
        """
        Collects logs from specified directories periodically.
        """
        while self.running:
            try:
                for directory in self.log_directories:
                    self._process_directory(directory)
                time.sleep(self.collection_interval)
            except Exception as e:
                self.logger.error(f"Error while collecting logs: {e}")
                time.sleep(self.collection_interval)

    def _process_directory(self, directory: str):
        """
        Processes all log files in the specified directory.
        :param directory: The directory containing log files.
        """
        if not os.path.exists(directory):
            self.logger.warning(f"Directory does not exist: {directory}")
            return

        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path) and filename.endswith(".log"):
                self._process_log_file(file_path)

    def _process_log_file(self, file_path: str):
        """
        Processes a single log file by reading its content and logging it.
        :param file_path: The path to the log file.
        """
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    self.logger.info(f"[{os.path.basename(file_path)}] {line.strip()}")
        except Exception as e:
            self.logger.error(f"Error while processing log file {file_path}: {e}")

# Example usage
if __name__ == "__main__":
    # Set up logger
    log_collector_logger = logging.getLogger("log_collector")
    log_collector_logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    log_collector_logger.addHandler(console_handler)

    # Directories to collect logs from
    log_directories = [
        "./logs/agents",
        "./logs/orchestrator",
        "./logs/blockchain"
    ]

    # Initialize LogCollector
    log_collector = LogCollector(log_directories=log_directories, collection_interval=15, logger=log_collector_logger)

    # Start collecting logs
    log_collector.start_collection()

    # Allow some time for demonstration purposes
    try:
        time.sleep(60)  # Keep running for 1 minute to simulate log collection
    finally:
        log_collector.stop_collection()
