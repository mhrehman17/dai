import torch
import torch.nn as nn
import torch.quantization
import logging
from typing import Optional

class ModelOptimizer:
    def __init__(self, model: nn.Module, logger: Optional[logging.Logger] = None):
        """
        Initializes the ModelOptimizer for optimizing neural network models.
        :param model: The neural network model to optimize.
        :param logger: Logger instance to log optimization activities.
        """
        self.model = model
        self.logger = logger or logging.getLogger(__name__)

    def quantize_model(self) -> nn.Module:
        """
        Applies quantization to the model to reduce its size and speed up inference.
        :return: The quantized model.
        """
        try:
            self.model.eval()  # Set model to evaluation mode before quantization
            quantized_model = torch.quantization.quantize_dynamic(
                self.model, {nn.Linear}, dtype=torch.qint8
            )
            self.logger.info("Model quantization completed successfully.")
            return quantized_model
        except Exception as e:
            self.logger.error(f"Failed to quantize model: {e}")
            return self.model

    def prune_model(self, amount: float = 0.3) -> nn.Module:
        """
        Applies pruning to the model to remove less important connections, making it more efficient.
        :param amount: The proportion of connections to prune (0.0 to 1.0).
        :return: The pruned model.
        """
        try:
            self.model.train()  # Set model to training mode for pruning
            parameters_to_prune = []
            for module_name, module in self.model.named_modules():
                if isinstance(module, nn.Linear):
                    parameters_to_prune.append((module, 'weight'))

            torch.nn.utils.prune.global_unstructured(
                parameters_to_prune,
                pruning_method=torch.nn.utils.prune.L1Unstructured,
                amount=amount
            )
            self.logger.info(f"Model pruning completed successfully with amount: {amount}")
            return self.model
        except Exception as e:
            self.logger.error(f"Failed to prune model: {e}")
            return self.model

    def convert_to_onnx(self, onnx_filepath: str, input_size: tuple = (1, 28 * 28)) -> None:
        """
        Converts the model to ONNX format for deployment in different environments.
        :param onnx_filepath: Path to save the ONNX model file.
        :param input_size: The input tensor size expected by the model.
        """
        try:
            dummy_input = torch.randn(*input_size)
            torch.onnx.export(self.model, dummy_input, onnx_filepath, verbose=True)
            self.logger.info(f"Model converted to ONNX format and saved at {onnx_filepath}")
        except Exception as e:
            self.logger.error(f"Failed to convert model to ONNX format: {e}")

# Example usage
if __name__ == "__main__":
    # Set up logger
    optimizer_logger = logging.getLogger("model_optimizer")
    optimizer_logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    optimizer_logger.addHandler(console_handler)

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

    # Initialize ModelOptimizer
    model_optimizer = ModelOptimizer(model=model, logger=optimizer_logger)

    # Quantize the model
    quantized_model = model_optimizer.quantize_model()

    # Prune the model
    pruned_model = model_optimizer.prune_model(amount=0.4)

    # Convert the model to ONNX
    model_optimizer.convert_to_onnx(onnx_filepath="simple_model.onnx", input_size=(1, 28 * 28))
