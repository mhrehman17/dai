import torch
from torch.utils.data import Dataset, DataLoader, Subset
from typing import List

class DataSharder:
    def __init__(self, dataset: Dataset, num_shards: int):
        """
        Initializes the DataSharder, which shards the dataset into smaller subsets.
        :param dataset: The dataset to be sharded.
        :param num_shards: Number of shards to split the dataset into.
        """
        self.dataset = dataset
        self.num_shards = num_shards

    def create_shards(self) -> List[Subset]:
        """
        Creates shards from the dataset.
        :return: A list of Subset objects representing the shards.
        """
        dataset_size = len(self.dataset)
        shard_size = dataset_size // self.num_shards
        indices = torch.randperm(dataset_size).tolist()  # Randomly shuffle dataset indices

        shards = []
        for i in range(self.num_shards):
            start_idx = i * shard_size
            end_idx = (i + 1) * shard_size if i != self.num_shards - 1 else dataset_size
            shard_indices = indices[start_idx:end_idx]
            shards.append(Subset(self.dataset, shard_indices))
        
        return shards

    def get_shard_loaders(self, batch_size: int = 32) -> List[DataLoader]:
        """
        Creates DataLoaders for each shard with the specified batch size.
        :param batch_size: Batch size for DataLoaders.
        :return: A list of DataLoaders, each corresponding to a shard.
        """
        shards = self.create_shards()
        shard_loaders = [DataLoader(shard, batch_size=batch_size, shuffle=True) for shard in shards]
        return shard_loaders

# Example usage
if __name__ == "__main__":
    from torchvision import datasets, transforms

    # Load the MNIST dataset
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
    mnist_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)

    # Initialize DataSharder to create 5 shards
    data_sharder = DataSharder(dataset=mnist_dataset, num_shards=5)
    shard_loaders = data_sharder.get_shard_loaders(batch_size=32)

    # Display shard details
    for shard_idx, shard_loader in enumerate(shard_loaders):
        print(f"Shard {shard_idx + 1}: Number of batches: {len(shard_loader)}")
        for batch_idx, (data, target) in enumerate(shard_loader):
            print(f"  Batch {batch_idx + 1}: Data shape: {data.shape}, Target shape: {target.shape}")
            if batch_idx == 1:  # Display first two batches only
                break
