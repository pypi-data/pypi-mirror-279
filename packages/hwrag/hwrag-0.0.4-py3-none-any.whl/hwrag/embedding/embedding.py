from abc import ABC, abstractmethod


class Embedding(ABC):
    subclasses = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses[cls.__name__] = cls

    def to_dict(self):
        return {"subclass_name": self.__class__.__name__}

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


class OpenAIEmbedding(Embedding):
    def __init__(self, model: str = "text-embedding-3-small"):
        from langchain_openai import OpenAIEmbeddings

        self.model = model
        self._embedding = OpenAIEmbeddings(model=self.model)

    def __getattr__(self, item):
        # 当尝试访问不存在的属性时，会尝试从self._embedding获取
        return getattr(self._embedding, item)

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({"model": self.model})
        return base_dict


class OllamaEmbedding(Embedding):
    def __init__(
        self, model: str = "nomic-embed-text", base_url: str = "http://localhost:11434"
    ):
        from langchain_community.embeddings import OllamaEmbeddings

        self._embedding = OllamaEmbeddings(model=model, base_url=base_url)

    def __getattr__(self, item):
        # 当尝试访问不存在的属性时，会尝试从self._embedding获取
        return getattr(self._embedding, item)

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update(
            {"model": self._embedding.model, "base_url": self._embedding.base_url}
        )
        return base_dict


class HuggingFaceEmbedding(Embedding):
    def __init__(self, model: str = ""):
        from langchain_community.embeddings import HuggingFaceEmbeddings

        self._embedding = HuggingFaceEmbeddings(model_name=model)

    def __getattr__(self, item):
        # 当尝试访问不存在的属性时，会尝试从self._embedding获取
        return getattr(self._embedding, item)

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({"model": self._embedding.model_name})
        return base_dict


if __name__ == "__main__":  # pragma: no cover
    embedding = Embedding.from_dict(
        {
            "subclass_name": "OllamaEmbedding",
            "model": "nomic-embed-text",
            "base_url": "https://chattcm.haiweikexin.com",
        }
    )
    vector = embedding.embed_query(
        "话多之人，总是试图隐藏什么；沉默之人，心里肯定坚信着什么。"
    )
    print(len(vector))
