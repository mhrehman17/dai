from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from core.agents.training_agent import TrainingAgent

# Initialize Router
router = APIRouter()

# Mock Database for Agents (In real implementation, replace with persistent storage)
agents_db = {}

# Request model for creating an agent
class CreateAgentRequest(BaseModel):
    agent_id: str
    description: str
    type: str = "training"

# Response model for retrieving an agent
class AgentResponse(BaseModel):
    agent_id: str
    description: str
    type: str
    status: str

# Endpoint to create an agent
@router.post("/create", response_model=AgentResponse)
async def create_agent(request: CreateAgentRequest):
    if request.agent_id in agents_db:
        raise HTTPException(status_code=400, detail="Agent with this ID already exists")
    
    # Create an instance of TrainingAgent (can be expanded for different agent types)
    agent = TrainingAgent(agent_id=request.agent_id, description=request.description)
    agents_db[request.agent_id] = agent
    return AgentResponse(agent_id=agent.agent_id, description=agent.description, type=request.type, status=agent.status)

# Endpoint to list all agents
@router.get("/list", response_model=List[AgentResponse])
async def list_agents():
    return [AgentResponse(agent_id=agent.agent_id, description=agent.description, type="training", status=agent.status) for agent in agents_db.values()]

# Endpoint to delete an agent
@router.delete("/delete/{agent_id}")
async def delete_agent(agent_id: str):
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")
    del agents_db[agent_id]
    return {"message": f"Agent {agent_id} has been deleted successfully"}