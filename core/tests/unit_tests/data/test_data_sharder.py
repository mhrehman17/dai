import unittest
import torch
from torch.utils.data import DataLoader, Dataset
from core.data.data_sharder import DataSharder  # Assuming the code is saved under core/data_sharder.py


# Mock Dataset for Testing
class MockDataset(Dataset):
    def __init__(self, size):
        self.data = torch.arange(size)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]


class TestDataSharder(unittest.TestCase):
    
    def setUp(self):
        # Set up a mock dataset of size 100 for testing
        self.dataset = MockDataset(size=100)
        self.num_shards = 5
        self.data_sharder = DataSharder(dataset=self.dataset, num_shards=self.num_shards)

    def test_create_shards(self):
        # Test if the correct number of shards are created
        shards = self.data_sharder.create_shards()
        self.assertEqual(len(shards), self.num_shards)

        # Ensure that each shard has the correct size (except potentially the last one)
        shard_sizes = [len(shard) for shard in shards]
        expected_shard_size = len(self.dataset) // self.num_shards
        for i in range(self.num_shards - 1):
            self.assertEqual(shard_sizes[i], expected_shard_size)
        # The last shard may be slightly larger if there's a remainder
        self.assertGreaterEqual(shard_sizes[-1], expected_shard_size)

    def test_shard_indices_uniqueness(self):
        # Ensure that the indices in shards are unique and cover the whole dataset
        shards = self.data_sharder.create_shards()
        all_indices = []
        for shard in shards:
            all_indices.extend(shard.indices)

        # Check if the number of unique indices is equal to dataset length and all indices are covered
        self.assertEqual(len(all_indices), len(self.dataset))
        self.assertEqual(len(set(all_indices)), len(self.dataset))

    def test_get_shard_loaders(self):
        # Test if DataLoaders are created correctly for each shard
        batch_size = 10
        shard_loaders = self.data_sharder.get_shard_loaders(batch_size=batch_size)
        
        # Ensure that each loader returns the correct batch size for most batches
        for loader in shard_loaders:
            for data in loader:
                self.assertEqual(data.shape[0], batch_size)
                break  # Only check the first batch for simplicity

    def test_loader_batch_count(self):
        # Test if DataLoader returns the expected number of batches per shard
        batch_size = 10
        shard_loaders = self.data_sharder.get_shard_loaders(batch_size=batch_size)
        
        # Calculate the expected number of batches
        expected_batches_per_shard = (len(self.dataset) // self.num_shards) // batch_size

        for loader in shard_loaders[:-1]:
            # All shards except the last should have the expected number of batches
            self.assertEqual(len(loader), expected_batches_per_shard)

        # The last shard may have more batches due to rounding
        self.assertGreaterEqual(len(shard_loaders[-1]), expected_batches_per_shard)


if __name__ == '__main__':
    unittest.main()
