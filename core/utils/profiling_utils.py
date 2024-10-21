import time
import psutil
import os
from typing import Callable, Any

class ProfilingUtils:
    def __init__(self):
        self.process = psutil.Process(os.getpid())

    def profile_memory_usage(self) -> float:
        """
        Profiles the current memory usage of the process.
        :return: The memory usage in MB.
        """
        memory_usage = self.process.memory_info().rss / (1024 * 1024)  # Convert bytes to MB
        print(f"Current memory usage: {memory_usage:.2f} MB")
        return memory_usage

    def profile_cpu_usage(self) -> float:
        """
        Profiles the current CPU usage percentage of the process.
        :return: The CPU usage as a percentage.
        """
        cpu_usage = self.process.cpu_percent(interval=1.0)
        print(f"Current CPU usage: {cpu_usage:.2f}%")
        return cpu_usage

    def profile_function(self, func: Callable, *args, **kwargs) -> Any:
        """
        Profiles the execution time, memory, and CPU usage of a function.
        :param func: The function to be profiled.
        :param args: Positional arguments to the function.
        :param kwargs: Keyword arguments to the function.
        :return: The result of the function execution.
        """
        # Profile memory before function execution
        memory_before = self.profile_memory_usage()
        cpu_before = self.profile_cpu_usage()

        # Time function execution
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        # Profile memory after function execution
        memory_after = self.profile_memory_usage()
        cpu_after = self.profile_cpu_usage()

        # Calculate resource usage
        memory_diff = memory_after - memory_before
        cpu_diff = cpu_after - cpu_before
        execution_time = end_time - start_time

        # Print profiling results
        print(f"Function '{func.__name__}' execution time: {execution_time:.2f} seconds")
        print(f"Memory usage change during execution: {memory_diff:.2f} MB")
        print(f"CPU usage change during execution: {cpu_diff:.2f}%")

        return result

# Example usage
def sample_function(x, y):
    time.sleep(2)  # Simulate some processing time
    return x + y

if __name__ == "__main__":
    profiler = ProfilingUtils()
    result = profiler.profile_function(sample_function, 5, 10)
    print(f"Result of sample function: {result}")