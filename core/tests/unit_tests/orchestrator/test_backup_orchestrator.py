import unittest
from unittest.mock import MagicMock, patch
from core.orchestrator.decentralized_orchestrator import DecentralizedOrchestrator
from core.agents.training_agent import TrainingAgent
from core.orchestrator.backup_orchestrator import BackupOrchestrator  # Assuming the original code is saved as backup_orchestrator.py
import time

class TestBackupOrchestrator(unittest.TestCase):

    def setUp(self):
        """Set up common test assets."""
        self.primary_orchestrator = MagicMock(spec=DecentralizedOrchestrator)
        self.primary_orchestrator.tasks = {
            "task_1": {"description": "Test task 1", "agents": ["agent_1"], "status": "in_progress"},
            "task_2": {"description": "Test task 2", "agents": ["agent_2"], "status": "completed"},
        }
        self.backup_orchestrator = BackupOrchestrator(primary_orchestrator=self.primary_orchestrator)

    @patch.object(BackupOrchestrator, 'check_primary_status')
    @patch.object(BackupOrchestrator, 'take_over_tasks')
    def test_monitor_primary(self, mock_take_over_tasks, mock_check_primary_status):
        """Test that the backup orchestrator monitors the primary orchestrator and takes over when it fails."""
        mock_check_primary_status.side_effect = [True, False]  # First active, then inactive

        self.backup_orchestrator.monitor_interval = 1
        with patch.object(self.backup_orchestrator, 'monitor_primary', wraps=self.backup_orchestrator.monitor_primary):
            self.backup_orchestrator.is_primary_active = True
            time.sleep(2)  # Allow time for the monitoring loop to run at least once
            mock_take_over_tasks.assert_called_once()
        self.assertFalse(self.backup_orchestrator.is_primary_active, "Backup should detect primary as inactive.")

    @patch.object(BackupOrchestrator, 'check_primary_status')
    def test_check_primary_status(self, mock_check_primary_status):
        """Test the check_primary_status method for different primary statuses."""
        # Mock different return values
        mock_check_primary_status.return_value = True
        status = self.backup_orchestrator.check_primary_status()
        self.assertTrue(status, "Primary orchestrator should be active.")

        mock_check_primary_status.return_value = False
        status = self.backup_orchestrator.check_primary_status()
        self.assertFalse(status, "Primary orchestrator should be inactive.")

    @patch.object(BackupOrchestrator, 'check_primary_status')
    def test_take_over_tasks(self, mock_check_primary_status):
        """Test that the backup orchestrator takes over tasks correctly when the primary orchestrator fails."""
        mock_check_primary_status.return_value = False  # Assume primary is down

        # Simulate calling take_over_tasks
        self.backup_orchestrator.take_over_tasks()

        # Ensure task 1 is reassigned (task 2 is completed, so it should not be reassigned)
        self.assertIn("task_1", self.backup_orchestrator.backup_tasks, "Task 1 should be taken over by backup orchestrator.")
        self.assertNotIn("task_2", self.backup_orchestrator.backup_tasks, "Completed tasks should not be reassigned.")
        task_1_status = self.backup_orchestrator.backup_tasks["task_1"]
        self.assertEqual(task_1_status["status"], "completed", "Task 1 should be marked as completed by the backup orchestrator.")

    def test_get_backup_task_status(self):
        """Test the get_backup_task_status method for valid and invalid task IDs."""
        # Simulate taking over a task
        self.backup_orchestrator.backup_tasks = {
            "task_1": {"description": "Test task 1", "agents": ["agent_1"], "status": "completed"}
        }

        task_status = self.backup_orchestrator.get_backup_task_status("task_1")
        self.assertEqual(task_status["status"], "completed", "Task status should be 'completed'.")

        invalid_task_status = self.backup_orchestrator.get_backup_task_status("task_999")
        self.assertEqual(invalid_task_status, {}, "Invalid task ID should return an empty dictionary.")

    @patch('threading.Thread.start')
    def test_thread_starts_on_init(self, mock_thread_start):
        """Test that the monitoring thread starts upon initializing the BackupOrchestrator."""
        BackupOrchestrator(primary_orchestrator=self.primary_orchestrator)
        mock_thread_start.assert_called_once()

if __name__ == "__main__":
    unittest.main()
