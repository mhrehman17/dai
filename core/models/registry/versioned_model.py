from core.models.base_model import BaseModel
from core.models.registry.model_registry import ModelRegistry
from typing import Optional
import torch

class VersionedModel:
    def __init__(self, base_model: BaseModel, registry: ModelRegistry):
        """
        Initializes the VersionedModel wrapper to manage multiple versions of a model.
        :param base_model: The base model architecture.
        :param registry: The model registry instance to interact with.
        """
        self.base_model = base_model
        self.registry = registry
        self.current_version: Optional[str] = None

    def save_version(self, version: str, description: str):
        """
        Saves the current state of the model as a new version in the registry.
        :param version: The version identifier for the model.
        :param description: A description of this version of the model.
        """
        self.registry.save_model(self.base_model, version, description)
        self.current_version = version
        print(f"Model version {version} saved and set as current.")

    def load_version(self, version: str) -> Optional[BaseModel]:
        """
        Loads a specified version of the model from the registry.
        :param version: The version identifier of the model to load.
        :return: The model with loaded weights, or None if the version does not exist.
        """
        loaded_model = self.registry.load_model(self.base_model, version)
        if loaded_model:
            self.current_version = version
            self.base_model = loaded_model
            print(f"Loaded model version {version} successfully.")
        else:
            print(f"Failed to load model version {version}.")
        return loaded_model

    def get_current_version(self) -> str:
        """
        Returns the current version of the model.
        :return: Current model version identifier.
        """
        if self.current_version:
            return self.current_version
        else:
            raise ValueError("No version has been set or loaded for the model.")

    def train(self, data_loader, num_epochs: int = 1):
        """
        Trains the model and saves the new version upon completion.
        :param data_loader: DataLoader for training data.
        :param num_epochs: Number of epochs for training.
        """
        self.base_model.train()
        optimizer = torch.optim.Adam(self.base_model.parameters())
        loss_fn = torch.nn.CrossEntropyLoss()

        for epoch in range(num_epochs):
            for batch_idx, (data, target) in enumerate(data_loader):
                optimizer.zero_grad()
                output = self.base_model(data)
                loss = loss_fn(output, target)
                loss.backward()
                optimizer.step()
                if batch_idx % 10 == 0:
                    print(f"Epoch [{epoch+1}/{num_epochs}], Batch [{batch_idx}], Loss: {loss.item():.4f}")
        # Save the newly trained version
        version = str(float(self.current_version) + 0.1) if self.current_version else "1.0"
        self.save_version(version, description="Trained version after {} epochs".format(num_epochs))

# Example usage
if __name__ == "__main__":
    from core.models.mnist_model import MNISTModel
    from torch.utils.data import DataLoader
    from torchvision import datasets, transforms

    # Initialize model, registry, and versioned model wrapper
    mnist_model = MNISTModel()
    registry = ModelRegistry()
    versioned_model = VersionedModel(base_model=mnist_model, registry=registry)

    # Save initial version
    versioned_model.save_version(version="1.0", description="Initial version of the model")

    # Load the saved version
    versioned_model.load_version(version="1.0")

    # Create data loader for training
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
    train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

    # Train the model and create a new version
    versioned_model.train(train_loader, num_epochs=1)
