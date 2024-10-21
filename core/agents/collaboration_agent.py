from typing import Optional, List
import random
import time
from core.agents.training_agent import TrainingAgent

class CollaborationAgent(TrainingAgent):
    def __init__(self, agent_id: str, description: str):
        """
        Initializes a collaboration agent capable of communicating with other agents to share learning updates.
        :param agent_id: Unique identifier for the agent.
        :param description: Description of the agent.
        """
        super().__init__(agent_id, description)
        self.peers: List[TrainingAgent] = []  # List of peer agents to collaborate with

    def add_peer(self, peer: TrainingAgent):
        """
        Adds a peer agent to the collaboration network.
        :param peer: The peer agent to add.
        """
        if peer.agent_id not in [p.agent_id for p in self.peers]:
            self.peers.append(peer)
            print(f"Agent {self.agent_id} added peer {peer.agent_id} to its collaboration network.")

    def remove_peer(self, peer_id: str):
        """
        Removes a peer agent from the collaboration network by agent ID.
        :param peer_id: The ID of the peer agent to remove.
        """
        self.peers = [peer for peer in self.peers if peer.agent_id != peer_id]
        print(f"Agent {self.agent_id} removed peer {peer_id} from its collaboration network.")

    def collaborate(self):
        """
        Collaborates with peers by sharing learning updates.
        """
        if not self.peers:
            print(f"Agent {self.agent_id} has no peers to collaborate with.")
            return

        # Simulate sharing updates with peers
        print(f"Agent {self.agent_id} is collaborating with peers...")
        for peer in self.peers:
            print(f"Agent {self.agent_id} is sending updates to peer {peer.agent_id}.")
            # Simulated data exchange or aggregation step here
            time.sleep(random.uniform(0.5, 1.0))
        print(f"Agent {self.agent_id} completed collaboration with peers.")

    def train(self, data: Optional[list] = None):
        """
        Overrides the base train method to include collaboration after training.
        :param data: Optional dataset to be used in training.
        """
        self.status = "training"
        print(f"Agent {self.agent_id} is starting training...")
        training_time = random.uniform(1.0, 5.0)
        time.sleep(training_time)
        print(f"Training complete for Agent {self.agent_id} in {training_time:.2f} seconds.")
        self.status = "collaborating"
        self.collaborate()
        self.status = "idle"

# Example usage
if __name__ == "__main__":
    agent_1 = CollaborationAgent(agent_id="agent_1", description="Collaboration agent 1 for federated learning")
    agent_2 = CollaborationAgent(agent_id="agent_2", description="Collaboration agent 2 for federated learning")
    agent_3 = CollaborationAgent(agent_id="agent_3", description="Collaboration agent 3 for federated learning")

    # Add peers
    agent_1.add_peer(agent_2)
    agent_1.add_peer(agent_3)
    agent_2.add_peer(agent_1)
    agent_3.add_peer(agent_1)

    # Train and collaborate
    agent_1.train()
    print(f"Agent Status: {agent_1.get_status()}")