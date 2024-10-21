import torch
from core.models.registry.model_registry import ModelRegistry
from core.models.base_model import BaseModel
from torch.utils.data import DataLoader
from typing import Dict

class ModelEvaluation:
    def __init__(self, model_registry: ModelRegistry):
        """
        Initializes the ModelEvaluation class, which is responsible for evaluating different versions of models.
        :param model_registry: The model registry instance to interact with.
        """
        self.model_registry = model_registry

    def evaluate(self, model: BaseModel, data_loader: DataLoader) -> Dict[str, float]:
        """
        Evaluates the performance of the model on the provided dataset.
        :param model: The model to evaluate.
        :param data_loader: DataLoader containing the evaluation dataset.
        :return: A dictionary containing evaluation metrics.
        """
        model.eval()
        total_correct = 0
        total_samples = 0
        loss_fn = torch.nn.CrossEntropyLoss()
        total_loss = 0.0

        with torch.no_grad():
            for data, target in data_loader:
                output = model(data)
                loss = loss_fn(output, target)
                total_loss += loss.item()
                predictions = torch.argmax(output, dim=1)
                total_correct += (predictions == target).sum().item()
                total_samples += target.size(0)

        accuracy = total_correct / total_samples
        avg_loss = total_loss / len(data_loader)

        metrics = {
            "accuracy": accuracy,
            "average_loss": avg_loss
        }
        print(f"Evaluation Metrics - Accuracy: {accuracy:.4f}, Average Loss: {avg_loss:.4f}")
        return metrics

    def compare_versions(self, version_a: str, version_b: str, data_loader: DataLoader) -> str:
        """
        Compares two versions of the model by evaluating them and comparing their metrics.
        :param version_a: Version identifier of the first model.
        :param version_b: Version identifier of the second model.
        :param data_loader: DataLoader containing the evaluation dataset.
        :return: A string indicating which version performs better.
        """
        model_a = self.model_registry.load_model(BaseModel(), version_a)
        model_b = self.model_registry.load_model(BaseModel(), version_b)

        if not model_a or not model_b:
            raise ValueError(f"One or both versions ({version_a}, {version_b}) could not be loaded.")

        metrics_a = self.evaluate(model_a, data_loader)
        metrics_b = self.evaluate(model_b, data_loader)

        if metrics_a["accuracy"] > metrics_b["accuracy"]:
            result = f"Version {version_a} outperforms version {version_b}."
        elif metrics_a["accuracy"] < metrics_b["accuracy"]:
            result = f"Version {version_b} outperforms version {version_a}."
        else:
            result = f"Both versions {version_a} and {version_b} have similar performance."

        print(result)
        return result

# Example usage
if __name__ == "__main__":
    from core.models.mnist_model import MNISTModel
    from torchvision import datasets, transforms
    from torch.utils.data import DataLoader

    # Initialize model, registry, and evaluation instance
    registry = ModelRegistry()
    evaluator = ModelEvaluation(model_registry=registry)

    # Create data loader for evaluation
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
    test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    # Evaluate a specific version of the model
    mnist_model = MNISTModel()
    registry.save_model(mnist_model, version="1.0", description="Initial MNIST model version")
    loaded_model = registry.load_model(mnist_model, "1.0")
    if loaded_model:
        evaluator.evaluate(loaded_model, test_loader)

    # Compare two versions of the model
    version_a = "1.0"
    version_b = "2.0"  # Assume version 2.0 has been trained and saved earlier
    try:
        evaluator.compare_versions(version_a, version_b, test_loader)
    except ValueError as e:
        print(e)
