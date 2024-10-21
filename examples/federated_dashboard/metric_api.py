from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import random
import logging

# Initialize FastAPI app and logging
app = FastAPI()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MetricsAPI")

# Mock data store for agent metrics
mock_metrics_db: Dict[str, Dict[str, float]] = {
    "agent_1": {"cpu_usage": 45.0, "memory_usage": 30.5, "training_loss": 0.15},
    "agent_2": {"cpu_usage": 50.3, "memory_usage": 40.7, "training_loss": 0.20},
    "agent_3": {"cpu_usage": 20.7, "memory_usage": 25.0, "training_loss": 0.10},
}

# Pydantic model to describe the metrics data
class Metrics(BaseModel):
    cpu_usage: float
    memory_usage: float
    training_loss: float

# Endpoint to get metrics for a specific agent
@app.get("/metrics/{agent_id}", response_model=Metrics)
async def get_metrics(agent_id: str):
    """
    Get metrics for a specific agent by its ID.
    """
    logger.info(f"Fetching metrics for agent: {agent_id}")
    if agent_id not in mock_metrics_db:
        logger.error(f"Agent {agent_id} not found in the metrics database.")
        raise HTTPException(status_code=404, detail="Agent not found")
    return mock_metrics_db[agent_id]

# Endpoint to update metrics for a specific agent
@app.put("/metrics/{agent_id}")
async def update_metrics(agent_id: str, metrics: Metrics):
    """
    Update metrics for a specific agent by its ID.
    """
    logger.info(f"Updating metrics for agent: {agent_id}")
    if agent_id not in mock_metrics_db:
        logger.error(f"Agent {agent_id} not found in the metrics database.")
        raise HTTPException(status_code=404, detail="Agent not found")
    mock_metrics_db[agent_id] = metrics.dict()
    logger.info(f"Metrics updated successfully for agent: {agent_id}")
    return {"message": "Metrics updated successfully."}

# Endpoint to get metrics for all agents
@app.get("/metrics", response_model=Dict[str, Metrics])
async def get_all_metrics():
    """
    Get metrics for all agents.
    """
    logger.info("Fetching metrics for all agents.")
    return mock_metrics_db

# Endpoint to simulate metrics (for testing purposes)
@app.post("/metrics/simulate/{agent_id}")
async def simulate_metrics(agent_id: str):
    """
    Simulate updating metrics with random values for a specific agent.
    """
    logger.info(f"Simulating metrics update for agent: {agent_id}")
    if agent_id not in mock_metrics_db:
        logger.error(f"Agent {agent_id} not found in the metrics database.")
        raise HTTPException(status_code=404, detail="Agent not found")
    mock_metrics_db[agent_id] = {
        "cpu_usage": random.uniform(10.0, 90.0),
        "memory_usage": random.uniform(10.0, 80.0),
        "training_loss": random.uniform(0.05, 0.5),
    }
    logger.info(f"Metrics simulated and updated for agent: {agent_id}")
    return {"message": "Metrics simulated and updated successfully."}
