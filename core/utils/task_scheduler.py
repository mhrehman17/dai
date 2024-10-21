import logging
import threading
import time
from typing import List, Dict, Callable, Optional

class TaskScheduler:
    def __init__(self, nodes: List[Dict[str, str]], logger: Optional[logging.Logger] = None):
        """
        Initializes the TaskScheduler for managing task distribution across nodes.
        :param nodes: A list of nodes containing information such as host and identifier.
        :param logger: Logger instance to log task scheduling activities.
        """
        self.nodes = nodes
        self.task_queue = []
        self.node_status = {node['id']: "available" for node in nodes}
        self.logger = logger or logging.getLogger(__name__)
        self.lock = threading.Lock()
        self.running = False

    def start_scheduler(self):
        """
        Starts the task scheduler in a separate thread.
        """
        self.running = True
        threading.Thread(target=self._run_scheduler, daemon=True).start()
        self.logger.info("Task scheduler started.")

    def stop_scheduler(self):
        """
        Stops the task scheduler.
        """
        self.running = False
        self.logger.info("Task scheduler stopped.")

    def add_task(self, task: Callable, task_id: str):
        """
        Adds a task to the task queue.
        :param task: A callable representing the task to be performed.
        :param task_id: A unique identifier for the task.
        """
        with self.lock:
            self.task_queue.append((task, task_id))
            self.logger.info(f"Task {task_id} added to the queue.")

    def _run_scheduler(self):
        """
        Runs the task scheduler to assign tasks to available nodes.
        """
        while self.running:
            with self.lock:
                if self.task_queue:
                    # Find an available node to assign a task
                    for node_id, status in self.node_status.items():
                        if status == "available" and self.task_queue:
                            task, task_id = self.task_queue.pop(0)
                            self.node_status[node_id] = "busy"
                            self._assign_task(task, task_id, node_id)
                            break
            time.sleep(1)  # Short delay to avoid excessive CPU usage

    def _assign_task(self, task: Callable, task_id: str, node_id: str):
        """
        Assigns a task to a node and manages task execution.
        :param task: The task to be assigned.
        :param task_id: The unique identifier of the task.
        :param node_id: The ID of the node the task is assigned to.
        """
        try:
            self.logger.info(f"Assigning task {task_id} to node {node_id}.")
            # Simulate task execution in a separate thread
            threading.Thread(target=self._execute_task, args=(task, task_id, node_id), daemon=True).start()
        except Exception as e:
            self.logger.error(f"Failed to assign task {task_id} to node {node_id}: {e}")
            self.node_status[node_id] = "available"

    def _execute_task(self, task: Callable, task_id: str, node_id: str):
        """
        Executes the assigned task and updates the node status.
        :param task: The task to be executed.
        :param task_id: The unique identifier of the task.
        :param node_id: The ID of the node executing the task.
        """
        try:
            task()  # Execute the task
            self.logger.info(f"Task {task_id} completed successfully on node {node_id}.")
        except Exception as e:
            self.logger.error(f"Error executing task {task_id} on node {node_id}: {e}")
        finally:
            self.node_status[node_id] = "available"

# Example usage
if __name__ == "__main__":
    # Set up logger
    scheduler_logger = logging.getLogger("task_scheduler")
    scheduler_logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    scheduler_logger.addHandler(console_handler)

    # Initialize TaskScheduler
    nodes_info = [
        {"host": "localhost", "id": "node_1"},
        {"host": "localhost", "id": "node_2"},
        {"host": "localhost", "id": "node_3"}
    ]
    task_scheduler = TaskScheduler(nodes=nodes_info, logger=scheduler_logger)

    # Define a sample task
    def sample_task():
        time.sleep(2)  # Simulate task duration
        print("Task executed.")

    # Start the task scheduler
    task_scheduler.start_scheduler()

    # Add tasks to the scheduler
    task_scheduler.add_task(sample_task, "task_1")
    task_scheduler.add_task(sample_task, "task_2")
    task_scheduler.add_task(sample_task, "task_3")

    # Allow some time for demonstration purposes
    try:
        time.sleep(20)  # Keep running for 20 seconds to simulate task scheduling
    finally:
        task_scheduler.stop_scheduler()
