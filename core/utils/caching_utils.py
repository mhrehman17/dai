import os
import pickle
import hashlib
from typing import Any

class CachingUtils:
    def __init__(self, cache_dir: str = './cache'):
        """
        Initializes caching utilities with the given cache directory.
        :param cache_dir: The directory where cached files will be stored.
        """
        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def _generate_cache_key(self, key: str) -> str:
        """
        Generates a hashed cache key from the given key string.
        :param key: The string to generate a cache key from.
        :return: A hashed string representing the cache key.
        """
        return hashlib.md5(key.encode()).hexdigest()

    def save_to_cache(self, key: str, data: Any):
        """
        Saves the data to the cache with the given key.
        :param key: The key to store the data under.
        :param data: The data to be cached.
        """
        cache_key = self._generate_cache_key(key)
        cache_path = os.path.join(self.cache_dir, cache_key)
        with open(cache_path, 'wb') as cache_file:
            pickle.dump(data, cache_file)
        print(f"Data cached successfully under key: {key}")

    def load_from_cache(self, key: str) -> Any:
        """
        Loads the data from the cache using the given key.
        :param key: The key to load the data from.
        :return: The cached data, if found, otherwise None.
        """
        cache_key = self._generate_cache_key(key)
        cache_path = os.path.join(self.cache_dir, cache_key)
        if os.path.exists(cache_path):
            with open(cache_path, 'rb') as cache_file:
                print(f"Data loaded successfully from key: {key}")
                return pickle.load(cache_file)
        else:
            print(f"Cache miss for key: {key}")
            return None

    def clear_cache(self):
        """
        Clears all cached files in the cache directory.
        """
        for filename in os.listdir(self.cache_dir):
            file_path = os.path.join(self.cache_dir, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        print(f"All cache cleared from directory: {self.cache_dir}")

# Example usage
if __name__ == "__main__":
    cache_utils = CachingUtils()
    sample_data = {"name": "MNIST Model", "accuracy": 0.95}
    cache_utils.save_to_cache("model_v1_metrics", sample_data)
    loaded_data = cache_utils.load_from_cache("model_v1_metrics")
    print(loaded_data)