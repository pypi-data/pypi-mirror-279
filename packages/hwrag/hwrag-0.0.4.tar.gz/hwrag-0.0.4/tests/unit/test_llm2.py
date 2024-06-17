import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from hwrag.llm import OpenAILLM, OllamaLLM, LLM


llms = [OpenAILLM(), OllamaLLM(base_url=os.getenv("OLLAMA_BASE_URL"))]


@pytest.mark.asyncio
@pytest.mark.parametrize("llm", llms)
async def test_llm(llm: LLM):
    chat_messages = [
        {"role": "user", "content": "你好，你怎么样？"},
    ]
    response = llm.make_llm_call(chat_messages)
    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.asyncio
@pytest.mark.parametrize("llm", llms)
async def test_llm_reflection(llm: LLM):
    config = llm.to_dict()
    chat_api_loaded = LLM.from_dict(config)
    assert chat_api_loaded.model == llm.model
    assert chat_api_loaded.temperature == llm.temperature
    assert chat_api_loaded.max_tokens == llm.max_tokens


if __name__ == "__main__":
    pytest.main()
