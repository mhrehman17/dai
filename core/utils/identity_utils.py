import uuid
import jwt
import datetime
from typing import Dict, Optional
import logging

class IdentityUtils:
    SECRET_KEY = "YOUR_SECRET_KEY"  # Replace this with your own secret key for signing tokens
    TOKEN_EXPIRATION_HOURS = 24  # Default expiration time for tokens (in hours)

    @staticmethod
    def generate_unique_id() -> str:
        """
        Generates a unique identifier for an agent or node.
        :return: A unique identifier string.
        """
        return str(uuid.uuid4())

    @staticmethod
    def generate_token(identity: str, logger: Optional[logging.Logger] = None) -> str:
        """
        Generates a JWT token for the given identity.
        :param identity: The identity for which the token is generated.
        :param logger: Logger instance to log the token generation.
        :return: A signed JWT token as a string.
        """
        try:
            expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=IdentityUtils.TOKEN_EXPIRATION_HOURS)
            payload = {
                "identity": identity,
                "exp": expiration_time
            }
            token = jwt.encode(payload, IdentityUtils.SECRET_KEY, algorithm="HS256")
            if logger:
                logger.info(f"Token generated for identity {identity}")
            return token
        except Exception as e:
            if logger:
                logger.error(f"Failed to generate token for identity {identity}: {e}")
            raise

    @staticmethod
    def verify_token(token: str, logger: Optional[logging.Logger] = None) -> Optional[Dict[str, str]]:
        """
        Verifies a given JWT token.
        :param token: The JWT token to verify.
        :param logger: Logger instance to log the verification process.
        :return: Decoded token payload if the token is valid, otherwise None.
        """
        try:
            decoded_token = jwt.decode(token, IdentityUtils.SECRET_KEY, algorithms=["HS256"])
            if logger:
                logger.info(f"Token verified for identity {decoded_token['identity']}")
            return decoded_token
        except jwt.ExpiredSignatureError:
            if logger:
                logger.error("Token has expired.")
            return None
        except jwt.InvalidTokenError:
            if logger:
                logger.error("Invalid token provided.")
            return None

    @staticmethod
    def refresh_token(token: str, logger: Optional[logging.Logger] = None) -> Optional[str]:
        """
        Refreshes a given JWT token by generating a new one if it is still valid.
        :param token: The existing JWT token to refresh.
        :param logger: Logger instance to log the refresh process.
        :return: A new signed JWT token as a string, or None if the original token is invalid.
        """
        try:
            decoded_token = IdentityUtils.verify_token(token, logger=logger)
            if decoded_token is None:
                if logger:
                    logger.error("Cannot refresh an invalid token.")
                return None
            # Generate a new token with the same identity but extended expiration time
            new_token = IdentityUtils.generate_token(decoded_token['identity'], logger=logger)
            if logger:
                logger.info(f"Token refreshed for identity {decoded_token['identity']}")
            return new_token
        except Exception as e:
            if logger:
                logger.error(f"Failed to refresh token: {e}")
            return None

# Example usage
if __name__ == "__main__":
    # Set up logger
    identity_logger = logging.getLogger("identity_utils")
    identity_logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    identity_logger.addHandler(console_handler)

    # Generate a unique identifier
    unique_id = IdentityUtils.generate_unique_id()
    identity_logger.info(f"Generated unique ID: {unique_id}")

    # Generate a JWT token for the unique identity
    token = IdentityUtils.generate_token(unique_id, logger=identity_logger)
    identity_logger.info(f"Generated Token: {token}")

    # Verify the token
    verified_payload = IdentityUtils.verify_token(token, logger=identity_logger)
    if verified_payload:
        identity_logger.info(f"Verified Token Payload: {verified_payload}")

    # Refresh the token
    refreshed_token = IdentityUtils.refresh_token(token, logger=identity_logger)
    if refreshed_token:
        identity_logger.info(f"Refreshed Token: {refreshed_token}")
