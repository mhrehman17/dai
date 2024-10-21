import unittest
from unittest.mock import patch
from flask import Flask
from flask.testing import FlaskClient
from api.endpoints.metrics import MetricsAPI
import pytest

# Integration tests for Metrics API and Core Metrics Logic

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(MetricsAPI, url_prefix='/metrics')
    return app

@pytest.fixture
def client(app) -> FlaskClient:
    return app.test_client()

@patch('api.endpoints.metrics.fetch_metrics_data')
def test_fetch_metrics_data_success(mock_fetch_metrics_data, client):
    # Simulate successful metrics data retrieval
    mock_fetch_metrics_data.return_value = {'data': [{'timestamp': 1625100000, 'value': 0.9}]}, 200
    response = client.get('/metrics/fetch')
    assert response.status_code == 200
    assert 'data' in response.get_data(as_text=True)
    assert 'value' in response.get_data(as_text=True)

@patch('api.endpoints.metrics.fetch_metrics_data')
def test_fetch_metrics_data_failure(mock_fetch_metrics_data, client):
    # Simulate failure to fetch metrics data (e.g., missing data)
    mock_fetch_metrics_data.side_effect = KeyError('Metrics not available')
    response = client.get('/metrics/fetch')
    assert response.status_code == 404
    assert 'Metrics not available' in response.get_data(as_text=True)

@patch('api.endpoints.metrics.handle_time_series_data')
def test_handle_time_series_data_success(mock_handle_time_series_data, client):
    # Simulate successful handling of time series data
    mock_handle_time_series_data.return_value = {'message': 'Time series data processed successfully'}, 200
    response = client.post('/metrics/time_series', json={'series': [0.1, 0.2, 0.3]})
    assert response.status_code == 200
    assert 'Time series data processed successfully' in response.get_data(as_text=True)

@patch('api.endpoints.metrics.handle_time_series_data')
def test_handle_time_series_data_failure(mock_handle_time_series_data, client):
    # Simulate failure in handling time series data (e.g., invalid format)
    mock_handle_time_series_data.side_effect = ValueError('Invalid time series format')
    response = client.post('/metrics/time_series', json={'series': 'invalid_data'})
    assert response.status_code == 400
    assert 'Invalid time series format' in response.get_data(as_text=True)

@patch('api.endpoints.metrics.get_metrics_summary')
def test_get_metrics_summary_success(mock_get_metrics_summary, client):
    # Simulate successful retrieval of metrics summary
    mock_get_metrics_summary.return_value = {'summary': {'accuracy': 0.95, 'loss': 0.05}}, 200
    response = client.get('/metrics/summary')
    assert response.status_code == 200
    assert 'accuracy' in response.get_data(as_text=True)
    assert 'loss' in response.get_data(as_text=True)

@patch('api.endpoints.metrics.get_metrics_summary')
def test_get_metrics_summary_failure(mock_get_metrics_summary, client):
    # Simulate failure in retrieving metrics summary (e.g., metrics calculation error)
    mock_get_metrics_summary.side_effect = RuntimeError('Metrics summary calculation failed')
    response = client.get('/metrics/summary')
    assert response.status_code == 500
    assert 'Metrics summary calculation failed' in response.get_data(as_text=True)

if __name__ == '__main__':
    pytest.main()
