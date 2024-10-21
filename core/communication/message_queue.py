import queue
import threading
import logging
from typing import Any, Dict, Optional

class MessageQueue:
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initializes a message queue for agent-to-agent communication.
        :param logger: Logger instance to log queue operations.
        """
        self.logger = logger or logging.getLogger(__name__)
        self.queues: Dict[str, queue.Queue] = {}
        self.lock = threading.Lock()

    def create_queue(self, agent_id: str):
        """
        Creates a message queue for a specific agent.
        :param agent_id: The unique identifier of the agent.
        """
        with self.lock:
            if agent_id not in self.queues:
                self.queues[agent_id] = queue.Queue()
                self.logger.info(f"Message queue created for agent {agent_id}")
            else:
                self.logger.warning(f"Message queue already exists for agent {agent_id}")

    def send_message(self, target_agent_id: str, message: Any):
        """
        Sends a message to a specific agent's queue.
        :param target_agent_id: The unique identifier of the target agent.
        :param message: The message to send to the target agent.
        """
        with self.lock:
            if target_agent_id in self.queues:
                self.queues[target_agent_id].put(message)
                self.logger.info(f"Message sent to agent {target_agent_id}: {message}")
            else:
                self.logger.error(f"Message queue for agent {target_agent_id} not found. Cannot send message.")

    def receive_message(self, agent_id: str, timeout: Optional[float] = None) -> Optional[Any]:
        """
        Receives a message from a specific agent's queue.
        :param agent_id: The unique identifier of the agent to receive the message.
        :param timeout: Optional timeout for receiving the message.
        :return: The received message, or None if no message is available within the timeout period.
        """
        with self.lock:
            if agent_id in self.queues:
                try:
                    message = self.queues[agent_id].get(timeout=timeout)
                    self.logger.info(f"Message received by agent {agent_id}: {message}")
                    return message
                except queue.Empty:
                    self.logger.warning(f"No message available for agent {agent_id} within timeout period.")
                    return None
            else:
                self.logger.error(f"Message queue for agent {agent_id} not found. Cannot receive message.")
                return None

    def delete_queue(self, agent_id: str):
        """
        Deletes a message queue for a specific agent.
        :param agent_id: The unique identifier of the agent.
        """
        with self.lock:
            if agent_id in self.queues:
                del self.queues[agent_id]
                self.logger.info(f"Message queue deleted for agent {agent_id}")
            else:
                self.logger.warning(f"Attempted to delete non-existent message queue for agent {agent_id}")

# Example usage
if __name__ == "__main__":
    # Set up logger
    mq_logger = logging.getLogger("message_queue")
    mq_logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    mq_logger.addHandler(console_handler)

    # Initialize MessageQueue
    message_queue = MessageQueue(logger=mq_logger)

    # Create queues for agents
    message_queue.create_queue(agent_id="agent_1")
    message_queue.create_queue(agent_id="agent_2")

    # Send messages between agents
    message_queue.send_message(target_agent_id="agent_1", message="Hello from agent_2")
    message_queue.send_message(target_agent_id="agent_2", message="Hello from agent_1")

    # Receive messages
    message_1 = message_queue.receive_message(agent_id="agent_1")
    print(f"Agent 1 received: {message_1}")

    message_2 = message_queue.receive_message(agent_id="agent_2")
    print(f"Agent 2 received: {message_2}")

    # Delete queues
    message_queue.delete_queue(agent_id="agent_1")
    message_queue.delete_queue(agent_id="agent_2")
