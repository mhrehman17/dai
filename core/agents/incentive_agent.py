from typing import Optional, Dict
import random
import time
from core.agents.collaboration_agent import CollaborationAgent

class IncentiveAgent(CollaborationAgent):
    def __init__(self, agent_id: str, description: str):
        """
        Initializes an incentive-based agent capable of rewarding peers based on their contributions.
        :param agent_id: Unique identifier for the agent.
        :param description: Description of the agent.
        """
        super().__init__(agent_id, description)
        self.reputation_scores: Dict[str, float] = {}  # Stores reputation scores for peers

    def add_peer(self, peer: CollaborationAgent):
        """
        Adds a peer agent and initializes its reputation score.
        :param peer: The peer agent to add.
        """
        super().add_peer(peer)
        self.reputation_scores[peer.agent_id] = 1.0  # Start with a neutral reputation score
        print(f"Initialized reputation for peer {peer.agent_id}.")

    def reward_peer(self, peer_id: str, reward: float):
        """
        Rewards a peer by increasing its reputation score.
        :param peer_id: ID of the peer agent to reward.
        :param reward: Reward value to increase the reputation score.
        """
        if peer_id in self.reputation_scores:
            self.reputation_scores[peer_id] += reward
            print(f"Agent {self.agent_id} rewarded peer {peer_id} with {reward:.2f} points. New reputation: {self.reputation_scores[peer_id]:.2f}")
        else:
            print(f"Agent {self.agent_id} could not find peer {peer_id} to reward.")

    def penalize_peer(self, peer_id: str, penalty: float):
        """
        Penalizes a peer by decreasing its reputation score.
        :param peer_id: ID of the peer agent to penalize.
        :param penalty: Penalty value to decrease the reputation score.
        """
        if peer_id in self.reputation_scores:
            self.reputation_scores[peer_id] = max(0.0, self.reputation_scores[peer_id] - penalty)
            print(f"Agent {self.agent_id} penalized peer {peer_id} with {penalty:.2f} points. New reputation: {self.reputation_scores[peer_id]:.2f}")
        else:
            print(f"Agent {self.agent_id} could not find peer {peer_id} to penalize.")

    def collaborate(self):
        """
        Overrides the collaborate method to reward peers based on successful collaboration.
        """
        if not self.peers:
            print(f"Agent {self.agent_id} has no peers to collaborate with.")
            return

        print(f"Agent {self.agent_id} is collaborating with peers...")
        for peer in self.peers:
            print(f"Agent {self.agent_id} is collaborating with peer {peer.agent_id}.")
            # Simulate successful collaboration and reward peers
            success = random.choice([True, False])
            if success:
                reward = random.uniform(0.1, 0.5)
                self.reward_peer(peer.agent_id, reward)
            else:
                penalty = random.uniform(0.05, 0.2)
                self.penalize_peer(peer.agent_id, penalty)
            time.sleep(random.uniform(0.5, 1.0))
        print(f"Agent {self.agent_id} completed collaboration with peers.")

# Example usage
if __name__ == "__main__":
    agent_1 = IncentiveAgent(agent_id="agent_1", description="Incentive agent 1 for rewarding contributions")
    agent_2 = IncentiveAgent(agent_id="agent_2", description="Incentive agent 2 for rewarding contributions")
    agent_3 = IncentiveAgent(agent_id="agent_3", description="Incentive agent 3 for rewarding contributions")

    # Add peers
    agent_1.add_peer(agent_2)
    agent_1.add_peer(agent_3)

    # Train, collaborate, and reward peers
    agent_1.train()
    print(f"Agent Status: {agent_1.get_status()}")
