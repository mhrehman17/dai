###the code needs massive improvements.

import streamlit as st
import pandas as pd
import requests
from typing import List, Tuple
import time

class MonitoringDashboard:
    def __init__(self, nodes: List[Tuple[str, int]], polling_interval: int = 10):
        """
        Initializes the MonitoringDashboard for displaying blockchain metrics.
        :param nodes: A list of node addresses in the format (host, port).
        :param polling_interval: The time interval (in seconds) between polling each node.
        """
        self.nodes = nodes
        self.polling_interval = polling_interval

    def fetch_node_status(self, host: str, port: int) -> dict:
        """
        Fetches the status of a blockchain node.
        :param host: The hostname or IP address of the node.
        :param port: The port of the node.
        :return: A dictionary containing the node's status information or error.
        """
        try:
            url = f"http://{host}:{port}/status"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status code {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def fetch_node_metrics(self, host: str, port: int, metrics_endpoint: str = '/metrics') -> dict:
        """
        Fetches detailed metrics of a blockchain node.
        :param host: The hostname or IP address of the node.
        :param port: The port of the node.
        :param metrics_endpoint: The endpoint to fetch metrics.
        :return: A dictionary containing the node's metrics information or error.
        """
        try:
            url = f"http://{host}:{port}{metrics_endpoint}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status code {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def run_dashboard(self):
        """
        Runs the monitoring dashboard using Streamlit.
        """
        st.title("Blockchain Monitoring Dashboard")

        # Fetch and display node statuses
        st.write("### Node Statuses")
        status_data = []
        for host, port in self.nodes:
            node_status = self.fetch_node_status(host, port)
            status_data.append({
                "Node": f"{host}:{port}",
                "Status": node_status.get('status', 'Error'),
                "Error": node_status.get('error', 'None')
            })
        df_status = pd.DataFrame(status_data)
        st.table(df_status)

        # Fetch and display node metrics
        st.write("### Node Metrics")
        metrics_data = []
        for host, port in self.nodes:
            metrics = self.fetch_node_metrics(host, port)
            metrics_data.append({
                "Node": f"{host}:{port}",
                "Metrics": metrics if "error" not in metrics else "Error",
                "Error": metrics.get('error', 'None')
            })
        df_metrics = pd.DataFrame(metrics_data)
        st.table(df_metrics)

        # Automatically refresh the dashboard
        st.write(f"### Dashboard is updating every {self.polling_interval} seconds.")
        # Using time.sleep() to refresh after polling_interval
        time.sleep(self.polling_interval)
        st.rerun()  # Forces the app to rerun and refresh


# Example usage
if __name__ == "__main__":
    # Example node addresses
    nodes = [
        ("localhost", 8545),
        ("localhost", 8546)
    ]

    # Initialize and run the dashboard
    dashboard = MonitoringDashboard(nodes=nodes, polling_interval=15)
    dashboard.run_dashboard()
