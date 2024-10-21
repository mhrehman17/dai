from typing import List, Dict
from core.agents.training_agent import TrainingAgent
from core.agents.identity_management import IdentityManagement
from core.orchestrator.load_balancer import LoadBalancer

class DecentralizedOrchestrator:
    def __init__(self):
        """
        Initializes the decentralized orchestrator to manage training and collaboration among multiple agents.
        """
        self.agents: Dict[str, TrainingAgent] = {}  # Registered agents
        self.identity_manager = IdentityManagement()  # Manage agent identities
        self.load_balancer = LoadBalancer()  # Load balancer to assign tasks to agents
        self.tasks: Dict[str, Dict] = {}  # Track tasks with assigned agents and their status

    def register_agent(self, agent: TrainingAgent) -> str:
        """
        Registers a training agent and assigns a unique ID to it.
        :param agent: The agent to be registered.
        :return: The unique agent ID.
        """
        agent_id = self.identity_manager.generate_agent_id()
        self.agents[agent_id] = agent
        self.load_balancer.register_agent(agent)
        print(f"Agent {agent_id} registered successfully.")
        return agent_id

    def unregister_agent(self, agent_id: str):
        """
        Unregisters a training agent from the orchestrator.
        :param agent_id: The ID of the agent to be unregistered.
        """
        if agent_id in self.agents:
            agent = self.agents.pop(agent_id)
            self.load_balancer.unregister_agent(agent_id)
            print(f"Agent {agent_id} unregistered successfully.")
        else:
            print(f"Agent {agent_id} not found for unregistration.")

    def start_task(self, task_id: str, agent_ids: List[str], description: str):
        """
        Starts a task by allocating it to specific agents.
        :param task_id: Unique identifier of the task.
        :param agent_ids: List of agent IDs to assign the task to.
        :param description: Task description.
        """
        if any(agent_id not in self.agents for agent_id in agent_ids):
            print(f"One or more agents specified for task {task_id} are not registered.")
            return

        for agent_id in agent_ids:
            agent = self.agents[agent_id]
            print(f"Orchestrator is assigning task '{task_id}' to agent {agent_id}...")
            agent.train()  # Simulate starting the training task

        # Store the task details and status
        self.tasks[task_id] = {
            "description": description,
            "agents": agent_ids,
            "status": "completed"
        }
        print(f"Task '{task_id}' completed successfully.")

    def get_task_status(self, task_id: str) -> Dict:
        """
        Retrieves the status of a specific task.
        :param task_id: Unique identifier of the task.
        :return: Dictionary containing the task status details.
        """
        return self.tasks.get(task_id, {})

    def list_agents(self) -> List[str]:
        """
        Lists all registered agents.
        :return: A list of all registered agent IDs.
        """
        return list(self.agents.keys())

# Example usage
if __name__ == "__main__":
    orchestrator = DecentralizedOrchestrator()

    # Create and register agents
    agent_1 = TrainingAgent(agent_id="agent_1", description="Training Agent 1")
    agent_2 = TrainingAgent(agent_id="agent_2", description="Training Agent 2")

    agent_1_id = orchestrator.register_agent(agent_1)
    agent_2_id = orchestrator.register_agent(agent_2)

    # Start a task with registered agents
    orchestrator.start_task(task_id="task_1", agent_ids=[agent_1_id, agent_2_id], description="Federated Training Task")

    # Retrieve task status
    task_status = orchestrator.get_task_status("task_1")
    print(f"Task Status: {task_status}")

    # List registered agents
    registered_agents = orchestrator.list_agents()
    print(f"Registered Agents: {registered_agents}")
