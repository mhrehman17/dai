from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from core.orchestrator.decentralized_orchestrator import DecentralizedOrchestrator

# Initialize Router
router = APIRouter()

# Initialize Orchestrator
orchestrator = DecentralizedOrchestrator()

# Request model for starting a task
class StartTaskRequest(BaseModel):
    task_id: str
    agent_ids: List[str]
    description: str

# Response model for task status
class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    description: str

# Endpoint to start a task using multiple agents
@router.post("/start-task", response_model=TaskStatusResponse)
async def start_task(request: StartTaskRequest):
    try:
        orchestrator.start_task(task_id=request.task_id, agent_ids=request.agent_ids, description=request.description)
        return TaskStatusResponse(task_id=request.task_id, status="Task Started", description=request.description)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint to get the status of a task
@router.get("/task-status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    status = orchestrator.get_task_status(task_id)
    if not status:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskStatusResponse(task_id=task_id, status=status.status, description=status.description)