import unittest
import logging
from core.communication.message_queue import MessageQueue  # Assuming the file is named message_queue.py

class TestMessageQueue(unittest.TestCase):
    
    def setUp(self):
        # Set up logger for the tests
        self.logger = logging.getLogger("test_message_queue")
        self.logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Initialize MessageQueue for testing
        self.message_queue = MessageQueue(logger=self.logger)
        
    def test_create_queue(self):
        # Test creating a new queue for an agent
        self.message_queue.create_queue("agent_1")
        self.assertIn("agent_1", self.message_queue.queues)
        print("test_create_queue passed")

    def test_create_queue_already_exists(self):
        # Test creating a queue that already exists
        self.message_queue.create_queue("agent_1")
        self.message_queue.create_queue("agent_1")  # Should log a warning without creating a duplicate
        self.assertIn("agent_1", self.message_queue.queues)
        print("test_create_queue_already_exists passed")
        
    def test_send_message_success(self):
        # Test sending a message to an existing agent's queue
        self.message_queue.create_queue("agent_1")
        self.message_queue.send_message("agent_1", "Hello, agent_1")
        self.assertEqual(self.message_queue.queues["agent_1"].qsize(), 1)
        print("test_send_message_success passed")

    def test_send_message_failure(self):
        # Test sending a message to a non-existing agent's queue
        self.message_queue.send_message("agent_1", "Hello, agent_1")  # Should log an error
        self.assertNotIn("agent_1", self.message_queue.queues)
        print("test_send_message_failure passed")

    def test_receive_message_success(self):
        # Test receiving a message from an agent's queue
        self.message_queue.create_queue("agent_1")
        self.message_queue.send_message("agent_1", "Hello, agent_1")
        message = self.message_queue.receive_message("agent_1")
        self.assertEqual(message, "Hello, agent_1")
        print("test_receive_message_success passed")

    def test_receive_message_timeout(self):
        # Test receiving a message from an agent's queue with a timeout when the queue is empty
        self.message_queue.create_queue("agent_1")
        message = self.message_queue.receive_message("agent_1", timeout=1)  # Should return None after timeout
        self.assertIsNone(message)
        print("test_receive_message_timeout passed")

    def test_receive_message_no_queue(self):
        # Test receiving a message from a non-existing agent's queue
        message = self.message_queue.receive_message("agent_1")  # Should log an error and return None
        self.assertIsNone(message)
        print("test_receive_message_no_queue passed")

    def test_delete_queue_success(self):
        # Test deleting an existing agent's queue
        self.message_queue.create_queue("agent_1")
        self.message_queue.delete_queue("agent_1")
        self.assertNotIn("agent_1", self.message_queue.queues)
        print("test_delete_queue_success passed")

    def test_delete_queue_failure(self):
        # Test deleting a non-existing agent's queue
        self.message_queue.delete_queue("agent_1")  # Should log a warning
        self.assertNotIn("agent_1", self.message_queue.queues)
        print("test_delete_queue_failure passed")

if __name__ == '__main__':
    unittest.main()
