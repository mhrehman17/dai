import pytest
from locust import HttpUser, task, between
import random

# Load testing for Federated Dashboard Load Testing

class LoadTestFederatedDashboard(HttpUser):
    wait_time = between(1, 3)

    # Metrics Visualization (start_dashboard.py)
    @task(5)
    def test_metrics_dashboard_responsiveness(self):
        # Load test for the metrics dashboard for real-time data visualization
        for i in range(50):  # Simulate 50 users accessing the dashboard
            response = self.client.get(f"/api/endpoints/dashboard/metrics?user_id=user_{i}")
            assert response.status_code == 200

    @task(4)
    def test_simultaneous_metrics_access(self):
        # Validate performance under scenarios where many users access metrics simultaneously
        for i in range(100):  # Simulate 100 users accessing distributed training metrics
            user_id = f"user_{i}_{random.randint(1, 10000)}"
            response = self.client.get(f"/api/endpoints/dashboard/distributed_metrics?user_id={user_id}")
            assert response.status_code == 200

if __name__ == "__main__":
    import os
    os.system("locust -f test_load_federated_dashboard.py")
