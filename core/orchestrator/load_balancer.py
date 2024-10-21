import random
from typing import Dict, List
from core.agents.training_agent import TrainingAgent

class LoadBalancer:
    def __init__(self):
        """
        Initializes the load balancer to manage task distribution among agents.
        """
        self.agents: Dict[str, TrainingAgent] = {}  # Registered agents

    def register_agent(self, agent: TrainingAgent):
        """
        Registers an agent to the load balancer.
        :param agent: The agent to be registered.
        """
        if agent.agent_id not in self.agents:
            self.agents[agent.agent_id] = agent
            print(f"Agent {agent.agent_id} registered with load balancer.")

    def unregister_agent(self, agent_id: str):
        """
        Unregisters an agent from the load balancer.
        :param agent_id: The ID of the agent to be unregistered.
        """
        if agent_id in self.agents:
            del self.agents[agent_id]
            print(f"Agent {agent_id} unregistered from load balancer.")

    def allocate_task(self, task_id: str) -> str:
        """
        Allocates a task to an available agent based on a load balancing strategy.
        :param task_id: Unique identifier for the task to be allocated.
        :return: The agent ID of the selected agent.
        """
        if not self.agents:
            raise ValueError("No agents available for task allocation.")

        # Implement a simple load balancing strategy: random selection
        selected_agent_id = random.choice(list(self.agents.keys()))
        print(f"Task '{task_id}' has been allocated to agent {selected_agent_id}.")
        return selected_agent_id

    def allocate_task_round_robin(self, task_id: str, current_index: int = 0) -> str:
        """
        Allocates a task using a round-robin strategy.
        :param task_id: Unique identifier for the task to be allocated.
        :param current_index: The index of the last agent allocated.
        :return: The agent ID of the selected agent.
        """
        if not self.agents:
            raise ValueError("No agents available for task allocation.")

        agent_ids = list(self.agents.keys())
        selected_agent_id = agent_ids[current_index % len(agent_ids)]
        print(f"Task '{task_id}' has been allocated to agent {selected_agent_id} using round-robin strategy.")
        return selected_agent_id

    def list_agents(self) -> List[str]:
        """
        Lists all registered agents.
        :return: A list of registered agent IDs.
        """
        return list(self.agents.keys())

# Example usage
if __name__ == "__main__":
    load_balancer = LoadBalancer()

    # Create and register agents
    agent_1 = TrainingAgent(agent_id="agent_1", description="Training Agent 1")
    agent_2 = TrainingAgent(agent_id="agent_2", description="Training Agent 2")
    agent_3 = TrainingAgent(agent_id="agent_3", description="Training Agent 3")

    load_balancer.register_agent(agent_1)
    load_balancer.register_agent(agent_2)
    load_balancer.register_agent(agent_3)

    # Allocate tasks
    load_balancer.allocate_task("task_1")
    load_balancer.allocate_task_round_robin("task_2", current_index=1)

    # List registered agents
    registered_agents = load_balancer.list_agents()
    print(f"Registered Agents: {registered_agents}")
