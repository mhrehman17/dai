import unittest
import os
import shutil
import pickle
import hashlib
from core.data.data_cache import DataCache  # Assuming this is saved under core/data_cache.py


class TestDataCache(unittest.TestCase):
    
    def setUp(self):
        # Set up the cache directory for testing
        self.cache_dir = './test_data_cache'
        self.data_cache = DataCache(cache_dir=self.cache_dir)
        self.test_data = {"key": "value", "number": 42}
        self.test_key = self.data_cache._generate_cache_key(self.test_data)

    def tearDown(self):
        # Clean up by deleting the test cache directory
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)

    def test_generate_cache_key(self):
        # Ensure the cache key is generated correctly
        data_bytes = pickle.dumps(self.test_data)
        expected_key = hashlib.md5(data_bytes).hexdigest()
        self.assertEqual(self.test_key, expected_key)

    def test_save_to_cache(self):
        # Test saving data to cache
        self.data_cache.save_to_cache(self.test_key, self.test_data)
        cache_filepath = os.path.join(self.cache_dir, f"{self.test_key}.pkl")
        self.assertTrue(os.path.exists(cache_filepath))

    def test_load_from_cache(self):
        # Test loading data from cache after saving it
        self.data_cache.save_to_cache(self.test_key, self.test_data)
        loaded_data = self.data_cache.load_from_cache(self.test_key)
        self.assertEqual(loaded_data, self.test_data)

    def test_load_from_cache_nonexistent_key(self):
        # Test loading data from cache that doesn't exist
        nonexistent_key = "nonexistent_key"
        loaded_data = self.data_cache.load_from_cache(nonexistent_key)
        self.assertIsNone(loaded_data)

    def test_delete_from_cache(self):
        # Test deleting data from cache
        self.data_cache.save_to_cache(self.test_key, self.test_data)
        cache_filepath = os.path.join(self.cache_dir, f"{self.test_key}.pkl")
        self.assertTrue(os.path.exists(cache_filepath))
        
        # Delete the data and ensure it's removed
        self.data_cache.delete_from_cache(self.test_key)
        self.assertFalse(os.path.exists(cache_filepath))

    def test_delete_nonexistent_cache_key(self):
        # Test deleting a non-existent cache key
        nonexistent_key = "nonexistent_key"
        # Should not raise any errors
        self.data_cache.delete_from_cache(nonexistent_key)
        

if __name__ == '__main__':
    unittest.main()
