import pytest
from getai.core.dataset_search import AsyncDatasetSearch
from getai.core.dataset_downloader import AsyncDatasetDownloader
from getai.core.model_search import AsyncModelSearch
from getai.core.model_downloader import AsyncModelDownloader


@pytest.mark.asyncio
async def test_async_dataset_search():
    searcher = AsyncDatasetSearch(
        query="test",
        filtered_datasets=[],
        total_datasets=0,
        output_dir=None,
        max_connections=5,
        hf_token=None,
        session=None,
    )
    result = await searcher.search_datasets(query="test")
    assert result is not None


@pytest.mark.asyncio
async def test_async_dataset_downloader():
    downloader = AsyncDatasetDownloader(
        session=None, output_dir=None, max_connections=5, hf_token=None
    )
    result = await downloader.download_dataset_info(dataset_id="test")
    assert result is not None


@pytest.mark.asyncio
async def test_async_model_search():
    searcher = AsyncModelSearch(
        query="test", session=None, max_connections=5, hf_token=None
    )
    result = await searcher.search_models(query="test")
    assert result is not None


@pytest.mark.asyncio
async def test_async_model_downloader():
    downloader = AsyncModelDownloader(
        session=None, max_retries=5, output_dir=None, max_connections=5, hf_token=None
    )
    result = await downloader.download_model(model_id="test_model", branch="main")
    assert result is not None
