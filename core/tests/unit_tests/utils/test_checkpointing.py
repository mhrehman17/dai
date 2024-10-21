# checkpointing.py
import unittest
from unittest.mock import patch, MagicMock
from utilities.checkpointing import Checkpointing

class TestCheckpointing(unittest.TestCase):
    def setUp(self):
        self.checkpointing = Checkpointing()

    @patch('utilities.checkpointing.save_checkpoint')
    def test_save_checkpoint(self, mock_save_checkpoint):
        mock_save_checkpoint.return_value = True
        result = self.checkpointing.save_checkpoint('model_state', 'checkpoint.pth')
        self.assertTrue(result)  # Verify checkpoint saving is successful

    @patch('utilities.checkpointing.load_checkpoint')
    def test_load_checkpoint(self, mock_load_checkpoint):
        mock_load_checkpoint.return_value = 'model_state'
        result = self.checkpointing.load_checkpoint('checkpoint.pth')
        self.assertEqual(result, 'model_state')  # Verify checkpoint loading is successful

    def test_checkpoint_integrity(self):
        # Simulate saving and loading multiple times to verify integrity
        state = 'initial_state'
        for _ in range(5):
            self.checkpointing.save_checkpoint(state, 'checkpoint.pth')
            state = self.checkpointing.load_checkpoint('checkpoint.pth')
        self.assertEqual(state, 'initial_state')  # Verify checkpoint integrity after multiple iterations

if __name__ == '__main__':
    unittest.main()

