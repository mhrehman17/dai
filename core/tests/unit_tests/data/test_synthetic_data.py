import unittest
import torch
from torch.utils.data import DataLoader
from core.data.synthetic_data import SyntheticDataset  # Assuming the class is saved here

class TestSyntheticDataset(unittest.TestCase):

    def setUp(self):
        # Initialize the SyntheticDataset with a specific number of samples, features, and classes
        self.num_samples = 1000
        self.num_features = 20
        self.num_classes = 2
        self.synthetic_dataset = SyntheticDataset(
            num_samples=self.num_samples,
            num_features=self.num_features,
            num_classes=self.num_classes
        )

    def test_dataset_length(self):
        # Verify the length of the dataset matches the number of samples
        self.assertEqual(len(self.synthetic_dataset), self.num_samples)

    def test_sample_shape(self):
        # Verify the shape of each sample matches the number of features
        sample, label = self.synthetic_dataset[0]
        self.assertEqual(sample.shape[0], self.num_features)
        self.assertIsInstance(sample, torch.Tensor)
        self.assertIsInstance(label, torch.Tensor)

    def test_label_range(self):
        # Verify that all labels are within the range [0, num_classes-1]
        for _, label in self.synthetic_dataset:
            self.assertGreaterEqual(label.item(), 0)
            self.assertLess(label.item(), self.num_classes)

    def test_data_loader(self):
        # Initialize a DataLoader with the synthetic dataset
        batch_size = 32
        synthetic_loader = DataLoader(self.synthetic_dataset, batch_size=batch_size, shuffle=True)

        # Verify that the DataLoader has the correct number of batches
        expected_num_batches = len(self.synthetic_dataset) // batch_size
        self.assertGreaterEqual(len(synthetic_loader), expected_num_batches)

        # Verify the shape of data and target for the first batch
        for batch_idx, (data, target) in enumerate(synthetic_loader):
            self.assertEqual(data.shape, (batch_size, self.num_features))
            self.assertEqual(target.shape, (batch_size,))
            break  # Test only the first batch for simplicity

    def test_data_loader_with_different_batch_size(self):
        # Test DataLoader with different batch sizes to verify proper data loading
        for batch_size in [16, 64, 128]:
            synthetic_loader = DataLoader(self.synthetic_dataset, batch_size=batch_size, shuffle=True)
            for data, target in synthetic_loader:
                self.assertEqual(data.shape[0], batch_size)
                self.assertEqual(data.shape[1], self.num_features)
                self.assertEqual(target.shape[0], batch_size)
                break  # Test only the first batch for simplicity

if __name__ == '__main__':
    unittest.main()
