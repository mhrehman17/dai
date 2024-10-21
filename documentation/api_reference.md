# API Reference Documentation

## Overview
This document serves as a reference for the RESTful API endpoints provided by the Decentralized AI System. These endpoints are exposed via the FastAPI backend and provide various functionalities including agent management, orchestrator operations, metrics tracking, privacy and compliance management, monitoring, and more.

Base URL: `http://<server_ip>:<port>/api/v1`

---

## Endpoints

### 1. Agents

#### `GET /agents`
- **Description**: Retrieves a list of all registered agents.
- **Response**:
  - `200 OK`: Returns a list of agents with their current status and metadata.
  - **Example Response**:
    ```json
    [
      {
        "id": "agent_1",
        "status": "active",
        "role": "training"
      }
    ]
    ```

#### `POST /agents`
- **Description**: Registers a new agent in the system.
- **Request Body**:
  - `name` (string): The name of the agent.
  - `role` (string): The role assigned to the agent (e.g., training, evaluation).
- **Response**:
  - `201 Created`: Successfully registered the agent.

#### `DELETE /agents/{agent_id}`
- **Description**: Removes an agent from the system.
- **Parameters**:
  - `agent_id` (string): Unique identifier for the agent.
- **Response**:
  - `200 OK`: Agent successfully removed.

---

### 2. Orchestrator

#### `POST /orchestrator/start`
- **Description**: Starts the decentralized training orchestration.
- **Response**:
  - `200 OK`: Orchestrator successfully started.

#### `POST /orchestrator/stop`
- **Description**: Stops the orchestration process.
- **Response**:
  - `200 OK`: Orchestrator successfully stopped.

#### `GET /orchestrator/status`
- **Description**: Checks the status of the orchestrator.
- **Response**:
  - `200 OK`: Returns the current status of the orchestrator.
  - **Example Response**:
    ```json
    {
      "status": "running",
      "active_agents": 5
    }
    ```

---

### 3. Metrics

#### `GET /metrics`
- **Description**: Retrieves system metrics including agent performance, training progress, and resource utilization.
- **Response**:
  - `200 OK`: Returns a list of metrics.
  - **Example Response**:
    ```json
    {
      "cpu_usage": "75%",
      "memory_usage": "60%",
      "agents_active": 3
    }
    ```

#### `GET /metrics/{metric_id}`
- **Description**: Retrieves specific metrics based on the provided metric ID.
- **Parameters**:
  - `metric_id` (string): Unique identifier of the metric.
- **Response**:
  - `200 OK`: Returns the requested metric details.

---

### 4. Privacy

#### `POST /privacy/apply-differential-privacy`
- **Description**: Applies differential privacy techniques to the given data.
- **Request Body**:
  - `dataset_id` (string): The dataset to which privacy needs to be applied.
  - `privacy_budget` (number): The privacy budget value to be used.
- **Response**:
  - `200 OK`: Differential privacy successfully applied.

---

### 5. Monitoring

#### `GET /monitoring/agents`
- **Description**: Provides monitoring data for all agents in the system.
- **Response**:
  - `200 OK`: Returns information about the status, uptime, and health of agents.

#### `GET /monitoring/system`
- **Description**: Retrieves monitoring information for the overall system including resource utilization.
- **Response**:
  - `200 OK`: Returns system-level metrics.

---

### 6. Authentication

#### `POST /auth/login`
- **Description**: Authenticates a user and provides a JWT token for session management.
- **Request Body**:
  - `username` (string): Username of the user.
  - `password` (string): Password of the user.
- **Response**:
  - `200 OK`: Returns an authentication token.
  - **Example Response**:
    ```json
    {
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```

#### `POST /auth/logout`
- **Description**: Logs out the current user and invalidates the JWT token.
- **Response**:
  - `200 OK`: User successfully logged out.

---

## Common HTTP Response Codes
- **200 OK**: Request completed successfully.
- **201 Created**: Resource was successfully created.
- **400 Bad Request**: The request could not be understood or was missing required parameters.
- **401 Unauthorized**: Authentication failed or user is not authorized.
- **404 Not Found**: Requested resource not found.
- **500 Internal Server Error**: An error occurred on the server.

## Notes
- All endpoints require authentication except for `/auth/login`.
- JWT tokens must be included in the `Authorization` header as `Bearer <token>`.

## Versioning
- Current API version: **v1**
- Base URL for all requests: `http://<server_ip>:<port>/api/v1`

For more detailed usage examples, please refer to the usage documentation or visit the interactive API documentation page available with the FastAPI framework at `/docs` or `/redoc`.

