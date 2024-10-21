# mnist_model.py
import unittest
from models.mnist_model import MnistModel

class TestMnistModel(unittest.TestCase):
    def setUp(self):
        self.model = MnistModel()

    def test_forward_pass(self):
        input_data = [0.1, 0.2, 0.3]  # Sample input data
        output = self.model.forward(input_data)
        self.assertIsNotNone(output)  # Verify forward pass produces output

    def test_parameter_initialization(self):
        self.model.initialize_parameters()
        self.assertIsNotNone(self.model.parameters)  # Verify parameters are initialized

    def test_mode_switch(self):
        self.model.set_mode('evaluation')
        self.assertEqual(self.model.mode, 'evaluation')  # Verify model switches to evaluation mode
        self.model.set_mode('training')
        self.assertEqual(self.model.mode, 'training')  # Verify model switches to training mode

    def test_evaluation(self):
        evaluation_result = self.model.evaluate([0.1, 0.2, 0.3])  # Mock input data
        self.assertIsNotNone(evaluation_result)  # Verify evaluation runs successfully

if __name__ == '__main__':
    unittest.main()

