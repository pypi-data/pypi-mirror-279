import pytest
from getai.api.datasets import search_datasets, download_dataset
from getai.api.models import search_models, download_model


@pytest.mark.asyncio
async def test_search_datasets():
    result = await search_datasets(
        query="test", hf_token="dummy_token", max_connections=5
    )
    assert result is not None


@pytest.mark.asyncio
async def test_download_dataset():
    result = await download_dataset(
        identifier="test_dataset", hf_token="dummy_token", max_connections=5
    )
    assert result is not None


@pytest.mark.asyncio
async def test_search_models():
    result = await search_models(
        query="test", hf_token="dummy_token", max_connections=5
    )
    assert result is not None


@pytest.mark.asyncio
async def test_download_model():
    result = await download_model(
        identifier="test_model",
        branch="main",
        hf_token="dummy_token",
        max_connections=5,
    )
    assert result is not None
