import pytest
from locust import HttpUser, task, between
import random

# Load testing for Blockchain and Ledger Load Testing

class LoadTestBlockchainLedger(HttpUser):
    wait_time = between(1, 3)

    # Blockchain Ledger (blockchain_ledger.py)
    @task(5)
    def test_ledger_transactions_concurrently(self):
        # Load test for multiple agents writing to the blockchain simultaneously
        for i in range(50):  # Simulate 50 concurrent transactions
            transaction_id = f"txn_{i}_{random.randint(1, 10000)}"
            response = self.client.post(f"/api/endpoints/ledger/transaction", json={"transaction_id": transaction_id, "amount": random.randint(1, 1000)})
            assert response.status_code == 200

    @task(4)
    def test_consensus_mechanism_under_load(self):
        # Test the performance of the consensus mechanism under rapid, concurrent updates
        for i in range(20):  # Simulate 20 concurrent consensus validations
            block_id = f"block_{i}_{random.randint(1, 10000)}"
            response = self.client.post(f"/api/endpoints/ledger/consensus", json={"block_id": block_id})
            assert response.status_code == 200

    # Agent Registration on Blockchain (registration_contract.sol)
    @task(5)
    def test_agent_registration_on_blockchain(self):
        # Validate registration of hundreds of agents concurrently
        for i in range(100):  # Simulate registration of 100 agents
            agent_id = f"agent_{i}_{random.randint(1, 10000)}"
            response = self.client.post(f"/api/endpoints/blockchain/register_agent", json={"agent_id": agent_id})
            assert response.status_code in [200, 201]

    @task(3)
    def test_reward_distribution_contract(self):
        # Test reward distribution when multiple agents complete training tasks simultaneously
        for i in range(30):  # Simulate reward distribution for 30 agents
            agent_id = f"agent_{i}_{random.randint(1, 10000)}"
            response = self.client.post(f"/api/endpoints/blockchain/distribute_reward", json={"agent_id": agent_id, "reward_amount": random.randint(50, 200)})
            assert response.status_code == 200

if __name__ == "__main__":
    import os
    os.system("locust -f test_load_blockchain_ledger.py")
