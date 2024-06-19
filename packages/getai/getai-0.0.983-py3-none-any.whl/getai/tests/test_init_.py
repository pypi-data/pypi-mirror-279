# tests/test_init_.py

import pytest


def test_imports():
    """Test that all imports are working."""
    from getai import (
        search_datasets,
        download_dataset,
        search_models,
        download_model,
        get_hf_token,
        hf_login,
        SessionManager,
    )

    assert search_datasets is not None
    assert download_dataset is not None
    assert search_models is not None
    assert download_model is not None
    assert get_hf_token is not None
    assert hf_login is not None
    assert SessionManager is not None


def test_all_variable():
    """Test that __all__ variable is correctly set."""
    from getai import __all__

    expected_all = [
        "search_datasets",
        "download_dataset",
        "search_models",
        "download_model",
        "get_hf_token",
        "hf_login",
        "SessionManager",
    ]
    assert sorted(__all__) == sorted(expected_all)
