// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title RegistrationContract
 * @dev A smart contract that manages the registration of agents in a decentralized AI system.
 */
contract RegistrationContract {
    // Struct to represent an agent
    struct Agent {
        address agentAddress;
        string agentName;
        uint256 registrationTimestamp;
        bool isRegistered;
    }

    // Mapping to track registered agents
    mapping(address => Agent) public agents;
    
    // Event to notify when a new agent registers
    event AgentRegistered(address indexed agentAddress, string agentName, uint256 timestamp);

    // Modifier to check if the agent is already registered
    modifier notRegistered() {
        require(!agents[msg.sender].isRegistered, "Agent is already registered.");
        _;
    }

    /**
     * @dev Registers a new agent in the decentralized AI system.
     * @param agentName The name of the agent being registered.
     */
    function registerAgent(string memory agentName) public notRegistered {
        agents[msg.sender] = Agent({
            agentAddress: msg.sender,
            agentName: agentName,
            registrationTimestamp: block.timestamp,
            isRegistered: true
        });
        
        emit AgentRegistered(msg.sender, agentName, block.timestamp);
    }

    /**
     * @dev Retrieves details of a registered agent.
     * @param agentAddress The address of the agent to retrieve details for.
     * @return The agent's address, name, registration timestamp, and registration status.
     */
    function getAgentDetails(address agentAddress) public view returns (address, string memory, uint256, bool) {
        Agent memory agent = agents[agentAddress];
        return (agent.agentAddress, agent.agentName, agent.registrationTimestamp, agent.isRegistered);
    }

    /**
     * @dev Checks if an agent is registered.
     * @param agentAddress The address of the agent to check.
     * @return True if the agent is registered, otherwise false.
     */
    function isAgentRegistered(address agentAddress) public view returns (bool) {
        return agents[agentAddress].isRegistered;
    }
}
