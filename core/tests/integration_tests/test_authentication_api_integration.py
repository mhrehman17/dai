import unittest
from unittest.mock import patch
from flask import Flask
from flask.testing import FlaskClient
from api.endpoints.authentication import AuthenticationAPI
import pytest

# Integration tests for Authentication API and Core Authentication Logic

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(AuthenticationAPI, url_prefix='/auth')
    return app

@pytest.fixture
def client(app) -> FlaskClient:
    return app.test_client()

@patch('api.endpoints.authentication.login')
def test_login_success(mock_login, client):
    # Simulate successful login
    mock_login.return_value = {'token': 'mock_token'}, 200
    response = client.post('/auth/login', json={'username': 'test_user', 'password': 'password123'})
    assert response.status_code == 200
    assert 'mock_token' in response.get_data(as_text=True)

@patch('api.endpoints.authentication.login')
def test_login_failure(mock_login, client):
    # Simulate failed login (e.g., incorrect credentials)
    mock_login.side_effect = ValueError('Invalid credentials')
    response = client.post('/auth/login', json={'username': 'test_user', 'password': 'wrong_password'})
    assert response.status_code == 401
    assert 'Invalid credentials' in response.get_data(as_text=True)

@patch('api.endpoints.authentication.logout')
def test_logout_success(mock_logout, client):
    # Simulate successful logout
    mock_logout.return_value = {'message': 'Logged out successfully'}, 200
    response = client.post('/auth/logout', json={'token': 'mock_token'})
    assert response.status_code == 200
    assert 'Logged out successfully' in response.get_data(as_text=True)

@patch('api.endpoints.authentication.logout')
def test_logout_failure(mock_logout, client):
    # Simulate failed logout (e.g., invalid token)
    mock_logout.side_effect = KeyError('Invalid token')
    response = client.post('/auth/logout', json={'token': 'invalid_token'})
    assert response.status_code == 400
    assert 'Invalid token' in response.get_data(as_text=True)

@patch('api.endpoints.authentication.issue_token')
def test_issue_token_success(mock_issue_token, client):
    # Simulate successful token issuance
    mock_issue_token.return_value = {'token': 'new_token'}, 200
    response = client.post('/auth/issue_token', json={'username': 'test_user'})
    assert response.status_code == 200
    assert 'new_token' in response.get_data(as_text=True)

@patch('api.endpoints.authentication.issue_token')
def test_issue_token_failure(mock_issue_token, client):
    # Simulate token issuance failure (e.g., user not found)
    mock_issue_token.side_effect = KeyError('User not found')
    response = client.post('/auth/issue_token', json={'username': 'unknown_user'})
    assert response.status_code == 404
    assert 'User not found' in response.get_data(as_text=True)

@patch('api.endpoints.authentication.multi_factor_auth')
def test_mfa_success(mock_mfa, client):
    # Simulate successful multi-factor authentication
    mock_mfa.return_value = {'message': 'MFA successful'}, 200
    response = client.post('/auth/mfa', json={'user_id': '1', 'code': '123456'})
    assert response.status_code == 200
    assert 'MFA successful' in response.get_data(as_text=True)

@patch('api.endpoints.authentication.multi_factor_auth')
def test_mfa_failure(mock_mfa, client):
    # Simulate failed multi-factor authentication (e.g., incorrect code)
    mock_mfa.side_effect = ValueError('Invalid MFA code')
    response = client.post('/auth/mfa', json={'user_id': '1', 'code': 'wrong_code'})
    assert response.status_code == 401
    assert 'Invalid MFA code' in response.get_data(as_text=True)

if __name__ == '__main__':
    pytest.main()
