import logging
import os
from datetime import datetime

class LogUtils:
    @staticmethod
    def setup_logger(name: str, log_dir: str = './logs', level: int = logging.INFO) -> logging.Logger:
        """
        Sets up a logger with specified name and configuration.
        :param name: The name of the logger.
        :param log_dir: Directory where log files should be saved.
        :param level: Logging level (e.g., logging.INFO, logging.DEBUG).
        :return: Configured logger instance.
        """
        # Create log directory if it does not exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            print(f"Log directory created at {log_dir}")
        
        # Create a log file named with the current date and logger name
        log_filename = os.path.join(log_dir, f"{name}_{datetime.now().strftime('%Y-%m-%d')}.log")
        
        # Set up the logger
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Create file handler for writing logs to a file
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(level)

        # Create console handler for outputting logs to the console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # Define log formatting
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

# Example usage
if __name__ == "__main__":
    # Set up a logger for a blockchain node
    node_logger = LogUtils.setup_logger(name="blockchain_node", level=logging.DEBUG)

    # Log some messages
    node_logger.info("Blockchain node started.")
    node_logger.debug("Debugging blockchain state.")
    node_logger.error("An error occurred while validating the blockchain.")
