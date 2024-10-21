# Privacy Enhancement Examples

## Overview
This tutorial provides examples of how privacy-enhancing techniques can be integrated into the **Decentralized AI System** to ensure that sensitive information remains private during model training and deployment. We will explore different approaches such as **Differential Privacy**, **Homomorphic Encryption**, and **Secure Multiparty Computation (MPC)** that allow federated learning while maintaining robust data security.

## Privacy Enhancements Covered
1. **Differential Privacy**: Ensuring that individual data points cannot be inferred from model outputs.
2. **Homomorphic Encryption**: Encrypting data and performing computations directly on the encrypted data without decryption.
3. **Secure Multiparty Computation (MPC)**: Allowing multiple agents to collaboratively compute a function without revealing their private inputs.

## Prerequisites
- **Python 3.8+**
- **PySyft**: A Python library for privacy-preserving, federated learning.
  ```sh
  pip install syft
  ```
- **Cryptography**: Install the cryptography package for encryption-related examples.
  ```sh
  pip install cryptography
  ```
- **TensorFlow or PyTorch**: Depending on the backend used for training the model.
- **Docker & Kubernetes**: For containerized deployments.

## Example 1: Differential Privacy in Federated Learning
Differential privacy ensures that each participant's data cannot be re-identified from the trained model. 

### Step 1: Configure Privacy Budget
- The privacy budget, or **epsilon**, controls how much information the model can learn from any individual data point.
- Open the configuration file `configs/privacy_config.yaml` and set the following:
  ```yaml
  differential_privacy: true
  epsilon: 1.0  # Lower values provide stronger privacy
  delta: 1e-5
  noise_multiplier: 1.1
  ```

### Step 2: Train Model with Differential Privacy
- Use the **Differential Privacy Optimizer** to add noise to the gradients during training:
  ```python
  from core.privacy.differential_privacy import DPOptimizer
  from torch.optim import SGD

  model = MNISTModel()
  optimizer = SGD(model.parameters(), lr=0.01)
  dp_optimizer = DPOptimizer(optimizer, noise_multiplier=1.1, max_grad_norm=1.0)
  ```
- **Agent Training Script**: Modify the agent training script (`core/agents/training_agent.py`) to use the `DPOptimizer` instead of the regular optimizer to ensure privacy protection during training.

### Step 3: Execute Federated Training
- Initiate federated learning from the orchestrator, and the differential privacy mechanisms will be applied automatically:
  ```sh
  curl -X POST http://<orchestrator-ip>:8001/api/training/start --data '{"privacy": "differential"}'
  ```

## Example 2: Homomorphic Encryption for Data Privacy
Homomorphic encryption allows computations to be performed on encrypted data without the need to decrypt it first. This ensures data privacy while allowing the orchestrator to aggregate model updates.

### Step 1: Configure Encryption Settings
- Open `configs/privacy_config.yaml` and set **homomorphic_encryption** to true:
  ```yaml
  homomorphic_encryption: true
  encryption_scheme: CKKS  # Options: BFV, CKKS
  key_length: 4096
  ```

### Step 2: Encrypt Gradients During Training
- Update the gradient encryption logic in `core/agents/training_agent.py`:
  ```python
  from core.privacy.homomorphic_encryption import EncryptionHandler

  encryption_handler = EncryptionHandler(scheme="CKKS", key_length=4096)
  encrypted_gradients = encryption_handler.encrypt(gradients)
  ```
- Ensure that gradients are encrypted before being sent to the orchestrator.

### Step 3: Decrypt Aggregated Model at Orchestrator
- Modify the orchestrator script (`core/orchestrator/decentralized_orchestrator.py`) to decrypt the aggregated model updates using the **EncryptionHandler**:
  ```python
  aggregated_update = encryption_handler.decrypt(aggregated_encrypted_update)
  ```

## Example 3: Secure Multiparty Computation (MPC)
Secure Multiparty Computation allows multiple agents to compute a shared function without revealing their private data.

### Step 1: Set Up MPC
- Use **PySyft** for implementing MPC in Python. Install PySyft if not already installed:
  ```sh
  pip install syft
  ```
- Initialize secure workers (Alice, Bob, and a **crypto provider**):
  ```python
  import syft as sy
  hook = sy.TorchHook(torch)
  alice = sy.VirtualWorker(hook, id="alice")
  bob = sy.VirtualWorker(hook, id="bob")
  crypto_provider = sy.VirtualWorker(hook, id="crypto_provider")
  ```

### Step 2: Share Data Across Workers
- Each agent holds a secret share of the data, and no single agent knows the entire dataset:
  ```python
  data = data.fix_precision().share(alice, bob, crypto_provider=crypto_provider)
  ```
- Training can now be done on these secret-shared datasets.

### Step 3: Perform Federated Training
- Train a model on these secure data shares without exposing the raw data:
  ```python
  result = model(data)
  loss = criterion(result, target)
  loss.backward()
  optimizer.step()
  ```

## Example 4: Combining Privacy Techniques
To maximize privacy, you can combine the above techniques. For example, **Differential Privacy** can be used in conjunction with **Homomorphic Encryption** to ensure that encrypted model updates still maintain differential privacy constraints.

### Step 1: Enable Both Techniques
- Open `configs/privacy_config.yaml` and set both **differential_privacy** and **homomorphic_encryption** to true.
  ```yaml
  differential_privacy: true
  homomorphic_encryption: true
  epsilon: 1.0
  encryption_scheme: CKKS
  ```

### Step 2: Modify Training Pipeline
- Update the training script (`training_agent.py`) to utilize **DPOptimizer** and encrypt gradients before sharing.
- The orchestrator will then securely aggregate the model using MPC for additional protection.

## Best Practices for Privacy Enhancement
1. **Monitor Privacy Budget**: Regularly monitor the privacy budget (`epsilon`) to ensure the system does not exceed acceptable thresholds.
2. **Rotate Keys Regularly**: If using homomorphic encryption, periodically rotate keys to maintain security.
3. **Enable Logging**: Use the **privacy monitor** (`core/monitoring/privacy_monitor.py`) to log privacy-related metrics and ensure compliance.
4. **Run Tests**: Run **security tests** from the testing suite (`core/tests/security_tests/`) to verify that privacy mechanisms are properly integrated and operational.

## Summary
This tutorial demonstrated how to integrate privacy-enhancing techniques into the **Decentralized AI System** to ensure sensitive information is protected during training and aggregation. With techniques like **Differential Privacy**, **Homomorphic Encryption**, and **Secure MPC**, users can achieve robust privacy while maintaining model performance.

### Key Highlights
- Differential privacy ensures that data points cannot be re-identified.
- Homomorphic encryption allows secure model aggregation without decrypting data.
- Secure Multiparty Computation facilitates collaborative training while keeping data private.

For more detailed explanations, refer to the [Privacy Policy Documentation](privacy_policy.md) or consult with the **Security Configuration Guide** for further insights into system privacy management.

