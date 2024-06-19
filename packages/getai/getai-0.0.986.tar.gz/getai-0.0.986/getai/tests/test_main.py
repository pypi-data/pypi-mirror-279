# test_main.py
import unittest
import asyncio
import argparse
from unittest.mock import patch
from old.main import main


class TestMain(unittest.TestCase):
    @patch("getai.main.hf_login")
    @patch("argparse.ArgumentParser.parse_args")
    def test_hf_login(self, mock_parse_args, mock_hf_login):
        # Simulate command-line arguments
        mock_parse_args.return_value = argparse.Namespace(mode=None, hf_login=True)

        # Run the main function
        asyncio.run(main())

        # Check that hf_login was called once
        mock_hf_login.assert_called_once()


if __name__ == "__main__":
    unittest.main()
