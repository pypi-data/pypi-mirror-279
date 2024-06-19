# test_script_execution.py
import unittest
import subprocess
import sys
import os
from unittest.mock import patch, MagicMock


class TestScriptExecution(unittest.TestCase):
    @patch("getai.utils.get_hf_token", return_value="mock_token")
    @patch("subprocess.run")
    def test_main_execution(self, mock_subprocess_run, mock_get_hf_token):
        # Mock the return value of subprocess.run
        mock_completed_process = MagicMock()
        mock_completed_process.returncode = 0
        mock_completed_process.stderr = "INFO: Script executed successfully"
        mock_subprocess_run.return_value = mock_completed_process

        script_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "getai", "__main__.py")
        )

        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            check=True,  # Ensure an exception is raised for non-zero exit status
        )

        # Ensure subprocess.run was called once
        mock_subprocess_run.assert_called_once_with(
            [sys.executable, script_path], capture_output=True, text=True, check=True
        )

        # Check the mocked return values
        self.assertEqual(result.returncode, 0)
        self.assertIn("INFO: Script executed successfully", result.stderr)


if __name__ == "__main__":
    unittest.main()
