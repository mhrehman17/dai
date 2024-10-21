import os
import pickle
import hashlib
import logging
from typing import Any, Optional

class DataCache:
    def __init__(self, cache_dir: str = './data_cache', logger: Optional[logging.Logger] = None):
        """
        Initializes the DataCache for storing and retrieving data efficiently.
        :param cache_dir: Directory where cached data should be stored.
        :param logger: Logger instance to log caching activities.
        """
        self.cache_dir = cache_dir
        self.logger = logger or logging.getLogger(__name__)
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
            self.logger.info(f"Cache directory created at {self.cache_dir}")

    def _generate_cache_key(self, data: Any) -> str:
        """
        Generates a unique cache key for the given data using hashing.
        :param data: Data to generate a cache key for.
        :return: A hash key representing the given data.
        """
        data_bytes = pickle.dumps(data)
        cache_key = hashlib.md5(data_bytes).hexdigest()
        return cache_key

    def save_to_cache(self, key: str, data: Any):
        """
        Saves data to the cache with the specified key.
        :param key: Unique identifier for the cached data.
        :param data: The data to be cached.
        """
        cache_filepath = os.path.join(self.cache_dir, f"{key}.pkl")
        try:
            with open(cache_filepath, 'wb') as cache_file:
                pickle.dump(data, cache_file)
            self.logger.info(f"Data successfully cached with key: {key}")
        except Exception as e:
            self.logger.error(f"Failed to save data to cache with key {key}: {e}")

    def load_from_cache(self, key: str) -> Optional[Any]:
        """
        Loads data from the cache with the specified key.
        :param key: Unique identifier for the cached data.
        :return: The cached data, or None if the key is not found.
        """
        cache_filepath = os.path.join(self.cache_dir, f"{key}.pkl")
        if not os.path.exists(cache_filepath):
            self.logger.warning(f"Cache with key {key} not found.")
            return None
        try:
            with open(cache_filepath, 'rb') as cache_file:
                data = pickle.load(cache_file)
            self.logger.info(f"Data successfully loaded from cache with key: {key}")
            return data
        except Exception as e:
            self.logger.error(f"Failed to load data from cache with key {key}: {e}")
            return None

    def delete_from_cache(self, key: str):
        """
        Deletes cached data for a given key.
        :param key: Unique identifier for the cached data to be deleted.
        """
        cache_filepath = os.path.join(self.cache_dir, f"{key}.pkl")
        try:
            if os.path.exists(cache_filepath):
                os.remove(cache_filepath)
                self.logger.info(f"Cache with key {key} successfully deleted.")
            else:
                self.logger.warning(f"Attempted to delete non-existent cache with key {key}")
        except Exception as e:
            self.logger.error(f"Failed to delete cache with key {key}: {e}")

# Example usage
if __name__ == "__main__":
    # Set up logger
    cache_logger = logging.getLogger("data_cache")
    cache_logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    cache_logger.addHandler(console_handler)

    # Initialize DataCache
    data_cache = DataCache(logger=cache_logger)

    # Example data to cache
    data = {"key": "value", "number": 42}
    cache_key = data_cache._generate_cache_key(data)

    # Save data to cache
    data_cache.save_to_cache(cache_key, data)

    # Load data from cache
    cached_data = data_cache.load_from_cache(cache_key)
    print(f"Cached data: {cached_data}")

    # Delete data from cache
    data_cache.delete_from_cache(cache_key)