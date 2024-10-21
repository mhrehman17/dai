import torch
import torch.nn as nn
import torch.nn.functional as F
from core.models.base_model import BaseModel

class PersonalizedModel(BaseModel):
    def __init__(self, personalization_factor: int = 128):
        """
        Initializes a personalized model architecture designed for federated learning with individualized adaptations.
        The model consists of two convolutional layers followed by two fully connected layers, with an optional
        personalization layer to adapt the model to each specific client.
        :param personalization_factor: Size of the personalization layer to adapt the model to each client's requirements.
        """
        super(PersonalizedModel, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.personalized_fc = nn.Linear(128, personalization_factor)
        self.fc2 = nn.Linear(personalization_factor, 10)

    def forward(self, x):
        """
        Defines the forward pass of the personalized model.
        :param x: Input tensor to the model.
        :return: Output logits after passing through the model.
        """
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2, 2)
        x = x.view(-1, 64 * 7 * 7)  # Flatten the tensor
        x = F.relu(self.fc1(x))
        x = F.relu(self.personalized_fc(x))
        x = self.fc2(x)
        return x

    def get_model_info(self):
        """
        Returns information about the personalized model such as its architecture and the number of parameters.
        :return: A dictionary containing model information.
        """
        return {
            "model_name": "PersonalizedModel",
            "num_parameters": self.get_num_parameters(),
            "architecture": "2 Conv Layers, 2 Fully Connected Layers with Personalized Layer"
        }

    def apply_personalization(self, client_data):
        """
        Applies personalization by adjusting the model's weights using client-specific data.
        This method can be used to fine-tune the model for a particular client's dataset.
        :param client_data: The data specific to the client for personalization.
        """
        # Placeholder for personalization logic, such as fine-tuning on client data
        print(f"Applying personalization for client-specific data...")
        # Fine-tuning logic here (e.g., few-shot learning or parameter updates)

# Example usage
if __name__ == "__main__":
    model = PersonalizedModel(personalization_factor=64)
    print(model.get_model_info())

    # Test the model with a random tensor
    x = torch.randn(1, 1, 28, 28)  # Batch size of 1, 1 channel, 28x28 image
    output = model(x)
    print("Model output shape:", output.shape)

    # Apply personalization
    model.apply_personalization(client_data=None)  # Placeholder client data
