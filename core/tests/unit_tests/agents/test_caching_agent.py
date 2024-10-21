import unittest
from unittest.mock import patch, MagicMock, mock_open
import logging
import os
import json
from core.agents.caching_agent import CachingAgent
from core.utils.file_utils import FileUtils


class TestCachingAgent(unittest.TestCase):

    def setUp(self):
        # Set up a logger to capture the output during tests
        self.logger = logging.getLogger("test_logger")
        self.logger.setLevel(logging.INFO)
        self.caching_agent = CachingAgent(cache_dir='./test_cache', logger=self.logger)

    @patch('core.utils.file_utils.FileUtils.create_directory')
    def test_initialization(self, mock_create_directory):
        # Verify that the cache directory is created during initialization
        caching_agent = CachingAgent(cache_dir='./test_cache', logger=self.logger)
        mock_create_directory.assert_called_once_with('./test_cache')

    def test_generate_cache_key(self):
        # Test the generation of a cache key
        data = {"key": "value", "number": 42}
        key = self.caching_agent._generate_cache_key(data)
        self.assertIsInstance(key, str)
        # Verify the key length (MD5 hash length)
        self.assertEqual(len(key), 32)

    @patch('core.utils.file_utils.FileUtils.write_json')
    def test_save_to_cache_success(self, mock_write_json):
        # Test saving data to cache successfully
        data = {"key": "value", "number": 42}
        key = self.caching_agent._generate_cache_key(data)
        self.caching_agent.save_to_cache(key, data)
        cache_filepath = os.path.join('./test_cache', f"{key}.json")
        mock_write_json.assert_called_once_with(cache_filepath, data)

    @patch('core.utils.file_utils.FileUtils.write_json', side_effect=Exception("Write failed"))
    def test_save_to_cache_failure(self, mock_write_json):
        # Test failure when saving data to cache
        data = {"key": "value", "number": 42}
        key = self.caching_agent._generate_cache_key(data)
        with patch.object(self.logger, 'error') as mock_logger_error:
            self.caching_agent.save_to_cache(key, data)
            mock_logger_error.assert_called_once_with(f"Failed to save data to cache with key {key}: Write failed")

    @patch('core.utils.file_utils.FileUtils.read_json')
    def test_load_from_cache_success(self, mock_read_json):
        # Test loading data from cache successfully
        data = {"key": "value", "number": 42}
        key = self.caching_agent._generate_cache_key(data)
        mock_read_json.return_value = data
        result = self.caching_agent.load_from_cache(key)
        cache_filepath = os.path.join('./test_cache', f"{key}.json")
        mock_read_json.assert_called_once_with(cache_filepath)
        self.assertEqual(result, data)

    @patch('core.utils.file_utils.FileUtils.read_json', side_effect=FileNotFoundError)
    def test_load_from_cache_not_found(self, mock_read_json):
        # Test loading from cache when cache does not exist
        key = "non_existent_key"
        with patch.object(self.logger, 'warning') as mock_logger_warning:
            result = self.caching_agent.load_from_cache(key)
            cache_filepath = os.path.join('./test_cache', f"{key}.json")
            mock_read_json.assert_called_once_with(cache_filepath)
            mock_logger_warning.assert_called_once_with(f"Cache with key {key} not found.")
            self.assertIsNone(result)

    @patch('core.utils.file_utils.FileUtils.read_json', side_effect=Exception("Read failed"))
    def test_load_from_cache_failure(self, mock_read_json):
        # Test loading from cache failure with an unexpected exception
        key = "some_key"
        with patch.object(self.logger, 'error') as mock_logger_error:
            result = self.caching_agent.load_from_cache(key)
            cache_filepath = os.path.join('./test_cache', f"{key}.json")
            mock_read_json.assert_called_once_with(cache_filepath)
            mock_logger_error.assert_called_once_with(f"Failed to load data from cache with key {key}: Read failed")
            self.assertIsNone(result)

    @patch('core.utils.file_utils.FileUtils.delete_file')
    def test_delete_cache_success(self, mock_delete_file):
        # Test deleting a cache successfully
        key = "test_key"
        self.caching_agent.delete_cache(key)
        cache_filepath = os.path.join('./test_cache', f"{key}.json")
        mock_delete_file.assert_called_once_with(cache_filepath)

    @patch('core.utils.file_utils.FileUtils.delete_file', side_effect=Exception("Delete failed"))
    def test_delete_cache_failure(self, mock_delete_file):
        # Test failure to delete cache file
        key = "test_key"
        with patch.object(self.logger, 'error') as mock_logger_error:
            self.caching_agent.delete_cache(key)
            mock_logger_error.assert_called_once_with(f"Failed to delete cache with key {key}: Delete failed")

if __name__ == '__main__':
    unittest.main()
