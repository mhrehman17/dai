from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
import logging
from core.monitoring.agent_monitor import AgentMonitor
from core.monitoring.orchestrator_monitor import OrchestratorMonitor
from core.monitoring.blockchain_monitor import BlockchainMonitor
from core_utils_identity_utils import IdentityUtils
from core.agents.identity_management import IdentityManagement

router = APIRouter()
logger = logging.getLogger("monitoring_endpoint")

# Instantiate the monitors
agent_monitor = AgentMonitor()
orchestrator_monitor = OrchestratorMonitor()
blockchain_monitor = BlockchainMonitor()

@router.get("/agent/{agent_id}")
async def get_agent_metrics(agent_id: str, current_user: Dict = Depends(IdentityManagement.get_current_user)):
    """
    Endpoint to get monitoring metrics for a specific agent.
    :param agent_id: The unique identifier of the agent to monitor.
    :param current_user: The authenticated user making the request.
    :return: Monitoring metrics for the specified agent.
    """
    try:
        metrics = agent_monitor.get_metrics(agent_id)
        if not metrics:
            raise HTTPException(status_code=404, detail="Agent not found or metrics not available")

        logger.info(f"User '{current_user['username']}' accessed metrics for agent '{agent_id}'.")
        return metrics
    except Exception as e:
        logger.error(f"Error while fetching metrics for agent '{agent_id}': {e}")
        raise HTTPException(status_code=500, detail="Unable to fetch agent metrics")

@router.get("/orchestrator")
async def get_orchestrator_metrics(current_user: Dict = Depends(IdentityManagement.get_current_user)):
    """
    Endpoint to get monitoring metrics for the orchestrator.
    :param current_user: The authenticated user making the request.
    :return: Monitoring metrics for the orchestrator.
    """
    try:
        metrics = orchestrator_monitor.get_metrics()
        logger.info(f"User '{current_user['username']}' accessed orchestrator metrics.")
        return metrics
    except Exception as e:
        logger.error(f"Error while fetching orchestrator metrics: {e}")
        raise HTTPException(status_code=500, detail="Unable to fetch orchestrator metrics")

@router.get("/blockchain")
async def get_blockchain_metrics(current_user: Dict = Depends(IdentityManagement.get_current_user)):
    """
    Endpoint to get monitoring metrics for the blockchain.
    :param current_user: The authenticated user making the request.
    :return: Monitoring metrics for the blockchain.
    """
    try:
        metrics = blockchain_monitor.get_metrics()
        logger.info(f"User '{current_user['username']}' accessed blockchain metrics.")
        return metrics
    except Exception as e:
        logger.error(f"Error while fetching blockchain metrics: {e}")
        raise HTTPException(status_code=500, detail="Unable to fetch blockchain metrics")

@router.get("/status")
async def get_system_status(current_user: Dict = Depends(IdentityManagement.get_current_user)):
    """
    Endpoint to get the overall system health status.
    :param current_user: The authenticated user making the request.
    :return: System health status including agent, orchestrator, and blockchain components.
    """
    try:
        agent_status = agent_monitor.get_all_agents_status()
        orchestrator_status = orchestrator_monitor.get_status()
        blockchain_status = blockchain_monitor.get_status()

        system_status = {
            "agent_status": agent_status,
            "orchestrator_status": orchestrator_status,
            "blockchain_status": blockchain_status
        }

        logger.info(f"User '{current_user['username']}' accessed system status.")
        return system_status
    except Exception as e:
        logger.error(f"Error while fetching system status: {e}")
        raise HTTPException(status_code=500, detail="Unable to fetch system status")

# Example integration of the router
# To be used in the main FastAPI application
if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(router, prefix="/monitoring", tags=["monitoring"])

    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8003)