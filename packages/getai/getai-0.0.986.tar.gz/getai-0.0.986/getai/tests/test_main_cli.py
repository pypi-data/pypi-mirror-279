# INSTRUCTION FOR DEVELOPING TESTS HERE
#
# When developing tests for async functions using asyncio and pytest, ensure the following to avoid linter errors and runtime issues:
#
# 1. Use `pytest.mark.asyncio` to mark the test as an asyncio test function.
# 2. Patch `asyncio.run` and the target async functions (`main_script.main` in this case) correctly.
# 3. Define an async function to use as a side effect for the mocked async function to ensure it is awaitable.
# 4. Ensure `asyncio.run` is properly patched to handle the coroutine.
# 5. Use `asyncio.Future` to mock the return value of async functions to ensure they are awaitable.
# 6. Avoid returning `None` directly from an async function; use an awaitable object like `asyncio.Future`.
# 7. Ensure that the function under test (`main_script.run`) properly invokes `asyncio.run(main_script.main())`.
#
# These steps ensure that both the linter and the test requirements are satisfied without causing `NoneType` errors.

import pytest
import asyncio
from unittest.mock import patch, MagicMock
import old.__main__ as main_script


@pytest.mark.asyncio
async def test_main_run():
    """
    Test the main run function for 'model' mode with 'test-model' identifier.
    This test mocks the main function and asyncio.run to check if they are called once.
    """
    print("Testing main run function with 'model' mode and 'test-model' identifier.")

    args = ["model", "test-model"]

    with patch("sys.argv", ["getai"] + args), patch(
        "getai.main.get_hf_token", return_value="fake_token"
    ), patch("getai.main.main", new_callable=MagicMock) as mock_main, patch(
        "asyncio.run", new_callable=MagicMock
    ) as mock_run:

        async def async_main():
            await asyncio.sleep(0)  # Ensure it's an awaitable coroutine
            future = asyncio.Future()
            future.set_result(None)
            return future

        mock_main.side_effect = async_main

        async def async_run(coro):
            await coro
            return asyncio.Future()

        mock_run.side_effect = async_run

        await main_script.run()  # Call run with await

        mock_run.assert_called_once()
        mock_main.assert_called_once()
