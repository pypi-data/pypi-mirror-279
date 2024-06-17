from abc import ABC, abstractmethod
import os


class LLM(ABC):
    subclasses = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses[cls.__name__] = cls

    def to_dict(self):
        return {
            "subclass_name": self.__class__.__name__,
        }

    @classmethod
    def from_dict(cls, config):
        subclass_name = config.pop(
            "subclass_name", None
        )  # Remove subclass_name from config
        subclass = cls.subclasses.get(subclass_name)
        if subclass:
            return subclass(**config)  # Pass the modified config without subclass_name
        else:
            raise ValueError(f"Unknown subclass: {subclass_name}")

    @abstractmethod
    def make_llm_call(self, chat_messages: list[dict]) -> str:
        """
        Takes in chat_messages (OpenAI format) and returns the response from the LLM as a string.
        """
        pass


class OpenAILLM(LLM):
    def __init__(
        self, model: str = "gpt-4-0613", temperature: float = 0, max_tokens: int = 1000
    ):
        from openai import OpenAI

        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def make_llm_call(self, chat_messages: list[dict]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=chat_messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        llm_output = response.choices[0].message.content.strip()
        return llm_output

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update(
            {
                "model": self.model,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
            }
        )
        return base_dict


class OllamaLLM(LLM):
    def __init__(
        self,
        model: str = "qwen:7b-chat",
        temperature: float = 0.2,
        max_tokens: int = 1000,
        base_url: str = "http://localhost:11434/v1",
    ):
        from openai import OpenAI

        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.base_url = base_url
        self.client = OpenAI(api_key="ollama", base_url=self.base_url)

    def make_llm_call(self, chat_messages: list[dict]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=chat_messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        llm_output = response.choices[0].message.content.strip()
        return llm_output

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update(
            {
                "model": self.model,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "base_url": self.base_url,
            }
        )
        return base_dict
