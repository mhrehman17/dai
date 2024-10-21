from typing import Dict, List
import random
from core.monitoring.agent_metrics import AgentMetrics
class AgentMonitor:
    def __init__(self):
        # Mock data to store metrics for each agent
        self.agent_metrics: Dict[str, AgentMetrics] = {}

    def update_metrics(self, agent_id: str):
        """
        Update the metrics of an agent, simulating changes in CPU and memory usage.
        :param agent_id: The ID of the agent to update metrics for.
        """
        if agent_id not in self.agent_metrics:
            # Initialize metrics for an agent if it does not already exist
            self.agent_metrics[agent_id] = AgentMetrics(agent_id, cpu_usage=0.0, memory_usage=0.0, tasks_completed=0)

        # Simulate CPU and memory usage with random values
        cpu_usage = random.uniform(0.1, 0.9) * 100  # CPU usage in percentage
        memory_usage = random.uniform(0.1, 0.8) * 100  # Memory usage in percentage
        tasks_completed = self.agent_metrics[agent_id].tasks_completed + 1

        # Update agent metrics
        self.agent_metrics[agent_id] = AgentMetrics(agent_id, cpu_usage, memory_usage, tasks_completed)
        print(f"Updated metrics for Agent {agent_id}: CPU Usage - {cpu_usage:.2f}%, Memory Usage - {memory_usage:.2f}%, Tasks Completed - {tasks_completed}")

    def get_agent_metrics(self, agent_id: str) -> AgentMetrics:
        """
        Get the metrics for a specific agent.
        :param agent_id: The ID of the agent.
        :return: Metrics of the agent.
        """
        if agent_id not in self.agent_metrics:
            return None
        return self.agent_metrics[agent_id]

    def get_all_metrics(self) -> List[AgentMetrics]:
        """
        Get metrics for all agents being monitored.
        :return: List of metrics for all agents.
        """
        return list(self.agent_metrics.values())