import torch
import torch.nn as nn
import torch.nn.functional as F
from core.models.base_model import BaseModel

class MNISTModel(BaseModel):
    def __init__(self):
        """
        Initializes the MNIST-specific model architecture.
        The model consists of two convolutional layers followed by two fully connected layers.
        """
        super(MNISTModel, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        """
        Defines the forward pass of the model.
        :param x: Input tensor to the model.
        :return: Output logits after passing through the model.
        """
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2, 2)
        x = x.view(-1, 64 * 7 * 7)  # Flatten the tensor
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

    def get_model_info(self):
        """
        Returns information about the MNIST model such as its architecture and the number of parameters.
        :return: A dictionary containing model information.
        """
        return {
            "model_name": "MNISTModel",
            "num_parameters": self.get_num_parameters(),
            "architecture": "2 Conv Layers, 2 Fully Connected Layers"
        }

# Example usage
if __name__ == "__main__":
    model = MNISTModel()
    print(model.get_model_info())

    # Test the model with a random tensor
    x = torch.randn(1, 1, 28, 28)  # Batch size of 1, 1 channel, 28x28 image
    output = model(x)
    print("Model output shape:", output.shape)
