import torch
import torch.nn as nn
import torch.quantization
import logging
from typing import Optional

class ModelQuantizer:
    def __init__(self, model: nn.Module, logger: Optional[logging.Logger] = None):
        """
        Initializes the ModelQuantizer for applying quantization techniques to neural network models.
        :param model: The neural network model to quantize.
        :param logger: Logger instance to log quantization activities.
        """
        self.model = model
        self.logger = logger or logging.getLogger(__name__)

    def apply_dynamic_quantization(self) -> nn.Module:
        """
        Applies dynamic quantization to the model, which reduces the model size and improves inference speed.
        :return: The quantized model.
        """
        try:
            self.model.eval()  # Set model to evaluation mode before quantization
            quantized_model = torch.quantization.quantize_dynamic(
                self.model, {nn.Linear}, dtype=torch.qint8
            )
            self.logger.info("Dynamic quantization completed successfully.")
            return quantized_model
        except Exception as e:
            self.logger.error(f"Failed to apply dynamic quantization: {e}")
            return self.model

    def apply_static_quantization(self, calibration_data: torch.utils.data.DataLoader) -> nn.Module:
        """
        Applies static quantization to the model using calibration data.
        :param calibration_data: DataLoader containing data for calibration.
        :return: The statically quantized model.
        """
        try:
            # Prepare the model for quantization
            self.model.eval()
            self.model.qconfig = torch.quantization.get_default_qconfig('fbgemm')
            torch.quantization.prepare(self.model, inplace=True)
            
            # Calibrate the model with the calibration data
            with torch.no_grad():
                for inputs, _ in calibration_data:
                    self.model(inputs)
            
            # Convert the model to quantized version
            torch.quantization.convert(self.model, inplace=True)
            self.logger.info("Static quantization completed successfully.")
            return self.model
        except Exception as e:
            self.logger.error(f"Failed to apply static quantization: {e}")
            return self.model

    def apply_qat(self, train_loader: torch.utils.data.DataLoader, epochs: int = 5) -> nn.Module:
        """
        Applies Quantization-Aware Training (QAT) to the model, optimizing it for quantization during training.
        :param train_loader: DataLoader for training data used during QAT.
        :param epochs: Number of epochs to run QAT.
        :return: The quantized model after QAT.
        """
        try:
            # Set QAT configuration and prepare the model for QAT
            self.model.train()
            self.model.qconfig = torch.quantization.get_default_qat_qconfig('fbgemm')
            torch.quantization.prepare_qat(self.model, inplace=True)
            
            # Train the model using QAT
            optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
            criterion = nn.CrossEntropyLoss()
            for epoch in range(epochs):
                running_loss = 0.0
                for inputs, labels in train_loader:
                    optimizer.zero_grad()
                    outputs = self.model(inputs)
                    loss = criterion(outputs, labels)
                    loss.backward()
                    optimizer.step()
                    running_loss += loss.item()
                avg_loss = running_loss / len(train_loader)
                self.logger.info(f"Epoch [{epoch + 1}/{epochs}], Loss: {avg_loss:.4f}")

            # Convert the trained model to quantized version
            self.model.eval()
            torch.quantization.convert(self.model, inplace=True)
            self.logger.info("Quantization-Aware Training (QAT) completed successfully.")
            return self.model
        except Exception as e:
            self.logger.error(f"Failed to apply Quantization-Aware Training (QAT): {e}")
            return self.model

# Example usage
if __name__ == "__main__":
    # Set up logger
    quantizer_logger = logging.getLogger("model_quantizer")
    quantizer_logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    quantizer_logger.addHandler(console_handler)

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

    # Initialize ModelQuantizer
    model_quantizer = ModelQuantizer(model=model, logger=quantizer_logger)

    # Apply dynamic quantization
    quantized_model = model_quantizer.apply_dynamic_quantization()

    # Placeholder DataLoader for demonstration
    calibration_loader = torch.utils.data.DataLoader([])  # Replace with actual calibration data
    train_loader = torch.utils.data.DataLoader([])  # Replace with actual training data

    # Apply static quantization
    statically_quantized_model = model_quantizer.apply_static_quantization(calibration_loader)

    # Apply Quantization-Aware Training (QAT)
    qat_model = model_quantizer.apply_qat(train_loader, epochs=3)
