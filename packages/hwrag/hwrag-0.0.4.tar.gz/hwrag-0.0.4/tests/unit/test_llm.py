import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from hwrag.llm import OpenAILLM, OllamaLLM, LLM


class TestLLM(unittest.TestCase):
    def test__openai_chat_api(self):
        chat_api = OpenAILLM()
        chat_messages = [
            {"role": "user", "content": "你好，你怎么样？"},
        ]
        response = chat_api.make_llm_call(chat_messages)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test__ollama_chat_api(self):
        chat_api = OllamaLLM(base_url=os.getenv("OLLAMA_BASE_URL"))
        chat_messages = [
            {"role": "user", "content": "今天天气怎么样？"},
        ]
        response = chat_api.make_llm_call(chat_messages)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test__save_and_load_from_dict(self):
        chat_api = OpenAILLM(temperature=0.5, max_tokens=2000)
        config = chat_api.to_dict()
        chat_api_loaded = LLM.from_dict(config)
        self.assertEqual(chat_api_loaded.model, chat_api.model)
        self.assertEqual(chat_api_loaded.temperature, chat_api.temperature)
        self.assertEqual(chat_api_loaded.max_tokens, chat_api.max_tokens)


if __name__ == "__main__":
    unittest.main()
