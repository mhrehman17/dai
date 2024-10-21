from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from core.monitoring.agent_monitor import AgentMonitor

# Initialize Router
router = APIRouter()

# Initialize Monitor
agent_monitor = AgentMonitor()

# Response model for agent metrics
class AgentMetricsResponse(BaseModel):
    agent_id: str
    cpu_usage: float
    memory_usage: float
    tasks_completed: int

# Endpoint to get metrics for a specific agent
@router.get("/agent-metrics/{agent_id}", response_model=AgentMetricsResponse)
async def get_agent_metrics(agent_id: str):
    metrics = agent_monitor.get_agent_metrics(agent_id)
    if not metrics:
        raise HTTPException(status_code=404, detail="Agent not found")
    return AgentMetricsResponse(agent_id=metrics.agent_id, cpu_usage=metrics.cpu_usage, memory_usage=metrics.memory_usage, tasks_completed=metrics.tasks_completed)

# Endpoint to list all agent metrics
@router.get("/all-metrics", response_model=List[AgentMetricsResponse])
async def list_all_metrics():
    metrics_list = agent_monitor.get_all_metrics()
    return [AgentMetricsResponse(agent_id=metrics.agent_id, cpu_usage=metrics.cpu_usage, memory_usage=metrics.memory_usage, tasks_completed=metrics.tasks_completed) for metrics in metrics_list]