from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Dict
import logging
from datetime import timedelta
from core.utils.identity_utils import IdentityUtils
from core.agents.identity_management import IdentityManagement

router = APIRouter()
logger = logging.getLogger("authentication_endpoint")

# Constants for the authentication module
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token expiration set to 1 hour

# Example in-memory store of users, ideally this should be replaced by a proper database
fake_users_db = {
    "alice": {
        "username": "alice",
        "hashed_password": "fakehashedpassword",
        "disabled": False,
    },
    "bob": {
        "username": "bob",
        "hashed_password": "fakehashedpassword2",
        "disabled": False,
    },
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # A placeholder for real password verification, replace with proper hash check
    return plain_password == hashed_password

def authenticate_user(fake_db: Dict[str, Dict], username: str, password: str):
    user = fake_db.get(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint for obtaining an access token.
    :param form_data: Form data containing the username and password.
    :return: Access token and token type.
    """
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        logger.error(f"Authentication failed for username: {form_data.username}")
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = IdentityUtils.generate_token(user["username"], logger=logger)

    logger.info(f"User {form_data.username} successfully authenticated.")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(current_user: Dict = Depends(IdentityManagement.get_current_user)):
    """
    Get the current logged-in user details.
    :param current_user: Information about the current authenticated user.
    :return: The current user details.
    """
    return current_user

@router.post("/register")
async def register_user(username: str, password: str):
    """
    Endpoint for registering a new user.
    :param username: Username for the new user.
    :param password: Password for the new user.
    :return: Success message upon registration.
    """
    if username in fake_users_db:
        logger.error(f"Registration failed: Username '{username}' already exists.")
        raise HTTPException(status_code=400, detail="Username already registered")

    # Here we are using plain password, in real-world scenario we must hash the password
    hashed_password = password  # Replace with proper password hashing
    fake_users_db[username] = {
        "username": username,
        "hashed_password": hashed_password,
        "disabled": False,
    }
    logger.info(f"User '{username}' successfully registered.")
    return {"msg": "User registered successfully"}

@router.post("/revoke-token")
async def revoke_token(token: str):
    """
    Endpoint for revoking an access token.
    :param token: The token to be revoked.
    :return: Success message upon revocation.
    """
    # Note: Actual token revocation would involve blacklisting tokens, which is not implemented here.
    logger.info(f"Revoking token for user.")
    # Invalidate the token if using a proper token store
    return {"msg": "Token revoked successfully"}

# Example integration of the router
# To be used in the main FastAPI application
if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(router, prefix="/auth", tags=["authentication"])

    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8001)
