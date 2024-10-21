import os
import torch
import logging
from core.models.base_model import BaseModel

class CheckpointingUtils:
    def __init__(self, checkpoint_dir: str = './checkpoints', logger: logging.Logger = None):
        """
        Initializes the CheckpointingUtils for saving and loading model checkpoints.
        :param checkpoint_dir: Directory where checkpoints should be saved.
        :param logger: Logger instance to log checkpointing information.
        """
        self.checkpoint_dir = checkpoint_dir
        if not os.path.exists(self.checkpoint_dir):
            os.makedirs(self.checkpoint_dir)
            print(f"Checkpoint directory created at {self.checkpoint_dir}")
        self.logger = logger or logging.getLogger(__name__)

    def save_checkpoint(self, model: BaseModel, optimizer: torch.optim.Optimizer, epoch: int, filename: str):
        """
        Saves a checkpoint of the model's state, including optimizer information.
        :param model: The model instance to save.
        :param optimizer: The optimizer instance to save.
        :param epoch: The current epoch number.
        :param filename: The filename to save the checkpoint as.
        """
        checkpoint_path = os.path.join(self.checkpoint_dir, filename)
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict()
        }, checkpoint_path)
        self.logger.info(f"Checkpoint saved at {checkpoint_path} for epoch {epoch}")

    def load_checkpoint(self, model: BaseModel, optimizer: torch.optim.Optimizer, filename: str) -> int:
        """
        Loads a checkpoint and restores the model and optimizer state.
        :param model: The model instance to restore.
        :param optimizer: The optimizer instance to restore.
        :param filename: The filename of the checkpoint to load.
        :return: The epoch number of the loaded checkpoint.
        """
        checkpoint_path = os.path.join(self.checkpoint_dir, filename)
        if not os.path.exists(checkpoint_path):
            self.logger.error(f"Checkpoint {checkpoint_path} not found.")
            raise FileNotFoundError(f"Checkpoint {checkpoint_path} not found.")
        
        checkpoint = torch.load(checkpoint_path)
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        epoch = checkpoint['epoch']
        
        self.logger.info(f"Checkpoint loaded from {checkpoint_path}, resuming from epoch {epoch}")
        return epoch

# Example usage
if __name__ == "__main__":
    import torch.nn as nn
    import torch.optim as optim
    from core.models.mnist_model import MNISTModel
    from core.utils.log_utils import LogUtils

    # Set up logger
    checkpoint_logger = LogUtils.setup_logger(name="checkpoint_manager", level=logging.INFO)

    # Initialize the checkpointing utility
    checkpoint_utils = CheckpointingUtils(logger=checkpoint_logger)

    # Initialize model and optimizer
    model = MNISTModel()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Save a checkpoint
    checkpoint_utils.save_checkpoint(model, optimizer, epoch=5, filename="mnist_epoch_5.pth")

    # Load the checkpoint
    restored_epoch = checkpoint_utils.load_checkpoint(model, optimizer, filename="mnist_epoch_5.pth")
    print(f"Resumed training from epoch {restored_epoch}")