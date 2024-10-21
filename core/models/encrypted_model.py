import torch
import torch.nn as nn
import torch.nn.functional as F
from core.models.base_model import BaseModel
from phe import paillier  # Using Paillier encryption library for homomorphic encryption

class EncryptedModel(BaseModel):
    def __init__(self):
        """
        Initializes an encrypted model that can work with homomorphically encrypted data.
        The model consists of two fully connected layers and uses homomorphic encryption for secure data processing.
        """
        super(EncryptedModel, self).__init__()
        self.fc1 = nn.Linear(784, 128)
        self.fc2 = nn.Linear(128, 10)

        # Encryption-related attributes
        self.public_key, self.private_key = paillier.generate_paillier_keypair()
        self.encrypted_weights = None

    def encrypt_weights(self):
        """
        Encrypts the model weights using Paillier homomorphic encryption.
        This allows the model to securely store its parameters.
        """
        self.encrypted_weights = [
            self.public_key.encrypt(float(param.data.mean())) for param in self.parameters() if param.requires_grad
        ]
        print("Model weights encrypted successfully.")

    def decrypt_weights(self):
        """
        Decrypts the encrypted model weights.
        This is primarily for verification or auditing purposes.
        """
        if self.encrypted_weights is None:
            raise ValueError("No encrypted weights available to decrypt.")
        decrypted_weights = [
            self.private_key.decrypt(weight) for weight in self.encrypted_weights
        ]
        print(f"Decrypted Weights: {decrypted_weights}")
        return decrypted_weights

    def forward(self, x):
        """
        Defines the forward pass of the model.
        :param x: Input tensor to the model.
        :return: Output logits after passing through the model.
        """
        x = x.view(-1, 784)  # Flatten the tensor
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

    def get_model_info(self):
        """
        Returns information about the encrypted model such as its architecture and the number of parameters.
        :return: A dictionary containing model information.
        """
        return {
            "model_name": "EncryptedModel",
            "num_parameters": self.get_num_parameters(),
            "architecture": "2 Fully Connected Layers with Homomorphic Encryption Support"
        }

# Example usage
if __name__ == "__main__":
    model = EncryptedModel()
    print(model.get_model_info())

    # Encrypt and decrypt weights (for testing purposes)
    model.encrypt_weights()
    decrypted_weights = model.decrypt_weights()

    # Test the model with a random tensor
    x = torch.randn(1, 1, 28, 28)  # Batch size of 1, 1 channel, 28x28 image
    output = model(x)
    print("Model output shape:", output.shape)
