import torch
import logging
import json
import os
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from core.models.mnist_model import MNISTModel

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ModelComparison")

# Constants
MODEL_VERSIONS_DIR = "core/models/registry/storage"
BATCH_SIZE = 64

# Load test dataset
def load_test_data():
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
    test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    return test_loader

# Function to load a specific model version
def load_model(version_path):
    model = MNISTModel()
    model_checkpoint = os.path.join(version_path, "checkpoint.pth")
    if os.path.exists(model_checkpoint):
        model.load_state_dict(torch.load(model_checkpoint, map_location=torch.device('cpu')))
        model.eval()
        logger.info(f"Model loaded from {model_checkpoint}")
    else:
        logger.error(f"Model checkpoint not found at {model_checkpoint}")
        raise FileNotFoundError(f"Model checkpoint not found at {model_checkpoint}")
    return model

# Function to evaluate the model
def evaluate_model(model, test_loader):
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    accuracy = 100 * correct / total
    return accuracy

# Function to compare different model versions
def compare_model_versions():
    logger.info("Starting model version comparison...")
    test_loader = load_test_data()

    version_dirs = [os.path.join(MODEL_VERSIONS_DIR, d) for d in os.listdir(MODEL_VERSIONS_DIR) if os.path.isdir(os.path.join(MODEL_VERSIONS_DIR, d))]
    comparison_results = {}

    for version_dir in version_dirs:
        try:
            model = load_model(version_dir)
            accuracy = evaluate_model(model, test_loader)
            version_name = os.path.basename(version_dir)
            comparison_results[version_name] = accuracy
            logger.info(f"Model Version: {version_name}, Accuracy: {accuracy:.2f}%")
        except Exception as e:
            logger.error(f"Failed to evaluate model version in {version_dir}: {e}")

    # Save comparison results to a JSON file
    results_file = "comparison_results.json"
    with open(results_file, 'w') as f:
        json.dump(comparison_results, f, indent=4)
    logger.info(f"Comparison results saved to {results_file}")

if __name__ == "__main__":
    compare_model_versions()
