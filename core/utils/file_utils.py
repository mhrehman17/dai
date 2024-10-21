import os
import json
import logging
import shutil
from typing import Any

class FileUtils:
    def __init__(self, logger: logging.Logger = None):
        """
        Initializes FileUtils to handle common file operations.
        :param logger: Logger instance to log file operations.
        """
        self.logger = logger or logging.getLogger(__name__)

    def write_json(self, filepath: str, data: Any, indent: int = 4):
        """
        Writes a dictionary or list to a JSON file.
        :param filepath: Path where JSON file should be saved.
        :param data: Data to write to the file.
        :param indent: Indentation level for JSON file.
        """
        try:
            with open(filepath, 'w') as json_file:
                json.dump(data, json_file, indent=indent)
            self.logger.info(f"JSON data successfully written to {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to write JSON data to {filepath}: {e}")

    def read_json(self, filepath: str) -> Any:
        """
        Reads a JSON file and returns the data.
        :param filepath: Path to the JSON file.
        :return: Data read from the file.
        """
        if not os.path.exists(filepath):
            self.logger.error(f"JSON file {filepath} not found.")
            raise FileNotFoundError(f"JSON file {filepath} not found.")
        try:
            with open(filepath, 'r') as json_file:
                data = json.load(json_file)
            self.logger.info(f"JSON data successfully read from {filepath}")
            return data
        except Exception as e:
            self.logger.error(f"Failed to read JSON data from {filepath}: {e}")
            raise

    def create_directory(self, dir_path: str):
        """
        Creates a directory if it does not already exist.
        :param dir_path: Path of the directory to create.
        """
        try:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                self.logger.info(f"Directory created at {dir_path}")
            else:
                self.logger.info(f"Directory already exists at {dir_path}")
        except Exception as e:
            self.logger.error(f"Failed to create directory at {dir_path}: {e}")
            raise

    def delete_file(self, filepath: str):
        """
        Deletes a file from the filesystem.
        :param filepath: Path of the file to delete.
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                self.logger.info(f"File {filepath} successfully deleted.")
            else:
                self.logger.warning(f"File {filepath} not found.")
        except Exception as e:
            self.logger.error(f"Failed to delete file {filepath}: {e}")
            raise

    def backup_file(self, filepath: str, backup_dir: str = './backups'):
        """
        Creates a backup of the specified file in the backup directory.
        :param filepath: Path of the file to back up.
        :param backup_dir: Directory where the backup should be saved.
        """
        try:
            if not os.path.exists(filepath):
                self.logger.error(f"File {filepath} not found for backup.")
                raise FileNotFoundError(f"File {filepath} not found for backup.")

            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
                self.logger.info(f"Backup directory created at {backup_dir}")

            backup_filepath = os.path.join(backup_dir, os.path.basename(filepath))
            shutil.copy(filepath, backup_filepath)
            self.logger.info(f"File {filepath} successfully backed up to {backup_filepath}")
        except Exception as e:
            self.logger.error(f"Failed to back up file {filepath}: {e}")
            raise

    def restore_file(self, backup_filepath: str, restore_dir: str = './'):
        """
        Restores a backup file to the specified directory.
        :param backup_filepath: Path of the backup file to restore.
        :param restore_dir: Directory where the file should be restored.
        """
        try:
            if not os.path.exists(backup_filepath):
                self.logger.error(f"Backup file {backup_filepath} not found for restoration.")
                raise FileNotFoundError(f"Backup file {backup_filepath} not found for restoration.")

            if not os.path.exists(restore_dir):
                os.makedirs(restore_dir)
                self.logger.info(f"Restore directory created at {restore_dir}")

            restore_filepath = os.path.join(restore_dir, os.path.basename(backup_filepath))
            shutil.copy(backup_filepath, restore_filepath)
            self.logger.info(f"Backup file {backup_filepath} successfully restored to {restore_filepath}")
        except Exception as e:
            self.logger.error(f"Failed to restore file {backup_filepath}: {e}")
            raise

# Example usage
if __name__ == "__main__":
    # Set up logger
    file_logger = logging.getLogger("file_utils")
    file_logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_logger.addHandler(console_handler)

    # Initialize FileUtils with the logger
    file_utils = FileUtils(logger=file_logger)

    # Example operations
    test_data = {"name": "test", "value": 42}
    file_utils.write_json("./test.json", test_data)
    read_data = file_utils.read_json("./test.json")
    print(f"Read data: {read_data}")

    # Create directory
    file_utils.create_directory("./test_dir")

    # Backup file
    file_utils.backup_file("./test.json")

    # Restore file
    file_utils.restore_file("./backups/test.json", "./restored")

    # Delete file
    file_utils.delete_file("./test.json")