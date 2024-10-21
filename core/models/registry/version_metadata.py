import json
import os
import logging
from typing import Dict, Optional

class VersionMetadata:
    def __init__(self, metadata_dir: str = './model_registry', logger: Optional[logging.Logger] = None):
        """
        Initializes the VersionMetadata manager for managing metadata of different model versions.
        :param metadata_dir: Directory where model version metadata is stored.
        :param logger: Logger instance to log metadata management activities.
        """
        self.metadata_dir = metadata_dir
        self.logger = logger or logging.getLogger(__name__)
        if not os.path.exists(self.metadata_dir):
            os.makedirs(self.metadata_dir)
            self.logger.info(f"Metadata directory created at {self.metadata_dir}")

    def save_metadata(self, version: str, metadata: Dict[str, Any]):
        """
        Saves metadata for a specific version.
        :param version: Version identifier of the model.
        :param metadata: A dictionary containing metadata like accuracy, loss, timestamp, etc.
        """
        metadata_filepath = os.path.join(self.metadata_dir, f"{version}_metadata.json")
        try:
            with open(metadata_filepath, 'w') as metadata_file:
                json.dump(metadata, metadata_file, indent=4)
            self.logger.info(f"Metadata for version {version} saved successfully at {metadata_filepath}")
        except Exception as e:
            self.logger.error(f"Failed to save metadata for version {version}: {e}")

    def load_metadata(self, version: str) -> Optional[Dict[str, Any]]:
        """
        Loads metadata for a specific version.
        :param version: Version identifier of the model.
        :return: A dictionary containing metadata if found, otherwise None.
        """
        metadata_filepath = os.path.join(self.metadata_dir, f"{version}_metadata.json")
        if not os.path.exists(metadata_filepath):
            self.logger.warning(f"Metadata for version {version} not found.")
            return None
        try:
            with open(metadata_filepath, 'r') as metadata_file:
                metadata = json.load(metadata_file)
            self.logger.info(f"Metadata for version {version} loaded successfully from {metadata_filepath}")
            return metadata
        except Exception as e:
            self.logger.error(f"Failed to load metadata for version {version}: {e}")
            return None

    def update_metadata(self, version: str, updated_metadata: Dict[str, Any]):
        """
        Updates metadata for a specific version.
        :param version: Version identifier of the model.
        :param updated_metadata: A dictionary containing the updated metadata.
        """
        metadata = self.load_metadata(version)
        if metadata is None:
            self.logger.warning(f"Cannot update metadata: Version {version} not found.")
            return
        metadata.update(updated_metadata)
        self.save_metadata(version, metadata)
        self.logger.info(f"Metadata for version {version} updated successfully.")

    def delete_metadata(self, version: str):
        """
        Deletes metadata for a specific version.
        :param version: Version identifier of the model.
        """
        metadata_filepath = os.path.join(self.metadata_dir, f"{version}_metadata.json")
        try:
            if os.path.exists(metadata_filepath):
                os.remove(metadata_filepath)
                self.logger.info(f"Metadata for version {version} deleted successfully.")
            else:
                self.logger.warning(f"Attempted to delete metadata for non-existent version {version}")
        except Exception as e:
            self.logger.error(f"Failed to delete metadata for version {version}: {e}")

# Example usage
if __name__ == "__main__":
    # Set up logger
    metadata_logger = logging.getLogger("version_metadata")
    metadata_logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    metadata_logger.addHandler(console_handler)

    # Initialize VersionMetadata manager
    version_metadata_manager = VersionMetadata(logger=metadata_logger)

    # Example metadata for a model version
    metadata = {
        "version": "1.0",
        "accuracy": 0.95,
        "loss": 0.05,
        "timestamp": "2024-10-15T12:34:56"
    }

    # Save metadata for version 1.0
    version_metadata_manager.save_metadata("1.0", metadata)

    # Load metadata for version 1.0
    loaded_metadata = version_metadata_manager.load_metadata("1.0")
    print(f"Loaded metadata: {loaded_metadata}")

    # Update metadata for version 1.0
    updated_metadata = {"accuracy": 0.96}
    version_metadata_manager.update_metadata("1.0", updated_metadata)

    # Delete metadata for version 1.0
    version_metadata_manager.delete_metadata("1.0")
