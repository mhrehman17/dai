import logging
from typing import Dict, List

class AccessPolicy:
    def __init__(self, logger: logging.Logger = None):
        """
        Initializes an access policy manager to enforce communication policies.
        :param logger: Logger instance to log policy enforcement details.
        """
        self.logger = logger or logging.getLogger(__name__)
        self.access_policies: Dict[str, List[str]] = {}

    def define_policy(self, agent_id: str, allowed_peers: List[str]):
        """
        Defines the access policy for a given agent, specifying the peers it can communicate with.
        :param agent_id: The unique identifier for the agent.
        :param allowed_peers: A list of peer identifiers that the agent is allowed to communicate with.
        """
        self.access_policies[agent_id] = allowed_peers
        self.logger.info(f"Access policy defined for agent '{agent_id}': Allowed peers: {allowed_peers}")

    def can_communicate(self, agent_id: str, target_peer_id: str) -> bool:
        """
        Checks if communication is allowed between the given agent and the target peer.
        :param agent_id: The unique identifier for the requesting agent.
        :param target_peer_id: The unique identifier for the target peer.
        :return: True if communication is allowed, False otherwise.
        """
        allowed_peers = self.access_policies.get(agent_id, [])
        if target_peer_id in allowed_peers:
            self.logger.info(f"Communication allowed between agent '{agent_id}' and target peer '{target_peer_id}'")
            return True
        else:
            self.logger.info(f"Communication denied between agent '{agent_id}' and target peer '{target_peer_id}'")
            return False

    def revoke_policy(self, agent_id: str):
        """
        Revokes the access policy for a given agent.
        :param agent_id: The unique identifier for the agent.
        """
        if agent_id in self.access_policies:
            del self.access_policies[agent_id]
            self.logger.info(f"Access policy revoked for agent '{agent_id}'")
        else:
            self.logger.info(f"No access policy found for agent '{agent_id}', nothing to revoke.")

    def update_policy(self, agent_id: str, allowed_peers: List[str]):
        """
        Updates the access policy for a given agent.
        :param agent_id: The unique identifier for the agent.
        :param allowed_peers: A new list of peer identifiers that the agent is allowed to communicate with.
        """
        if agent_id in self.access_policies:
            self.access_policies[agent_id] = allowed_peers
            self.logger.info(f"Access policy updated for agent '{agent_id}': New allowed peers: {allowed_peers}")
        else:
            # Define the policy instead of issuing a warning if it doesn't exist.
            self.define_policy(agent_id, allowed_peers)
            self.logger.info(f"Access policy did not exist for agent '{agent_id}', a new policy has been defined.")

# Example usage
if __name__ == "__main__":
    # Set up logger
    access_policy_logger = logging.getLogger("access_policy")
    access_policy_logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    access_policy_logger.addHandler(console_handler)

    # Initialize AccessPolicy
    access_policy = AccessPolicy(logger=access_policy_logger)

    # Define access policies for agents
    access_policy.define_policy(agent_id="agent_1", allowed_peers=["agent_2", "agent_3"])
    access_policy.define_policy(agent_id="agent_2", allowed_peers=["agent_1"])

    # Check communication permissions
    access_policy.can_communicate(agent_id="agent_1", target_peer_id="agent_2")
    access_policy.can_communicate(agent_id="agent_1", target_peer_id="agent_4")

    # Update policy for an agent
    access_policy.update_policy(agent_id="agent_1", allowed_peers=["agent_4"])
    access_policy.can_communicate(agent_id="agent_1", target_peer_id="agent_4")

    # Revoke access policy for an agent
    access_policy.revoke_policy(agent_id="agent_1")
    access_policy.can_communicate(agent_id="agent_1", target_peer_id="agent_2")
