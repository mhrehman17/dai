from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
import logging
from core.privacy.differential_privacy import DifferentialPrivacy
from core.privacy.homomorphic_encryption import HomomorphicEncryption
from core.privacy.privacy_budget_manager import PrivacyBudgetManager
from core.agents.identity_management import IdentityManagement

router = APIRouter()
logger = logging.getLogger("privacy_endpoint")

# Instantiate the privacy utilities
differential_privacy = DifferentialPrivacy(epsilon=1.0)
homomorphic_encryption = HomomorphicEncryption()
privacy_budget_manager = PrivacyBudgetManager(initial_budget=10.0)

@router.post("/apply-differential-privacy")
async def apply_differential_privacy(data: float, epsilon: float = 1.0, current_user: Dict = Depends(IdentityManagement.get_current_user)):
    """
    Endpoint to apply differential privacy noise to the given data.
    :param data: The original data value to which noise will be added.
    :param epsilon: The privacy parameter controlling noise level.
    :param current_user: The authenticated user making the request.
    :return: The data value after differential privacy noise has been applied.
    """
    try:
        noisy_data = differential_privacy.apply_noise(data, epsilon)
        logger.info(f"User '{current_user['username']}' applied differential privacy to data.")
        return {"original_data": data, "noisy_data": noisy_data}
    except Exception as e:
        logger.error(f"Error while applying differential privacy: {e}")
        raise HTTPException(status_code=500, detail="Unable to apply differential privacy")

@router.post("/encrypt-data")
async def encrypt_data(data: float, current_user: Dict = Depends(IdentityManagement.get_current_user)):
    """
    Endpoint to encrypt data using homomorphic encryption.
    :param data: The original data to be encrypted.
    :param current_user: The authenticated user making the request.
    :return: The encrypted data.
    """
    try:
        encrypted_data = homomorphic_encryption.encrypt(data)
        logger.info(f"User '{current_user['username']}' encrypted data using homomorphic encryption.")
        return {"encrypted_data": encrypted_data}
    except Exception as e:
        logger.error(f"Error while encrypting data: {e}")
        raise HTTPException(status_code=500, detail="Unable to encrypt data")

@router.post("/decrypt-data")
async def decrypt_data(encrypted_data: str, current_user: Dict = Depends(IdentityManagement.get_current_user)):
    """
    Endpoint to decrypt data using homomorphic encryption.
    :param encrypted_data: The encrypted data to be decrypted.
    :param current_user: The authenticated user making the request.
    :return: The decrypted data.
    """
    try:
        decrypted_data = homomorphic_encryption.decrypt(encrypted_data)
        logger.info(f"User '{current_user['username']}' decrypted data using homomorphic encryption.")
        return {"decrypted_data": decrypted_data}
    except Exception as e:
        logger.error(f"Error while decrypting data: {e}")
        raise HTTPException(status_code=500, detail="Unable to decrypt data")

@router.get("/privacy-budget")
async def get_privacy_budget(current_user: Dict = Depends(IdentityManagement.get_current_user)):
    """
    Endpoint to retrieve the current privacy budget.
    :param current_user: The authenticated user making the request.
    :return: The current privacy budget.
    """
    try:
        budget = privacy_budget_manager.get_budget()
        logger.info(f"User '{current_user['username']}' retrieved the privacy budget.")
        return {"privacy_budget": budget}
    except Exception as e:
        logger.error(f"Error while retrieving privacy budget: {e}")
        raise HTTPException(status_code=500, detail="Unable to retrieve privacy budget")

@router.post("/spend-privacy-budget")
async def spend_privacy_budget(amount: float, current_user: Dict = Depends(IdentityManagement.get_current_user)):
    """
    Endpoint to spend a portion of the privacy budget.
    :param amount: The amount of the privacy budget to spend.
    :param current_user: The authenticated user making the request.
    :return: The updated privacy budget after spending.
    """
    try:
        new_budget = privacy_budget_manager.spend_budget(amount)
        logger.info(f"User '{current_user['username']}' spent privacy budget amount '{amount}'.")
        return {"new_privacy_budget": new_budget}
    except Exception as e:
        logger.error(f"Error while spending privacy budget: {e}")
        raise HTTPException(status_code=500, detail="Unable to spend privacy budget")

# Example integration of the router
# To be used in the main FastAPI application
if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(router, prefix="/privacy", tags=["privacy"])

    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8004)