import unittest
from unittest.mock import patch, MagicMock
from core.agents.arm_agent import ARMTrainingAgent

class TestARMTrainingAgent(unittest.TestCase):

    @patch('platform.machine', return_value='armv7l')
    def test_initialize_on_arm_device(self, mock_machine):
        # Test initialization on an ARM-based device
        agent = ARMTrainingAgent(agent_id="arm_agent_1", description="ARM training agent for edge deployment")
        self.assertEqual(agent.agent_id, "arm_agent_1")
        self.assertTrue(agent.is_arm_device())

    @patch('platform.machine', return_value='x86_64')
    def test_initialize_on_non_arm_device_raises_error(self, mock_machine):
        # Test initialization on a non-ARM-based device raises an EnvironmentError
        with self.assertRaises(EnvironmentError) as context:
            agent = ARMTrainingAgent(agent_id="arm_agent_1", description="ARM training agent for edge deployment")
        self.assertIn("must be run on an ARM-based device", str(context.exception))

    @patch('platform.machine', return_value='armv8')
    def test_is_arm_device_true(self, mock_machine):
        # Test that the agent correctly identifies the platform as ARM
        agent = ARMTrainingAgent(agent_id="arm_agent_2", description="ARM training agent for edge deployment")
        self.assertTrue(agent.is_arm_device())

    @patch('platform.machine', return_value='x86_64')
    def test_is_arm_device_false(self, mock_machine):
        # Test that the agent correctly identifies the platform as non-ARM
        with self.assertRaises(EnvironmentError):
            agent = ARMTrainingAgent(agent_id="arm_agent_3", description="ARM training agent for edge deployment")

    @patch('time.sleep', return_value=None)  # Mock sleep to speed up test execution
    @patch('platform.machine', return_value='armv7l')
    def test_optimize_training_for_arm(self, mock_machine, mock_sleep):
        # Test that ARM-specific optimizations are applied during training
        agent = ARMTrainingAgent(agent_id="arm_agent_4", description="ARM training agent for edge deployment")
        with patch('builtins.print') as mock_print:
            agent.optimize_training_for_arm()
            mock_print.assert_any_call("Agent arm_agent_4 is applying ARM-specific optimizations for training.")

    @patch('time.sleep', return_value=None)  # Mock sleep to speed up test execution
    @patch('platform.machine', return_value='armv7l')
    def test_train_on_arm_device(self, mock_machine, mock_sleep):
        # Test training process on an ARM-based device
        agent = ARMTrainingAgent(agent_id="arm_agent_5", description="ARM training agent for edge deployment")
        with patch('builtins.print') as mock_print:
            agent.train()
            mock_print.assert_any_call("Agent arm_agent_5 is starting training on an ARM-based device...")
            calls = [call[0][0] for call in mock_print.call_args_list]
            training_complete_message = next((msg for msg in calls if "Training complete for Agent arm_agent_5 on ARM-based device in" in msg), None)
            self.assertIsNotNone(training_complete_message, "Training complete message was not printed.")

    @patch('platform.machine', return_value='armv7l')
    def test_get_status(self, mock_machine):
        # Test getting the status of the ARMTrainingAgent
        agent = ARMTrainingAgent(agent_id="arm_agent_6", description="ARM training agent for edge deployment")
        self.assertEqual(agent.get_status(), "initialized")
        agent.status = "training"
        self.assertEqual(agent.get_status(), "training")

if __name__ == '__main__':
    unittest.main()
