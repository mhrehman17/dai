import os
import json
import hashlib
import logging
from typing import Any, Optional
from core.utils.file_utils import FileUtils

class CachingAgent:
    def __init__(self, cache_dir: str = './cache', logger: Optional[logging.Logger] = None):
        """
        Initializes a caching agent to store and retrieve data for faster processing.
        :param cache_dir: Directory where cache files should be stored.
        :param logger: Logger instance to log caching operations.
        """
        self.cache_dir = cache_dir
        self.logger = logger or logging.getLogger(__name__)
        self.file_utils = FileUtils(logger=self.logger)
        self.file_utils.create_directory(self.cache_dir)

    def _generate_cache_key(self, data: Any) -> str:
        """
        Generates a unique cache key based on the data using hashing.
        :param data: Data to generate the cache key for.
        :return: A unique cache key as a string.
        """
        data_string = json.dumps(data, sort_keys=True)
        return hashlib.md5(data_string.encode()).hexdigest()

    def save_to_cache(self, key: str, data: Any):
        """
        Saves data to the cache with a given key.
        :param key: The key to store the cached data.
        :param data: Data to be cached.
        """
        cache_filepath = os.path.join(self.cache_dir, f"{key}.json")
        try:
            self.file_utils.write_json(cache_filepath, data)
            self.logger.info(f"Data successfully cached with key: {key}")
        except Exception as e:
            self.logger.error(f"Failed to save data to cache with key {key}: {e}")

    def load_from_cache(self, key: str) -> Optional[Any]:
        """
        Loads data from the cache if it exists.
        :param key: The key to retrieve cached data.
        :return: The cached data, or None if not found.
        """
        cache_filepath = os.path.join(self.cache_dir, f"{key}.json")
        try:
            data = self.file_utils.read_json(cache_filepath)
            self.logger.info(f"Data successfully loaded from cache with key: {key}")
            return data
        except FileNotFoundError:
            self.logger.warning(f"Cache with key {key} not found.")
            return None
        except Exception as e:
            self.logger.error(f"Failed to load data from cache with key {key}: {e}")
            return None

    def delete_cache(self, key: str):
        """
        Deletes a cached file based on the key.
        :param key: The key of the cache to delete.
        """
        cache_filepath = os.path.join(self.cache_dir, f"{key}.json")
        try:
            self.file_utils.delete_file(cache_filepath)
            self.logger.info(f"Cache with key {key} successfully deleted.")
        except Exception as e:
            self.logger.error(f"Failed to delete cache with key {key}: {e}")

# Example usage
if __name__ == "__main__":
    # Set up logger
    cache_logger = logging.getLogger("caching_agent")
    cache_logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    cache_logger.addHandler(console_handler)

    # Initialize caching agent
    caching_agent = CachingAgent(logger=cache_logger)

    # Example data
    data = {"key": "value", "number": 42}
    cache_key = caching_agent._generate_cache_key(data)

    # Save data to cache
    caching_agent.save_to_cache(cache_key, data)

    # Load data from cache
    cached_data = caching_agent.load_from_cache(cache_key)
    print(f"Cached data: {cached_data}")

    # Delete cache
    caching_agent.delete_cache(cache_key)
