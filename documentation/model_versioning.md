# Model Versioning and Registry Documentation

## Overview
Model versioning is a core feature of the **Decentralized AI System**, allowing users to manage, track, and utilize multiple versions of AI models across training and deployment environments. The **Model Registry** provides a centralized repository for managing models, storing metadata, and supporting different deployment scenarios, ensuring that all nodes within the decentralized system can access the most up-to-date and optimal versions of models.

## Key Features of Model Versioning
- **Version Management**: Track changes between different versions of a model, including performance metrics such as accuracy, loss, and resource utilization.
- **Metadata Tracking**: Keep detailed information about each model version, such as training data used, training parameters, model architecture, and other important metadata.
- **Deployment History**: Track where and how each version of the model has been deployed in the decentralized system, including both cloud and edge deployments.
- **Rollbacks**: Easily roll back to a previous model version if the current version underperforms or fails.

## Directory Structure for Model Versioning
The model versions are stored in the `core/models/registry/storage/` directory, with each version having its own subdirectory:

```
core/models/registry/storage/
├── version_1/
│   ├── checkpoint.pth             # Model weights and state
│   ├── metrics.json               # Performance metrics (accuracy, loss, etc.)
│   └── metadata.json              # Model metadata (training data, architecture details)
├── version_2/
│   ├── checkpoint.pth
│   ├── metrics.json
│   └── metadata.json
└── ...                            # Additional versions as needed
```
- **`checkpoint.pth`**: Stores the model weights and optimizer state.
- **`metrics.json`**: Stores metrics collected during training and evaluation.
- **`metadata.json`**: Stores detailed information about the model version, such as hyperparameters and dataset information.

## Workflow for Managing Model Versions
### Step 1: Training a New Version
When a new model version is trained, it is saved locally by the agent. The agent uploads the trained model to the **Model Registry** using a REST API exposed by `model_registry.py`. The **training agent** saves metadata, including training parameters, version number, and evaluation metrics.

### Step 2: Registration in the Model Registry
The new version of the model is registered with the central **Model Registry**.
- The **model registry API** (`API/endpoints/models.py`) is responsible for handling model uploads and metadata registration.
- Each model version is assigned a unique identifier, which is then used by agents and orchestrators to reference and retrieve the model for future training or inference tasks.

### Step 3: Updating Metadata and Metrics
Once the model is uploaded, performance metrics and additional metadata are saved to `metrics.json` and `metadata.json`. This metadata is used to:
- Track the performance of different model versions.
- Facilitate comparisons between models to choose the best-performing version for deployment.
- Ensure compatibility between models and deployment environments.

### Step 4: Deploying a Model Version
Orchestrators use the **Model Registry** to retrieve the latest version of the model that has been approved for deployment. Depending on the deployment scenario, different versions can be deployed to cloud or edge environments.
- **Edge Deployment**: Agents at the edge can download a model version using the **ONNX format** to optimize compatibility and resource usage.
- **Cloud Deployment**: Models are deployed on cloud instances and can use full-precision versions, which might have been trained with more complex architectures and resources.

### Step 5: Model Rollbacks
If an issue is detected in a newly deployed model version, the orchestrator can initiate a rollback using the model registry.
- The rollback process involves deprecating the faulty model and restoring the previous stable version from `core/models/registry/storage/`.
- Version metadata is updated to mark the faulty version as deprecated.

## Example REST API Endpoints for Model Version Management
The **Model Registry API** exposes several endpoints to manage model versions:

- **Upload a Model**:
  ```http
  POST /api/models/upload
  ```
  - **Parameters**: Model file, metadata (training parameters, dataset information)
  - **Response**: Returns the unique version ID and registration status.

- **Get Model Metadata**:
  ```http
  GET /api/models/{version_id}/metadata
  ```
  - **Parameters**: `version_id` - Identifier of the model version
  - **Response**: Returns metadata including architecture, training data, and hyperparameters.

- **List Available Versions**:
  ```http
  GET /api/models/versions
  ```
  - **Response**: Returns a list of all available model versions, along with their metrics and metadata.

- **Download a Model**:
  ```http
  GET /api/models/{version_id}/download
  ```
  - **Parameters**: `version_id` - Identifier of the model version
  - **Response**: Returns the model file in the requested format (e.g., PyTorch `.pth` or ONNX).

## Version Metadata Structure
Each model version includes metadata that describes the training conditions, data, and hyperparameters used. Below is an example of what the `metadata.json` file might look like:

```json
{
  "version_id": "2",
  "model_name": "mnist_model",
  "training_data": "MNIST Dataset",
  "architecture": "Convolutional Neural Network (2 Conv Layers, 1 Dense Layer)",
  "hyperparameters": {
    "learning_rate": 0.001,
    "batch_size": 64,
    "num_epochs": 10
  },
  "training_timestamp": "2024-10-15T12:45:00",
  "optimizer": "Adam",
  "loss_function": "CrossEntropyLoss",
  "accuracy": 0.975,
  "deployed": false
}
```
- **`version_id`**: The version number of the model.
- **`training_data`**: The dataset used during training.
- **`architecture`**: The model architecture description.
- **`hyperparameters`**: Contains key hyperparameters used during training.
- **`deployed`**: Indicates if the model is currently deployed.

## Model Registry Features
### 1. **ONNX Conversion for Edge Devices**
The system supports **ONNX** model conversion for lightweight deployments. This helps in edge environments where computation power is limited. The conversion process is automated using the script `onnx_conversion.py`.

### 2. **Version Comparison and Metrics Analysis**
The **compare_model_versions.py** script in the `examples/mnist_pytorch/` directory allows for detailed analysis and comparison of different model versions based on training metrics and evaluation performance.

### 3. **Model Deprecation**
If a model version is found to have issues, it can be deprecated by updating the metadata. Deprecation ensures that the model is no longer available for future deployments.

## Best Practices
- **Incremental Versioning**: Always increment version numbers in a consistent and meaningful way to track updates effectively.
- **Metadata Completeness**: Provide complete metadata for each model to facilitate comparisons and deployments.
- **Version Testing**: Thoroughly test each new model version in both the cloud and edge environments before making it available for widespread deployment.
- **Model Rollback Procedures**: Keep previous versions ready and tested for rollback in case of unexpected model behavior.

## Summary
Model versioning is crucial for ensuring the robustness, traceability, and reliability of AI models in the Decentralized AI System. The **Model Registry** provides the infrastructure for managing, deploying, and monitoring these versions effectively, ensuring that agents and orchestrators always use the best available model.

For further information on deployment and version management, please refer to the [Deployment Guide](deployment_guide.md) or reach out to the project maintainers.

