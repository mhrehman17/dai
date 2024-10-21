from typing import List, Dict
from core.agents.training_agent import TrainingAgent
from core.agents.identity_management import IdentityManagement
from core.orchestrator.decentralized_orchestrator import DecentralizedOrchestrator

class HierarchicalOrchestrator:
    def __init__(self):
        """
        Initializes the hierarchical orchestrator to manage both edge and cloud agents in a coordinated manner.
        """
        self.edge_orchestrators: List[DecentralizedOrchestrator] = []  # Edge level orchestrators
        self.cloud_agents: Dict[str, TrainingAgent] = {}  # Cloud-based agents
        self.identity_manager = IdentityManagement()  # Manage agent identities
        self.tasks: Dict[str, Dict] = {}  # Track tasks with assigned agents and their status

    def add_edge_orchestrator(self, orchestrator: DecentralizedOrchestrator):
        """
        Adds an edge orchestrator to the hierarchical system.
        :param orchestrator: The edge orchestrator to add.
        """
        self.edge_orchestrators.append(orchestrator)
        print(f"Added edge orchestrator to the hierarchical system.")

    def register_cloud_agent(self, agent: TrainingAgent) -> str:
        """
        Registers a cloud agent to the orchestrator system.
        :param agent: The cloud agent to be registered.
        :return: The unique agent ID.
        """
        agent_id = self.identity_manager.generate_agent_id()
        self.cloud_agents[agent_id] = agent
        print(f"Cloud Agent {agent_id} registered successfully.")
        return agent_id

    def unregister_cloud_agent(self, agent_id: str):
        """
        Unregisters a cloud agent from the orchestrator system.
        :param agent_id: The ID of the cloud agent to be unregistered.
        """
        if agent_id in self.cloud_agents:
            del self.cloud_agents[agent_id]
            print(f"Cloud Agent {agent_id} unregistered successfully.")
        else:
            print(f"Cloud Agent {agent_id} not found for unregistration.")

    def start_task(self, task_id: str, description: str, agent_ids: List[str] = None):
        """
        Starts a task by allocating it to cloud agents or coordinating through edge orchestrators.
        :param task_id: Unique identifier of the task.
        :param description: Task description.
        :param agent_ids: List of cloud agent IDs to assign the task to (optional).
        """
        if agent_ids:
            # Allocate task to cloud agents if specified
            for agent_id in agent_ids:
                if agent_id in self.cloud_agents:
                    agent = self.cloud_agents[agent_id]
                    print(f"Hierarchical orchestrator assigning task '{task_id}' to cloud agent {agent_id}...")
                    agent.train()
                else:
                    print(f"Cloud agent {agent_id} is not registered.")
        else:
            # Allocate task to all edge orchestrators
            for edge_orchestrator in self.edge_orchestrators:
                print(f"Hierarchical orchestrator delegating task '{task_id}' to an edge orchestrator...")
                # For simplicity, delegate to the first two agents managed by the edge orchestrator
                agent_list = edge_orchestrator.list_agents()[:2]
                edge_orchestrator.start_task(task_id, agent_list, description)

        # Store the task details and status
        self.tasks[task_id] = {
            "description": description,
            "agents": agent_ids if agent_ids else ["edge_orchestrators"],
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

    def list_cloud_agents(self) -> List[str]:
        """
        Lists all registered cloud agents.
        :return: A list of all registered cloud agent IDs.
        """
        return list(self.cloud_agents.keys())

# Example usage
if __name__ == "__main__":
    hierarchical_orchestrator = HierarchicalOrchestrator()

    # Create edge orchestrators and add them to the hierarchical orchestrator
    edge_orchestrator_1 = DecentralizedOrchestrator()
    edge_orchestrator_2 = DecentralizedOrchestrator()
    hierarchical_orchestrator.add_edge_orchestrator(edge_orchestrator_1)
    hierarchical_orchestrator.add_edge_orchestrator(edge_orchestrator_2)

    # Create and register cloud agents
    cloud_agent_1 = TrainingAgent(agent_id="cloud_agent_1", description="Cloud Training Agent 1")
    cloud_agent_2 = TrainingAgent(agent_id="cloud_agent_2", description="Cloud Training Agent 2")

    cloud_agent_1_id = hierarchical_orchestrator.register_cloud_agent(cloud_agent_1)
    cloud_agent_2_id = hierarchical_orchestrator.register_cloud_agent(cloud_agent_2)

    # Start a task on cloud agents
    hierarchical_orchestrator.start_task(task_id="task_cloud", description="Training on cloud agents", agent_ids=[cloud_agent_1_id, cloud_agent_2_id])

    # Start a task on edge orchestrators
    hierarchical_orchestrator.start_task(task_id="task_edge", description="Edge-level federated training task")

    # Retrieve task status
    task_status = hierarchical_orchestrator.get_task_status("task_cloud")
    print(f"Task Status: {task_status}")

    # List registered cloud agents
    registered_cloud_agents = hierarchical_orchestrator.list_cloud_agents()
    print(f"Registered Cloud Agents: {registered_cloud_agents}")
