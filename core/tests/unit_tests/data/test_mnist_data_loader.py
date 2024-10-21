import unittest
from core.data.mnist_data_loader import MNISTDataLoader  # Assuming the class is saved here
from torch.utils.data import DataLoader

class TestMNISTDataLoader(unittest.TestCase):
    
    def setUp(self):
        # Initialize MNISTDataLoader with a specific batch size for testing
        self.batch_size = 64
        self.data_dir = "./data"
        self.data_loader = MNISTDataLoader(batch_size=self.batch_size, data_dir=self.data_dir)

    def test_train_loader(self):
        # Get training data loader
        train_loader = self.data_loader.get_train_loader()
        
        # Verify that the train loader is an instance of DataLoader
        self.assertIsInstance(train_loader, DataLoader)
        
        # Check the length of the dataset (at least 1 to ensure it's loaded correctly)
        self.assertGreater(len(train_loader), 0)

        # Verify the shape of the data in the first batch
        for batch_idx, (data, target) in enumerate(train_loader):
            # Check data dimensions
            self.assertEqual(data.shape[0], self.batch_size)
            self.assertEqual(data.shape[1], 1)  # Single channel (grayscale)
            self.assertEqual(data.shape[2], 28) # Height of MNIST images
            self.assertEqual(data.shape[3], 28) # Width of MNIST images
            # Check target dimensions
            self.assertEqual(target.shape[0], self.batch_size)
            break

    def test_test_loader(self):
        # Get testing data loader
        test_loader = self.data_loader.get_test_loader()
        
        # Verify that the test loader is an instance of DataLoader
        self.assertIsInstance(test_loader, DataLoader)
        
        # Check the length of the dataset (at least 1 to ensure it's loaded correctly)
        self.assertGreater(len(test_loader), 0)

        # Verify the shape of the data in the first batch
        for batch_idx, (data, target) in enumerate(test_loader):
            # Check data dimensions
            self.assertEqual(data.shape[0], self.batch_size)
            self.assertEqual(data.shape[1], 1)  # Single channel (grayscale)
            self.assertEqual(data.shape[2], 28) # Height of MNIST images
            self.assertEqual(data.shape[3], 28) # Width of MNIST images
            # Check target dimensions
            self.assertEqual(target.shape[0], self.batch_size)
            break

    def test_different_batch_sizes(self):
        # Test different batch sizes to verify proper data loading
        for batch_size in [16, 32, 128]:
            self.data_loader = MNISTDataLoader(batch_size=batch_size, data_dir=self.data_dir)
            train_loader = self.data_loader.get_train_loader()
            for data, target in train_loader:
                self.assertEqual(data.shape[0], batch_size)
                self.assertEqual(target.shape[0], batch_size)
                break  # Test only the first batch for simplicity

if __name__ == '__main__':
    unittest.main()
