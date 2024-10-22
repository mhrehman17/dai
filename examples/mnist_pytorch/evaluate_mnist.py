import torch
import logging
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from core.models.mnist_model import MNISTModel

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MNISTEvaluation")

# Constants
BATCH_SIZE = 64
MODEL_PATH = "core/models/registry/storage/version_1.0/checkpoint.pth"

# Load test dataset
def load_test_data():
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
    test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    return test_loader

# Function to load the model
def load_model(model_path):
    model = MNISTModel()
    if not torch.cuda.is_available():
        model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    else:
        model.load_state_dict(torch.load(model_path))
        model = model.cuda()
    model.eval()
    logger.info(f"Model loaded successfully from {model_path}")
    return model

# Function to evaluate the model
def evaluate_model(model, test_loader):
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            if torch.cuda.is_available():
                images, labels = images.cuda(), labels.cuda()
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    accuracy = 100 * correct / total
    return accuracy

# Main function to evaluate the MNIST model
def evaluate_mnist_model():
    logger.info("Loading test data...")
    test_loader = load_test_data()
    logger.info("Test data loaded successfully.")

    logger.info("Loading model...")
    model = load_model(MODEL_PATH)

    logger.info("Evaluating model...")
    accuracy = evaluate_model(model, test_loader)
    logger.info(f"Model Evaluation Completed. Accuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    evaluate_mnist_model()
