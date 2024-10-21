
# file_utils.py
import unittest
from unittest.mock import patch, mock_open
from utilities.file_utils import FileUtils

class TestFileUtils(unittest.TestCase):
    def setUp(self):
        self.file_utils = FileUtils()

    @patch('builtins.open', new_callable=mock_open, read_data='file content')
    def test_file_reading(self, mock_file):
        content = self.file_utils.read_file('dummy.txt')
        self.assertEqual(content, 'file content')  # Verify file reading

    @patch('builtins.open', new_callable=mock_open)
    def test_file_writing(self, mock_file):
        result = self.file_utils.write_file('dummy.txt', 'new content')
        self.assertTrue(result)  # Verify file writing is successful
        mock_file().write.assert_called_once_with('new content')

    @patch('utilities.file_utils.os.path.exists')
    def test_missing_file_error_handling(self, mock_exists):
        mock_exists.return_value = False
        with self.assertRaises(FileNotFoundError):
            self.file_utils.read_file('missing.txt')  # Verify error handling for missing files

if __name__ == '__main__':
    unittest.main()
