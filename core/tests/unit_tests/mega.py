import pytest
import requests
from requests.auth import HTTPBasicAuth
import json
import time

# Base URL of the FastAPI application
BASE_URL = "http://localhost:8000/api/endpoints"

# Sample Authentication Token for Testing (Replace with a valid token for actual tests)
VALID_TOKEN = "valid_test_token"
EXPIRED_TOKEN = "expired_test_token"
INVALID_TOKEN = "invalid_test_token"

# Helper function to get authentication headers
def get_auth_headers(token):
    return {"Authorization": f"Bearer {token}"}

# 1. Authentication and Authorization Tests

@pytest.mark.parametrize("endpoint", [
    f"{BASE_URL}/agents",
    f"{BASE_URL}/orchestrator",
    f"{BASE_URL}/metrics",
    f"{BASE_URL}/privacy",
    f"{BASE_URL}/monitoring",
])
def test_authentication_required(endpoint):
    response = requests.get(endpoint)
    assert response.status_code == 401, f"Unauthorized access allowed on endpoint {endpoint}"

@pytest.mark.parametrize("endpoint", [
    f"{BASE_URL}/agents",
    f"{BASE_URL}/orchestrator",
    f"{BASE_URL}/metrics",
    f"{BASE_URL}/privacy",
    f"{BASE_URL}/monitoring",
])
def test_valid_token_authentication(endpoint):
    headers = get_auth_headers(VALID_TOKEN)
    response = requests.get(endpoint, headers=headers)
    assert response.status_code == 200, f"Valid token failed on endpoint {endpoint}"

@pytest.mark.parametrize("endpoint", [
    f"{BASE_URL}/agents",
    f"{BASE_URL}/orchestrator",
])
def test_mfa_required(endpoint):
    # Assuming MFA requires an additional header "X-MFA-Code"
    headers = get_auth_headers(VALID_TOKEN)
    response = requests.get(endpoint, headers=headers)
    assert response.status_code == 403, "Access without MFA code was not blocked"
    headers["X-MFA-Code"] = "123456"  # Assuming a test MFA code
    response = requests.get(endpoint, headers=headers)
    assert response.status_code == 200, "Access with MFA code failed"


# 2. Input Validation Tests
@pytest.mark.parametrize("endpoint, payload", [
    (f"{BASE_URL}/agents", {"name": "test_agent' OR '1'='1"}),  # SQL Injection
    (f"{BASE_URL}/privacy", {"input": "<script>alert(1)</script>"}),  # XSS
    (f"{BASE_URL}/orchestrator", {"command": "&& rm -rf /"}),  # Command Injection
])
def test_input_validation(endpoint, payload):
    headers = get_auth_headers(VALID_TOKEN)
    response = requests.post(endpoint, headers=headers, json=payload)
    assert response.status_code in [400, 422], f"Input validation failed on endpoint {endpoint}"


# 3. Rate Limiting Tests
@pytest.mark.parametrize("endpoint", [
    f"{BASE_URL}/agents",
    f"{BASE_URL}/orchestrator",
    f"{BASE_URL}/metrics",
])
def test_rate_limiting(endpoint):
    headers = get_auth_headers(VALID_TOKEN)
    # Sending 20 requests in rapid succession to test rate limiting
    responses = [requests.get(endpoint, headers=headers) for _ in range(20)]
    rate_limited_responses = [r for r in responses if r.status_code == 429]
    assert len(rate_limited_responses) > 0, f"Rate limiting not enforced on endpoint {endpoint}"


# 4. Token Expiry and Security Tests
@pytest.mark.parametrize("endpoint", [
    f"{BASE_URL}/agents",
    f"{BASE_URL}/orchestrator",
])
def test_token_expiry(endpoint):
    headers = get_auth_headers(EXPIRED_TOKEN)
    response = requests.get(endpoint, headers=headers)
    assert response.status_code == 401, f"Expired token was allowed on endpoint {endpoint}"

@pytest.mark.parametrize("endpoint", [
    f"{BASE_URL}/agents",
    f"{BASE_URL}/orchestrator",
])
def test_replay_attack(endpoint):
    headers = get_auth_headers(VALID_TOKEN)
    response = requests.get(endpoint, headers=headers)
    assert response.status_code == 200, f"Valid token failed on endpoint {endpoint}"
    # Reusing the same token (assuming it should only be valid once)
    response = requests.get(endpoint, headers=headers)
    assert response.status_code == 401, f"Replay attack not prevented on endpoint {endpoint}"


# 5. CORS Configuration Tests
def test_cors_configuration():
    headers = {"Origin": "http://unauthorized.com"}
    response = requests.options(f"{BASE_URL}/agents", headers=headers)
    assert "Access-Control-Allow-Origin" not in response.headers, "CORS misconfiguration allows unauthorized origin"


# 6. Data Exposure Tests
@pytest.mark.parametrize("endpoint", [
    f"{BASE_URL}/orchestrator",
    f"{BASE_URL}/metrics",
    f"{BASE_URL}/privacy",
])
def test_data_exposure(endpoint):
    headers = get_auth_headers(VALID_TOKEN)
    response = requests.get(endpoint, headers=headers)
    assert response.status_code == 200, f"Failed to get a response from {endpoint}"
    response_text = response.text.lower()
    sensitive_keywords = ["api_key", "password", "token"]
    for keyword in sensitive_keywords:
        assert keyword not in response_text, f"Sensitive information ({keyword}) exposed in {endpoint}"


if __name__ == "__main__":
    pytest.main()


