from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from core.orchestrator.decentralized_orchestrator import DecentralizedOrchestrator

# Initialize Router and Orchestrator with type hints
router = APIRouter()
orchestrator: DecentralizedOrchestrator = DecentralizedOrchestrator()

class StartTaskRequest(BaseModel):
    task_id: str
    agent_ids: List[str]
    description: str

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    description: str

async def start_task(request: StartTaskRequest) -> TaskStatusResponse:
    try:
        orchestrator.start_task(task_id=request.task_id, agent_ids=request.agent_ids, description=request.description)
        return TaskStatusResponse(task_id=request.task_id, status="Task Started", description=request.description)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_task_status(task_id: str) -> TaskStatusResponse:
    status = orchestrator.get_task_status(task_id)
    if not status:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskStatusResponse(task_id=task_id, status=status.status, description=status.description)

# Expose start-task and get-task-status endpoints on the router
router.post("/start-task", response_model=TaskStatusResponse)(start_task)
router.get("/task-status/{task_id}", response_model=TaskStatusResponse)(get_task_status)
