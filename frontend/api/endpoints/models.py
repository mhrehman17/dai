from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import List, Dict, Optional
import logging
import os
import shutil
from datetime import datetime
from core.models.registry.model_registry import ModelRegistry
from core_utils_identity_utils import IdentityUtils
from core.agents.identity_management import IdentityManagement

router = APIRouter()
logger = logging.getLogger("models_endpoint")

# Example in-memory model registry (ideally should be replaced by a database or persistent storage)
model_registry = ModelRegistry()

@router.post("/register")
async def register_model(file: UploadFile = File(...), model_name: str = None, current_user: Dict = Depends(IdentityManagement.get_current_user)):
    """
    Endpoint to register a new model by uploading a file.
    :param file: Model file to be registered.
    :param model_name: Optional name for the model.
    :param current_user: The authenticated user making the request.
    :return: Success message upon registration.
    """
    try:
        # Save uploaded model file
        model_dir = "./models/uploads/"
        os.makedirs(model_dir, exist_ok=True)
        file_path = os.path.join(model_dir, f"{model_name or file.filename}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pth")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Register model in the model registry
        model_metadata = {
            "model_name": model_name or file.filename,
            "file_path": file_path,
            "uploaded_by": current_user['username'],
            "timestamp": datetime.now().isoformat()
        }
        model_registry.register_model(model_metadata)

        logger.info(f"Model '{model_metadata['model_name']}' successfully registered by user '{current_user['username']}'.")
        return {"msg": "Model registered successfully", "model_metadata": model_metadata}
    except Exception as e:
        logger.error(f"Error while registering model: {e}")
        raise HTTPException(status_code=500, detail="Unable to register model")

@router.get("/list")
async def list_models(current_user: Dict = Depends(IdentityManagement.get_current_user)) -> List[Dict]:
    """
    Endpoint to list all models in the registry.
    :param current_user: The authenticated user making the request.
    :return: A list of all registered models.
    """
    try:
        models = model_registry.get_all_models()
        logger.info(f"User '{current_user['username']}' listed all models.")
        return models
    except Exception as e:
        logger.error(f"Error while listing models: {e}")
        raise HTTPException(status_code=500, detail="Unable to list models")

@router.get("/download/{model_id}")
async def download_model(model_id: str, current_user: Dict = Depends(IdentityManagement.get_current_user)):
    """
    Endpoint to download a specific model by ID.
    :param model_id: The unique identifier of the model to download.
    :param current_user: The authenticated user making the request.
    :return: The model file.
    """
    try:
        model_metadata = model_registry.get_model_by_id(model_id)
        if not model_metadata:
            raise HTTPException(status_code=404, detail="Model not found")

        file_path = model_metadata["file_path"]
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Model file not found")

        logger.info(f"User '{current_user['username']}' downloaded model '{model_metadata['model_name']}'.")
        return File(file_path, filename=os.path.basename(file_path))
    except Exception as e:
        logger.error(f"Error while downloading model: {e}")
        raise HTTPException(status_code=500, detail="Unable to download model")

@router.delete("/delete/{model_id}")
async def delete_model(model_id: str, current_user: Dict = Depends(IdentityManagement.get_current_user)):
    """
    Endpoint to delete a specific model by ID.
    :param model_id: The unique identifier of the model to delete.
    :param current_user: The authenticated user making the request.
    :return: Success message upon deletion.
    """
    try:
        model_metadata = model_registry.get_model_by_id(model_id)
        if not model_metadata:
            raise HTTPException(status_code=404, detail="Model not found")

        file_path = model_metadata["file_path"]
        if os.path.exists(file_path):
            os.remove(file_path)

        model_registry.delete_model(model_id)
        logger.info(f"User '{current_user['username']}' deleted model '{model_metadata['model_name']}'.")
        return {"msg": "Model deleted successfully"}
    except Exception as e:
        logger.error(f"Error while deleting model: {e}")
        raise HTTPException(status_code=500, detail="Unable to delete model")

# Example integration of the router
# To be used in the main FastAPI application
if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(router, prefix="/models", tags=["models"])

    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8002)
