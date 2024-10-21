import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np

class SyntheticDataset(Dataset):
    def __init__(self, num_samples: int = 1000, num_features: int = 20, num_classes: int = 2):
        """
        Initializes the SyntheticDataset, which generates synthetic data for testing purposes.
        :param num_samples: Number of samples in the dataset.
        :param num_features: Number of features per sample.
        :param num_classes: Number of classes for classification.
        """
        self.num_samples = num_samples
        self.num_features = num_features
        self.num_classes = num_classes

        # Generate synthetic data and labels
        self.data = np.random.randn(num_samples, num_features).astype(np.float32)
        self.labels = np.random.randint(0, num_classes, num_samples).astype(np.int64)

    def __len__(self):
        """
        Returns the total number of samples in the dataset.
        :return: The length of the dataset.
        """
        return self.num_samples

    def __getitem__(self, idx):
        """
        Retrieves a sample and its corresponding label by index.
        :param idx: Index of the sample to retrieve.
        :return: A tuple containing the sample and its label.
        """
        sample = torch.tensor(self.data[idx])
        label = torch.tensor(self.labels[idx])
        return sample, label

# Example usage
if __name__ == "__main__":
    # Initialize SyntheticDataset with 1000 samples, 20 features, and 2 classes
    synthetic_dataset = SyntheticDataset(num_samples=1000, num_features=20, num_classes=2)
    synthetic_loader = DataLoader(synthetic_dataset, batch_size=32, shuffle=True)

    # Display some data statistics
    print(f"Number of samples in dataset: {len(synthetic_dataset)}")
    print(f"Number of batches in DataLoader: {len(synthetic_loader)}")

    # Iterate over the synthetic data
    for batch_idx, (data, target) in enumerate(synthetic_loader):
        print(f"Batch {batch_idx + 1}: Data shape: {data.shape}, Target shape: {target.shape}")
        if batch_idx == 1:  # Display first two batches only
            break
