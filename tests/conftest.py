import datetime
import os

import pytest

from ragxiv.datamodel import ArxivPaper
from ragxiv.logger import log_storage
from ragxiv.text import ArxivFetcher

if os.getenv("_PYTEST_RAISE", "0") != "0":

    @pytest.hookimpl(tryfirst=True)
    def pytest_exception_interact(call):
        raise call.excinfo.value

    @pytest.hookimpl(tryfirst=True)
    def pytest_internalerror(excinfo):
        raise excinfo.value


@pytest.fixture(autouse=True)
def cleared_log_storage():
    """Fixture to clear the log storage before each test."""
    log_storage.clear()
    yield log_storage


def generate_arxiv_fetcher(
    category: str = "cond-mat.str-el",
    max_results: int = 1,
    data_folder: str = "tests/data",
    fetched_arxiv_ids_file: str = "fetched_arxiv_ids.txt",
):
    return ArxivFetcher(
        category=category,
        max_results=max_results,
        data_folder=data_folder,
        fetched_arxiv_ids_file=fetched_arxiv_ids_file,
    )


def generate_arxiv_paper(id: str = "1234.5678v1"):
    return ArxivPaper(
        id=id,
        url=f"http://arxiv.org/abs/{id}",
        pdf_url=f"http://arxiv.org/pdf/{id}",
        title="Test Title",
        summary="A summary or abstract.",
        authors=[],
        comment="",
        categories=[],
        updated=datetime.datetime(2024, 4, 25, 0, 0, tzinfo=datetime.timezone.utc),
        published=datetime.datetime(2024, 4, 25, 0, 0, tzinfo=datetime.timezone.utc),
    )
