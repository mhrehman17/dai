import time
import logging
from typing import Dict
from core.utils.log_utils import LogUtils
class MetricUtils:
    def __init__(self, logger: logging.Logger):
        """
        Initializes the MetricUtils to manage and log various performance metrics.
        :param logger: Logger instance to log metric information.
        """
        self.logger = logger
        self.metrics = {}

    def start_timer(self, metric_name: str):
        """
        Starts a timer for a given metric to measure time taken.
        :param metric_name: Name of the metric to start timing.
        """
        self.metrics[metric_name] = time.time()
        self.logger.info(f"Started timing: {metric_name}")

    def end_timer(self, metric_name: str):
        """
        Ends the timer for a given metric and logs the duration.
        :param metric_name: Name of the metric to stop timing.
        """
        if metric_name in self.metrics:
            elapsed_time = time.time() - self.metrics[metric_name]
            self.logger.info(f"Metric '{metric_name}' completed in {elapsed_time:.2f} seconds.")
            del self.metrics[metric_name]
        else:
            self.logger.warning(f"Timer for metric '{metric_name}' was not started.")

    def log_metric(self, metric_name: str, value: float):
        """
        Logs a custom metric value.
        :param metric_name: Name of the metric.
        :param value: Value of the metric to be logged.
        """
        self.logger.info(f"Metric '{metric_name}': {value}")

    def get_metrics(self) -> Dict[str, float]:
        """
        Returns the current recorded metrics.
        :return: Dictionary of metrics and their values.
        """
        return self.metrics

# Example usage
if __name__ == "__main__":
    # Set up a logger for metrics management
    metric_logger = LogUtils.setup_logger(name="metric_manager", level=logging.INFO)

    # Initialize MetricUtils with the logger
    metric_utils = MetricUtils(logger=metric_logger)

    # Start and end timers for a sample operation
    metric_utils.start_timer("blockchain_sync")
    time.sleep(2)  # Simulate blockchain synchronization delay
    metric_utils.end_timer("blockchain_sync")

    # Log custom metrics
    metric_utils.log_metric("cpu_usage", 75.5)
    metric_utils.log_metric("memory_usage", 63.4)

    # Print recorded metrics
    print(metric_utils.get_metrics())
