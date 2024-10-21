import hashlib
import hmac
import os
import time
from typing import Optional

class Authentication:
    def __init__(self, secret_key: Optional[str] = None):
        """
        Initializes the authentication system with a secret key.
        :param secret_key: Optional secret key for generating HMACs. If not provided, a new key will be generated.
        """
        self.secret_key = secret_key or os.urandom(32)

    def generate_token(self, user_id: str, timestamp: Optional[int] = None) -> str:
        """
        Generates a token for a user using HMAC with the secret key.
        :param user_id: Unique identifier for the user.
        :param timestamp: Optional timestamp to include in the token.
        :return: Generated token as a hexadecimal string.
        """
        if timestamp is None:
            timestamp = int(time.time())
        message = f"{user_id}:{timestamp}".encode()
        token = hmac.new(self.secret_key, message, hashlib.sha256).hexdigest()
        print(f"Generated token for user '{user_id}': {token}")
        return token

    def verify_token(self, user_id: str, token: str, timestamp: int, max_age_seconds: int = 300) -> bool:
        """
        Verifies a given token for authenticity and ensures it is not expired.
        :param user_id: Unique identifier for the user.
        :param token: Token to be verified.
        :param timestamp: The timestamp included in the token.
        :param max_age_seconds: The maximum allowed age of the token, in seconds.
        :return: True if the token is valid and not expired, otherwise False.
        """
        current_time = int(time.time())
        if current_time - timestamp > max_age_seconds:
            print(f"Token expired for user '{user_id}'.")
            return False

        expected_token = self.generate_token(user_id, timestamp)
        if hmac.compare_digest(expected_token, token):
            print(f"Token verified successfully for user '{user_id}'.")
            return True
        else:
            print(f"Token verification failed for user '{user_id}'.")
            return False

    def hash_password(self, password: str, salt: Optional[bytes] = None) -> str:
        """
        Hashes a password with a given salt using SHA-256.
        :param password: Password to be hashed.
        :param salt: Optional salt value. If not provided, a new salt is generated.
        :return: The hashed password as a hexadecimal string.
        """
        if salt is None:
            salt = os.urandom(16)
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        hash_str = salt.hex() + "$" + hashed_password.hex()
        print(f"Password hashed successfully: {hash_str}")
        return hash_str

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verifies if the given password matches the hashed password.
        :param password: Password to verify.
        :param hashed_password: Hashed password for comparison.
        :return: True if the password matches, otherwise False.
        """
        salt_hex, stored_hash_hex = hashed_password.split('$')
        salt = bytes.fromhex(salt_hex)
        recalculated_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()
        if recalculated_hash == stored_hash_hex:
            print(f"Password verified successfully.")
            return True
        else:
            print(f"Password verification failed.")
            return False

# Example usage
if __name__ == "__main__":
    auth = Authentication()
    user_id = "user123"
    password = "secure_password"

    # Generate and verify a token
    token_timestamp = int(time.time())
    token = auth.generate_token(user_id, token_timestamp)
    is_token_valid = auth.verify_token(user_id, token, token_timestamp)
    print(f"Is token valid? {is_token_valid}")

    # Hash and verify a password
    hashed_pw = auth.hash_password(password)
    is_password_valid = auth.verify_password(password, hashed_pw)
    print(f"Is password valid? {is_password_valid}")