import os
import json
from typing import Dict, Optional
from core.models.base_model import BaseModel
from datetime import datetime

import torch

class ModelRegistry:
    def __init__(self, storage_path: str = "core/models/registry/storage"):
        """
        Initializes the model registry, responsible for managing model versions, metadata, and lifecycle.
        :param storage_path: Path where models and metadata will be stored.
        """
        self.storage_path = storage_path
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
        self.metadata_file = os.path.join(self.storage_path, "version_metadata.json")
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> Dict:
        """
        Loads model version metadata from the storage path.
        :return: A dictionary containing metadata for all model versions.
        """
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, "r") as f:
                return json.load(f)
        return {}

    def _save_metadata(self):
        """
        Saves the current model metadata to disk.
        """
        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata, f, indent=4)

    def save_model(self, model: BaseModel, version: str, description: str):
        """
        Saves a model checkpoint to disk and updates the metadata.
        :param model: The model to be saved.
        :param version: The version of the model.
        :param description: A description of the model version.
        """
        model_path = os.path.join(self.storage_path, f"version_{version}")
        if not os.path.exists(model_path):
            os.makedirs(model_path)
        checkpoint_path = os.path.join(model_path, "checkpoint.pth")
        torch.save(model.state_dict(), checkpoint_path)
        metrics_path = os.path.join(model_path, "metrics.json")

        dt = datetime.now()


        self.metadata[version] = {
            "description": description,
            "checkpoint_path": checkpoint_path,
            "metrics_path": metrics_path,
            "num_parameters": model.get_num_parameters(),
            "architecture": model.get_model_info()["architecture"],
            "timestamp": datetime.timestamp(dt)  # Placeholder for timestamp
        }
        self._save_metadata()
        print(f"Model version {version} saved successfully.")

    def load_model(self, model: BaseModel, version: str) -> Optional[BaseModel]:
        """
        Loads a model checkpoint from disk for a given version.
        :param model: The model object into which the weights should be loaded.
        :param version: The version of the model to load.
        :return: The model with loaded weights, or None if the version does not exist.
        """
        if version not in self.metadata:
            print(f"Model version {version} not found.")
            return None
        checkpoint_path = self.metadata[version]["checkpoint_path"]
        model.load_state_dict(torch.load(checkpoint_path))
        print(f"Model version {version} loaded successfully.")
        return model

    def list_versions(self) -> Dict:
        """
        Lists all the available model versions in the registry.
        :return: A dictionary containing metadata for all model versions.
        """
        return self.metadata

# Example usage
if __name__ == "__main__":
    from core.models.mnist_model import MNISTModel

    registry = ModelRegistry()
    mnist_model = MNISTModel()

    # Save a new version of the model
    registry.save_model(mnist_model, version="1.0", description="Initial version of the MNIST model.")

    # List all model versions
    versions = registry.list_versions()
    print(f"Available model versions: {json.dumps(versions, indent=4)}")

    # Load the saved model version
    loaded_model = registry.load_model(MNISTModel(), version="1.0")
