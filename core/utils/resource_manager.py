import psutil
import logging
from core.utils.log_utils import LogUtils

class ResourceManager:
    def __init__(self, logger: logging.Logger):
        """
        Initializes the ResourceManager to monitor system resources.
        :param logger: Logger instance to log resource information.
        """
        self.logger = logger

    def get_cpu_usage(self) -> float:
        """
        Retrieves the current CPU usage percentage.
        :return: CPU usage as a float percentage.
        """
        cpu_usage = psutil.cpu_percent(interval=1)
        self.logger.info(f"CPU Usage: {cpu_usage}%")
        return cpu_usage

    def get_memory_usage(self) -> float:
        """
        Retrieves the current memory usage percentage.
        :return: Memory usage as a float percentage.
        """
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent
        self.logger.info(f"Memory Usage: {memory_usage}%")
        return memory_usage

    def get_disk_usage(self) -> float:
        """
        Retrieves the current disk usage percentage.
        :return: Disk usage as a float percentage.
        """
        disk_info = psutil.disk_usage('/')
        disk_usage = disk_info.percent
        self.logger.info(f"Disk Usage: {disk_usage}%")
        return disk_usage

    def get_available_memory(self) -> int:
        """
        Retrieves the available memory in bytes.
        :return: Available memory in bytes.
        """
        memory_info = psutil.virtual_memory()
        available_memory = memory_info.available
        self.logger.info(f"Available Memory: {available_memory} bytes")
        return available_memory

# Example usage
if __name__ == "__main__":
    # Set up a logger for resource management
    resource_logger = LogUtils.setup_logger(name="resource_manager", level=logging.INFO)

    # Initialize ResourceManager with the logger
    resource_manager = ResourceManager(logger=resource_logger)

    # Monitor system resources
    cpu_usage = resource_manager.get_cpu_usage()
    memory_usage = resource_manager.get_memory_usage()
    disk_usage = resource_manager.get_disk_usage()
    available_memory = resource_manager.get_available_memory()
