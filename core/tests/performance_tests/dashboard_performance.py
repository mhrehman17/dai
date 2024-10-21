import pytest
from locust import User, task, between
import random

# Performance testing for Federated Dashboard Performance Testing

class PerformanceTestFederatedDashboard(User):
    wait_time = between(1, 3)

    # Metrics Visualization (start_dashboard.py)
    @task(5)
    def test_metrics_visualization_performance(self):
        # Evaluate the performance of the metrics visualization dashboard for real-time federated learning data
        for i in range(100):  # Simulate requests to visualize metrics in real-time
            response = self.client.get(f"/api/endpoints/dashboard/metrics?session_id=training_session_{i}")
            assert response.status_code == 200

    @task(4)
    def test_dashboard_responsiveness_under_concurrent_users(self):
        # Test the system's responsiveness when accessed by many concurrent users
        for i in range(150):  # Simulate concurrent users accessing the dashboard
            user_id = f"user_{i}_{random.randint(1, 10000)}"
            response = self.client.get(f"/api/endpoints/dashboard/view?user_id={user_id}")
            assert response.status_code == 200

if __name__ == "__main__":
    import os
    os.system("locust -f test_performance_federated_dashboard.py")
