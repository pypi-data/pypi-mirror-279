import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from hwrag.embedding import Embedding

embeddings = [
    Embedding.from_dict(
        {
            "subclass_name": "OpenAIEmbedding",
            "model": "text-embedding-3-small",
        }
    ),
    Embedding.from_dict(
        {
            "subclass_name": "OllamaEmbedding",
            "model": "nomic-embed-text",
            "base_url": os.getenv("OLLAMA_BASE_URL"),
        }
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("embedding", embeddings)
async def test_embedding(embedding: Embedding):
    query = "话多之人，总是试图隐藏什么；沉默之人，心里肯定坚信着什么。"
    vector = embedding.embed_query(query)
    assert isinstance(vector, list)

    from hwrag.embedding import OpenAIEmbedding, OllamaEmbedding

    if isinstance(embedding, OpenAIEmbedding):
        assert len(vector) == 1536
    if isinstance(embedding, OllamaEmbedding):
        assert len(vector) == 768


if __name__ == "__main__":
    pytest.main()
