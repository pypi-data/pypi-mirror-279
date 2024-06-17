import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from hwrag.splitter.splitter import Splitter

splitters = [
    Splitter.from_dict(
        {
            "subclass_name": "ChineseSplitter",
            "chunk_size": 100,
        }
    ),
    Splitter.from_dict(
        {
            "subclass_name": "CharacterSplitter",
            "chunk_size": 512,
            "chunk_overlap": 10,
        }
    ),
    Splitter.from_dict(
        {
            "subclass_name": "RecursiveWithTikTokenSplitter",
            "chunk_size": 512,
            "chunk_overlap": 10,
        }
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("splitter", splitters)
async def test_splitter_reflection(splitter: Splitter):
    from hwrag.splitter import CharacterSplitter, RecursiveWithTikTokenSplitter

    config = splitter.to_dict()
    splitter_loaded = Splitter.from_dict(config)

    assert splitter_loaded.chunk_size == splitter.chunk_size

    if isinstance(splitter, CharacterSplitter) or isinstance(
        splitter, RecursiveWithTikTokenSplitter
    ):
        assert splitter_loaded.chunk_overlap == splitter.chunk_overlap
        assert splitter_loaded.chunk_size > splitter_loaded.chunk_overlap


@pytest.mark.asyncio
@pytest.mark.parametrize("splitter", splitters)
async def test_splitter(splitter: Splitter):
    from hwrag.splitter import (
        ChineseSplitter,
        CharacterSplitter,
        RecursiveWithTikTokenSplitter,
    )
    from hwrag.loader import Loader

    doc_dir = os.path.abspath("docs")
    documents = Loader(doc_dir).load()
    documents = splitter.invoke(documents)
    assert isinstance(documents, list)

    if isinstance(splitter, ChineseSplitter):
        for doc in documents:
            assert len(doc.page_content) < 100
    if isinstance(splitter, CharacterSplitter):
        for doc in documents:
            assert len(doc.page_content) < 512
    if isinstance(splitter, RecursiveWithTikTokenSplitter):
        for doc in documents:
            assert len(doc.page_content) < 512


if __name__ == "__main__":
    pytest.main()
