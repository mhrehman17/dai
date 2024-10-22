from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

class CreateAgentRequest(BaseModel):
    agent_id: str
    description: str
    type: str = "training"

class AgentResponse(BaseModel):
    agent_id: str
    description: str
    type: str
    status: str

router = APIRouter()

# In-memory data store for agents (replace with a proper database in production)
router.db = {}

@router.post("/create", response_model=AgentResponse)
async def create_agent(request: CreateAgentRequest):
    if request.agent_id in router.db:
        raise HTTPException(status_code=400, detail="Agent with this ID already exists")
    
    agent = TrainingAgent(agent_id=request.agent_id, description=request.description)
    router.db[request.agent_id] = agent
    return AgentResponse(agent_id=agent.agent_id, description=agent.description, type=request.type, status="active")

@router.get("/list", response_model=List[AgentResponse])
async def list_agents():
    return [AgentResponse(agent_id=agent.agent_id, description=agent.description, type="training", status="active") for agent in router.db.values()]

@router.delete("/delete/{agent_id}")
async def delete_agent(agent_id: str):
    if agent_id not in router.db:
        raise HTTPException(status_code=404, detail="Agent not found")
    del router.db[agent_id]
    return {"message": f"Agent {agent_id} has been deleted successfully"}
