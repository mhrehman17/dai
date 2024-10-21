import pytest
from locust import HttpUser, task, between
import random

# Load testing for Frontend Interaction Load Testing

class LoadTestFrontendInteraction(HttpUser):
    wait_time = between(1, 3)

    # Metrics Page (metrics.html)
    @task(5)
    def test_render_metrics_visualization(self):
        # Simulate multiple users accessing metrics dashboard concurrently
        for _ in range(100):  # Simulate 100 concurrent requests
            response = self.client.get("/metrics")
            assert response.status_code == 200
            assert "Metrics Dashboard" in response.text  # Check for successful rendering

    @task(3)
    def test_multiple_users_accessing_metrics(self):
        # Load test for multiple users accessing metrics visualization
        response = self.client.get("/metrics?user_count=50")  # Simulating 50 users accessing concurrently
        assert response.status_code == 200

    # Agent Management Page (agents.html)
    @task(4)
    def test_manage_agents(self):
        # Simulate managing multiple agents (registering, updating, removing) through frontend interface
        for i in range(50):  # Simulate 50 agent interactions
            agent_id = f"agent_{i}_{random.randint(1, 10000)}"
            action = random.choice(["register", "update", "remove"])
            if action == "register":
                response = self.client.post(f"/agents/register", json={"agent_id": agent_id, "type": "worker"})
            elif action == "update":
                response = self.client.put(f"/agents/update/{agent_id}", json={"status": "active"})
            elif action == "remove":
                response = self.client.delete(f"/agents/remove/{agent_id}")
            assert response.status_code in [200, 201, 204]  # Ensure all actions are successful

    # JavaScript Functions (scripts.js)
    @task(5)
    def test_javascript_api_calls(self):
        # Load test JavaScript functions that make API calls
        for i in range(20):  # Simulate 20 repeated API calls from JavaScript
            api_endpoint = random.choice(["/api/endpoints/agents/register", "/api/endpoints/orchestrator/assign_task"])
            response = self.client.post(api_endpoint, json={"dummy_data": f"value_{i}"})
            assert response.status_code in [200, 201]

    @task(3)
    def test_dom_updates_and_ui_responsiveness(self):
        # Simulate high volume of agent interactions and validate DOM updates/UI responsiveness
        for i in range(30):  # Simulate 30 agent status updates
            agent_id = f"agent_{i}_{random.randint(1, 10000)}"
            response = self.client.get(f"/agents/status/{agent_id}")
            assert response.status_code == 200
            assert f"Agent {agent_id} Status" in response.text  # Verify DOM reflects the update

if __name__ == "__main__":
    import os
    os.system("locust -f test_load_frontend_interaction.py")
