from abc import ABC, abstractmethod
import torch.nn as nn

class BaseModel(nn.Module, ABC):
    def __init__(self):
        """
        Initializes the base model, serving as an abstract foundation for other models in the decentralized AI system.
        """
        super(BaseModel, self).__init__()

    @abstractmethod
    def forward(self, x):
        """
        Defines the computation performed at every call of the model.
        This method should be overridden by all subclasses.
        :param x: Input tensor to the model.
        """
        pass

    @abstractmethod
    def get_model_info(self):
        """
        Returns information about the model such as its architecture and the number of parameters.
        :return: A dictionary containing model information.
        """
        pass

    def get_num_parameters(self) -> int:
        """
        Returns the number of learnable parameters in the model.
        :return: The total number of learnable parameters.
        """
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

# Example usage of inheritance
class ExampleModel(BaseModel):
    def __init__(self):
        super(ExampleModel, self).__init__()
        self.layer1 = nn.Linear(10, 5)
        self.layer2 = nn.Linear(5, 1)

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        return x

    def get_model_info(self):
        return {
            "model_name": "ExampleModel",
            "num_parameters": self.get_num_parameters()
        }

# Example usage
if __name__ == "__main__":
    model = ExampleModel()
    print(model.get_model_info())
