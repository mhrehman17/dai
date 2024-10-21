import logging
import threading
from typing import List, Tuple, Any
import torch
from torch import nn, optim
from torch.utils.data import DataLoader
from core.data.distributed_data_loader import DistributedDataLoader
from core.models.registry.version_metadata import VersionMetadata
from core.utils.log_utils import LogUtils

class DistributedModelTraining:
    def __init__(self, model: nn.Module, train_loader: DataLoader, test_loader: DataLoader,
                 host: str, port: int, peers: List[Tuple[str, int]],
                 logger: logging.Logger = None, cache_dir: str = './data_cache', version_dir: str = './model_registry'):
        """
        Initializes a DistributedModelTraining instance that facilitates distributed model training.
        :param model: The neural network model to train.
        :param train_loader: DataLoader for training data.
        :param test_loader: DataLoader for testing data.
        :param host: The hostname or IP address to bind the server.
        :param port: The port on which the server will listen.
        :param peers: A list of peer addresses in the format (host, port).
        :param logger: Logger instance to log distributed training activities.
        :param cache_dir: Directory where cached data should be stored.
        :param version_dir: Directory where model version metadata is stored.
        """
        self.logger = logger or logging.getLogger(__name__)
        self.model = model
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.distributed_loader = DistributedDataLoader(host, port, peers, cache_dir, logger=self.logger)
        self.version_metadata = VersionMetadata(metadata_dir=version_dir, logger=self.logger)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.criterion = nn.CrossEntropyLoss()
        self.running = False

    def start_training(self, epochs: int):
        """
        Starts the distributed model training.
        :param epochs: Number of epochs for training.
        """
        self.running = True
        self.distributed_loader.start_loader()
        threading.Thread(target=self._train, args=(epochs,), daemon=True).start()
        self.logger.info("Distributed model training started.")

    def stop_training(self):
        """
        Stops the distributed model training.
        """
        self.running = False
        self.distributed_loader.stop_loader()
        self.logger.info("Distributed model training stopped.")

    def _train(self, epochs: int):
        """
        Trains the model over a number of epochs, periodically evaluating and updating the version metadata.
        :param epochs: Number of epochs for training.
        """
        for epoch in range(epochs):
            self.model.train()
            running_loss = 0.0
            for inputs, labels in self.train_loader:
                self.optimizer.zero_grad()
                outputs = self.model(inputs)
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()
                running_loss += loss.item()
            avg_loss = running_loss / len(self.train_loader)
            self.logger.info(f"Epoch [{epoch + 1}/{epochs}], Loss: {avg_loss:.4f}")

            # Evaluate the model on test data
            accuracy = self._evaluate()
            self.logger.info(f"Epoch [{epoch + 1}/{epochs}], Accuracy: {accuracy:.4f}")

            # Save version metadata
            version = f"{epoch + 1}"  # Example version naming by epoch number
            metadata = {
                "version": version,
                "accuracy": accuracy,
                "loss": avg_loss,
                "epoch": epoch + 1
            }
            self.version_metadata.save_metadata(version, metadata)

    def _evaluate(self) -> float:
        """
        Evaluates the model's accuracy on the test data.
        :return: The accuracy of the model.
        """
        self.model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for inputs, labels in self.test_loader:
                outputs = self.model(inputs)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        accuracy = correct / total * 100
        return accuracy

# Example usage
if __name__ == "__main__":
    # Set up logger
    training_logger = LogUtils.setup_logger(name="distributed_model_training", level=logging.INFO)

    # Define a simple neural network model
    class SimpleModel(nn.Module):
        def __init__(self):
            super(SimpleModel, self).__init__()
            self.fc1 = nn.Linear(28 * 28, 128)
            self.fc2 = nn.Linear(128, 10)

        def forward(self, x):
            x = x.view(-1, 28 * 28)
            x = torch.relu(self.fc1(x))
            x = self.fc2(x)
            return x

    model = SimpleModel()

    # Assume train_loader and test_loader are defined elsewhere
    train_loader = DataLoader([])  # Placeholder, should be replaced with actual DataLoader
    test_loader = DataLoader([])  # Placeholder, should be replaced with actual DataLoader

    # Initialize and start distributed model training
    distributed_training = DistributedModelTraining(
        model=model,
        train_loader=train_loader,
        test_loader=test_loader,
        host="localhost",
        port=7000,
        peers=[("localhost", 7001)],
        logger=training_logger
    )
    distributed_training.start_training(epochs=5)

    # Allow some time for training
    try:
        threading.Event().wait(30)
    finally:
        distributed_training.stop_training()
