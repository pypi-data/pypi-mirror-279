import pytest
import time
from rich import print

@pytest.fixture(autouse=True)
def time_test():
    before = time.time()
    yield
    after = time.time()
    print(f"Test took {after - before:.02f} seconds!")


@pytest.fixture(autouse=True, scope="session")
def time_test():
    before = time.time()
    yield
    after = time.time()
    print(f"Test took {after - before:.02f} seconds!")


@pytest.fixture()
def mock_documennts_with_score():
    from langchain_core.documents import Document

    docs = []
    for i in range(1, 9):
        docs.append((Document(page_content=str(i), metadata={}), i / 10, i / 20))
    return docs
