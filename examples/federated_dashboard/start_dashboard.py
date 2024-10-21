import streamlit as st
import requests
import time

# Constants for the metrics API
METRICS_API_BASE_URL = "http://localhost:8000/metrics"
REFRESH_INTERVAL = 10  # Refresh interval in seconds

# Function to fetch metrics from the API
def fetch_metrics(agent_id):
    try:
        response = requests.get(f"{METRICS_API_BASE_URL}/{agent_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch metrics for {agent_id}: {e}")
        return None

# Function to display metrics for a given agent
def display_agent_metrics(agent_id, metrics):
    st.subheader(f"Metrics for Agent: {agent_id}")
    st.metric(label="CPU Usage (%)", value=f"{metrics['cpu_usage']:.2f}")
    st.metric(label="Memory Usage (%)", value=f"{metrics['memory_usage']:.2f}")
    st.metric(label="Training Loss", value=f"{metrics['training_loss']:.4f}")

# Main dashboard function
def start_dashboard():
    st.title("Federated Dashboard - Agent Metrics Monitoring")

    # Input for agent ID
    agent_id = st.sidebar.text_input("Enter Agent ID", value="agent_1")

    # Button to trigger refresh
    refresh_button = st.sidebar.button("Refresh Now")

    # Auto-refresh setting
    auto_refresh = st.sidebar.checkbox("Auto Refresh", value=True)

    # Metrics Display Loop
    last_refresh_time = 0
    while True:
        current_time = time.time()
        if refresh_button or (auto_refresh and current_time - last_refresh_time >= REFRESH_INTERVAL):
            metrics = fetch_metrics(agent_id)
            if metrics:
                st.empty()  # Clear the old output
                display_agent_metrics(agent_id, metrics)
            last_refresh_time = current_time

        # Wait before refreshing to prevent excessive looping
        time.sleep(REFRESH_INTERVAL)

if __name__ == "__main__":
    start_dashboard()
