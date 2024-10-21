import torch
import logging
from torch import nn, optim
from core.models.mnist_model import MNISTModel
from core.data.mnist_data_loader import load_mnist_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MNISTTrainingAgent")

# Constants
BATCH_SIZE = 32
LEARNING_RATE = 0.001
EPOCHS = 5
MODEL_SAVE_PATH = "mnist_trained_model.pth"

# MNIST Training Agent Class
class MNISTTrainingAgent:
    def __init__(self):
        self.model = MNISTModel()
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=LEARNING_RATE)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def train(self, train_loader):
        """
        Train the MNIST model using the training data loader.
        """
        self.model.train()
        for epoch in range(EPOCHS):
            running_loss = 0.0
            for images, labels in train_loader:
                images, labels = images.to(self.device), labels.to(self.device)

                # Zero the parameter gradients
                self.optimizer.zero_grad()

                # Forward pass
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)

                # Backward pass and optimization
                loss.backward()
                self.optimizer.step()

                running_loss += loss.item()

            logger.info(f"Epoch [{epoch + 1}/{EPOCHS}], Loss: {running_loss / len(train_loader):.4f}")

    def evaluate(self, test_loader):
        """
        Evaluate the MNIST model using the test data loader.
        """
        self.model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for images, labels in test_loader:
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = self.model(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        accuracy = 100 * correct / total
        return accuracy

    def save_model(self):
        """
        Save the trained MNIST model to a file.
        """
        torch.save(self.model.state_dict(), MODEL_SAVE_PATH)
        logger.info(f"Model saved successfully at {MODEL_SAVE_PATH}")

# Main function to train and evaluate the MNIST model
def run_mnist_training_agent():
    logger.info("Loading MNIST data...")
    train_loader, test_loader = load_mnist_data(batch_size=BATCH_SIZE)
    logger.info("MNIST data loaded successfully.")

    training_agent = MNISTTrainingAgent()

    logger.info("Starting training process...")
    training_agent.train(train_loader)
    logger.info("Training process completed.")

    logger.info("Evaluating model...")
    accuracy = training_agent.evaluate(test_loader)
    logger.info(f"Model Evaluation Completed. Accuracy: {accuracy:.2f}%")

    logger.info("Saving trained model...")
    training_agent.save_model()

if __name__ == "__main__":
    run_mnist_training_agent()
