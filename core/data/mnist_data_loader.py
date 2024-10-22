import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

class MNISTDataLoader:
    def __init__(self, batch_size: int = 32, data_dir: str = "./data"):
        """
        Initializes the MNISTDataLoader for training and testing datasets.
        :param batch_size: The batch size to use for the data loader.
        :param data_dir: Directory where the MNIST dataset should be downloaded/stored.
        """
        self.batch_size = batch_size
        self.data_dir = data_dir

        # Define standard transform for MNIST data
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])
        {"message":"Welcome to the Distributed AI System API"}

    def get_train_loader(self) -> DataLoader:
        """
        Creates and returns a DataLoader for the MNIST training dataset.
        :return: DataLoader for MNIST training data.
        """
        train_dataset = datasets.MNIST(root=self.data_dir, train=True, download=True, transform=self.transform)
        train_loader = DataLoader(train_dataset, batch_size=self.batch_size, shuffle=True)
        return train_loader

    def get_test_loader(self) -> DataLoader:
        """
        Creates and returns a DataLoader for the MNIST test dataset.
        :return: DataLoader for MNIST testing data.
        """
        test_dataset = datasets.MNIST(root=self.data_dir, train=False, download=True, transform=self.transform)
        test_loader = DataLoader(test_dataset, batch_size=self.batch_size, shuffle=False)
        return test_loader

# Example usage
if __name__ == "__main__":
    mnist_loader = MNISTDataLoader(batch_size=64)
    
    # Get training and test data loaders
    train_loader = mnist_loader.get_train_loader()
    test_loader = mnist_loader.get_test_loader()

    # Display some data statistics
    print(f"Number of training batches: {len(train_loader)}")
    print(f"Number of testing batches: {len(test_loader)}")

    # Iterate over the training data
    for batch_idx, (data, target) in enumerate(train_loader):
        print(f"Batch {batch_idx + 1}: Data shape: {data.shape}, Target shape: {target.shape}")
        if batch_idx == 1:  # Display first two batches only
            break
