// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title AggregationContract
 * @dev A smart contract that manages secure aggregation of model weights from agents in a decentralized AI system.
 */
contract AggregationContract {
    // Struct to represent an agent's contribution
    struct Contribution {
        uint256 timestamp;
        bytes32 modelHash;
        uint256 weight;
    }

    // Mapping to track contributions from agents
    mapping(address => Contribution) public contributions;
    
    // Event to notify when a new contribution is made
    event ContributionAdded(address indexed agent, bytes32 modelHash, uint256 weight, uint256 timestamp);
    
    /**
     * @dev Adds a contribution from an agent.
     * @param modelHash The hash of the model contributed by the agent.
     * @param weight The weight or reputation score of the contribution.
     */
    function addContribution(bytes32 modelHash, uint256 weight) public {
        // Record the contribution in the contract's state
        contributions[msg.sender] = Contribution(block.timestamp, modelHash, weight);
        
        // Emit an event to notify listeners of the new contribution
        emit ContributionAdded(msg.sender, modelHash, weight, block.timestamp);
    }

    /**
     * @dev Gets the contribution details of a specific agent.
     * @param agent The address of the agent.
     * @return The timestamp, model hash, and weight of the contribution.
     */
    function getContribution(address agent) public view returns (uint256, bytes32, uint256) {
        Contribution memory contribution = contributions[agent];
        return (contribution.timestamp, contribution.modelHash, contribution.weight);
    }
}
