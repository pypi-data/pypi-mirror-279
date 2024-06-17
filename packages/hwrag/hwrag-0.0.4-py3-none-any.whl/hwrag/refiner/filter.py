from abc import ABC, abstractmethod
from langchain_core.documents import Document


class Filter(ABC):
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
    def invoke(
        self, documents: list[Document, float, float], top_k: int
    ) -> list[Document, float, float]:
        pass


class ScoreFilter(Filter):

    def __init__(self): ...

    def invoke(
        self, documents: list[Document, float, float], top_k: int
    ) -> list[Document, float, float]:
        docs = sorted(documents, key=lambda x: x[-1], reverse=True)
        return docs[:top_k]


class NoFilter(Filter):

    def __init__(self): ...

    def invoke(
        self, documents: list[Document, float, float]
    ) -> list[Document, float, float]:
        return documents
