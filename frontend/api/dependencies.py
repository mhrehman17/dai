from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
import logging
from core_utils_identity_utils import IdentityUtils
from core.database.database import SessionLocal
from core.agents.identity_management import IdentityManagement

# Set up logging
logger = logging.getLogger("api_dependencies")

# Database dependency
def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get a database session.
    :return: Yields a new database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency for token verification
def get_current_user(token: str = Depends(IdentityUtils.oauth2_scheme)) -> dict:
    """
    Dependency to verify the current user based on the provided token.
    :param token: OAuth2 token string.
    :return: User details if verification is successful.
    """
    try:
        user = IdentityManagement.verify_user_token(token)
        if not user:
            logger.warning("Invalid token provided or user not found.")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user
    except Exception as e:
        logger.error(f"Error during token verification: {e}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

# Dependency for privileged actions
def get_current_admin_user(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Dependency to ensure that the current user is an admin for privileged actions.
    :param current_user: Current user dictionary retrieved from get_current_user.
    :return: User details if the user is authorized as an admin.
    """
    if not current_user.get("is_admin", False):
        logger.warning(f"Unauthorized attempt to access admin resources by user '{current_user['username']}'.")
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return current_user

# Example usage within a router (for reference)
# from fastapi import APIRouter
# router = APIRouter()
# @router.get("/protected-resource/")
# async def get_protected_resource(current_user: dict = Depends(get_current_user)):
#     return {"message": "You have access to this resource.", "user": current_user}

if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI, HTTPException

    app = FastAPI()

    @app.get("/verify-token")
    async def verify_token(current_user: dict = Depends(get_current_user)):
        """
        Sample endpoint to verify token functionality.
        :param current_user: Current user verified by get_current_user.
        :return: User details if the token is valid.
        """
        return {"msg": "Token verification successful", "user": current_user}

    # Run the server for demo purposes
    uvicorn.run(app, host="0.0.0.0", port=8005)