// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title RewardContract
 * @dev A smart contract that manages rewards for agents based on their contributions to the decentralized AI system.
 */
contract RewardContract {
    // Mapping to track the reputation and rewards for agents
    mapping(address => uint256) public rewards;

    // Event to notify when rewards are distributed to an agent
    event RewardDistributed(address indexed agent, uint256 rewardAmount, uint256 timestamp);

    /**
     * @dev Adds rewards to an agent based on their contributions.
     * @param agent The address of the agent receiving the reward.
     * @param rewardAmount The amount of reward to be added.
     */
    function distributeReward(address agent, uint256 rewardAmount) public {
        require(agent != address(0), "Invalid agent address.");
        require(rewardAmount > 0, "Reward amount must be greater than zero.");
        
        // Add reward amount to the agent's total rewards
        rewards[agent] += rewardAmount;
        
        // Emit an event to notify listeners of the new reward distribution
        emit RewardDistributed(agent, rewardAmount, block.timestamp);
    }

    /**
     * @dev Retrieves the reward balance of a specific agent.
     * @param agent The address of the agent.
     * @return The total reward balance of the agent.
     */
    function getRewardBalance(address agent) public view returns (uint256) {
        return rewards[agent];
    }

    /**
     * @dev Allows an agent to withdraw their rewards.
     */
    function withdrawReward() public {
        uint256 rewardAmount = rewards[msg.sender];
        require(rewardAmount > 0, "No rewards available for withdrawal.");
        
        // Set the agent's reward balance to zero before transfer
        rewards[msg.sender] = 0;
        
        // Transfer the reward to the agent
        payable(msg.sender).transfer(rewardAmount);
    }

    // Function to receive Ether (to fund rewards distribution)
    receive() external payable {}
}
