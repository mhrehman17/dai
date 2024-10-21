from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
import os
import logging
from core_utils_identity_utils import IdentityUtils
from core.agents.identity_management import IdentityManagement

router = APIRouter()
logger = logging.getLogger("logs_endpoint")

# Directory path to collect logs from - in a real application, this should be configurable
LOG_DIRECTORIES = [
    "./logs/agents",
    "./logs/orchestrator",
    "./logs/blockchain"
]

@router.get("/logs")
async def get_logs(filename: str = None, current_user: Dict = Depends(IdentityManagement.get_current_user)):
    """
    Endpoint to fetch logs from various components.
    :param filename: The specific log file to fetch (optional).
    :param current_user: The authenticated user making the request.
    :return: The contents of the log file or all logs available.
    """
    logs_data = {}
    try:
        if filename:
            # If a specific file is requested, fetch it
            log_content = _read_log_file(filename)
            logs_data[filename] = log_content
        else:
            # If no filename is specified, fetch all logs
            for directory in LOG_DIRECTORIES:
                logs_data.update(_read_logs_from_directory(directory))
        logger.info(f"User '{current_user['username']}' accessed logs.")
        return logs_data
    except Exception as e:
        logger.error(f"Error while fetching logs: {e}")
        raise HTTPException(status_code=500, detail="Unable to fetch logs")


def _read_logs_from_directory(directory: str) -> Dict[str, List[str]]:
    """
    Reads all log files from the given directory.
    :param directory: Directory to read logs from.
    :return: Dictionary of log filenames and their content.
    """
    logs = {}
    if not os.path.exists(directory):
        logger.warning(f"Directory does not exist: {directory}")
        return logs

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith(".log"):
            logs[filename] = _read_log_file(file_path)
    return logs


def _read_log_file(file_path: str) -> List[str]:
    """
    Reads a specific log file.
    :param file_path: Path to the log file.
    :return: List of log lines.
    """
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file.readlines()]
    except Exception as e:
        logger.error(f"Error reading log file {file_path}: {e}")
        raise HTTPException(status_code=500, detail=f"Unable to read log file: {file_path}")


# Example integration of the router
# To be used in the main FastAPI application
if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(router, prefix="/logs", tags=["logs"])

    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8001)