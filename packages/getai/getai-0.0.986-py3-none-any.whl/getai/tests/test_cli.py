import subprocess


def test_search_datasets():
    result = subprocess.run(
        ["python", "-m", "getai.cli.main", "search-datasets", "test"],
        capture_output=True,
    )
    assert result.returncode == 0


def test_download_dataset():
    result = subprocess.run(
        ["python", "-m", "getai.cli.main", "download-dataset", "test_dataset"],
        capture_output=True,
    )
    assert result.returncode == 0


def test_search_models():
    result = subprocess.run(
        ["python", "-m", "getai.cli.main", "search-models", "test"], capture_output=True
    )
    assert result.returncode == 0


def test_download_model():
    result = subprocess.run(
        ["python", "-m", "getai.cli.main", "download-model", "test_model"],
        capture_output=True,
    )
    assert result.returncode == 0
