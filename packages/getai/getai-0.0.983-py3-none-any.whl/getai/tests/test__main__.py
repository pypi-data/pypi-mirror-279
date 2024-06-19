# test__main__.py
import unittest
import os
import sys
import subprocess
import tracemalloc
from unittest.mock import patch, AsyncMock
import asyncio
from old.__main__ import run


# Test Passes - Dont need to modify
class TestMainModule(unittest.TestCase):
    @patch("getai.main.main", new_callable=AsyncMock)
    @patch("asyncio.run")
    def test_run(
        self, mock_asyncio_run, mock_main
    ):  # noqa: F841 # pylint: disable=unused-argument
        # Call the run function
        run()

        # Ensure the main coroutine is created and passed to asyncio.run
        mock_asyncio_run.assert_called_once()
        called_arg = mock_asyncio_run.call_args[0][0]
        self.assertTrue(asyncio.iscoroutine(called_arg))


class TestScriptExecution(unittest.TestCase):
    @patch.dict(os.environ, {"HUGGINGFACE_TOKEN": "mock_token"})
    @patch("getai.utils.get_hf_token", return_value="mock_token")
    def test_main_execution(self, mock_get_hf_token):
        tracemalloc.start()

        script_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "getai", "__main__.py")
        )

        try:
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                check=True,  # Ensure an exception is raised for non-zero exit status
            )
        except subprocess.CalledProcessError as e:
            current, peak = tracemalloc.get_traced_memory()
            print(
                f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB"
            )
            snapshot = tracemalloc.take_snapshot()
            tracemalloc.stop()
            top_stats = snapshot.statistics("lineno")
            print("Top 10 memory allocations:")
            for stat in top_stats[:10]:
                print(stat)

            # Re-raise the exception to fail the test
            raise e

        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        snapshot = tracemalloc.take_snapshot()
        tracemalloc.stop()
        top_stats = snapshot.statistics("lineno")
        print("Top 10 memory allocations:")
        for stat in top_stats[:10]:
            print(stat)

        # Ensure the script ran without raising an exception
        self.assertEqual(result.returncode, 0)
        # Check for specific output or log entries to ensure script execution
        self.assertIn("INFO", result.stderr)


if __name__ == "__main__":
    unittest.main()
