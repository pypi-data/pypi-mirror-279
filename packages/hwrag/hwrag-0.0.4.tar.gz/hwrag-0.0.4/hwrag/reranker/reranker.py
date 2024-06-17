from abc import ABC, abstractmethod
from langchain_core.documents import Document


class Reranker(ABC):
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
        self, query: str, documents: list[Document, float]
    ) -> list[Document, float, float]:
        pass


class NoReranker(Reranker):
    def invoke(
        self, query: str, documents: list[Document, float]
    ) -> list[Document, float, float]:
        buffer = []
        for document, score in documents:
            buffer.append((document, score, score))
        return buffer

    def to_dict(self):
        return super().to_dict()


class BCEReranker(Reranker):

    def __init__(self, model: str = "maidalun1020/bce-reranker-base_v1"):
        self.model = model

        from sentence_transformers import CrossEncoder
        import torch

        self.reranker = CrossEncoder(
            model,
            max_length=512,
            device=torch.device("cuda" if torch.cuda.is_available() else "cpu"),
        )

    def invoke(
        self, query: str, documents: list[Document, float]
    ) -> list[Document, float, float]:
        buffer = []
        for document, score in documents:
            ranker_score = self.reranker.predict([[query, document.page_content]])[0]
            buffer.append((document, score, ranker_score))

        buffer.sort(key=lambda x: x[2], reverse=True)
        return buffer

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({"model": self.model})
        return base_dict


class BAAIReranker(Reranker):

    def __init__(self, model: str = "BAAI/bge-reranker-v2-m3"):
        self.model = model

        from FlagEmbedding import FlagReranker
        import torch

        self.reranker = FlagReranker(
            model, use_fp16=True, device="cuda" if torch.cuda.is_available() else "cpu"
        )

    def invoke(
        self, query: str, documents: list[Document, float]
    ) -> list[Document, float, float]:
        buffer = []
        for document, score in documents:
            ranker_score = self.reranker.compute_score(
                [query, document.page_content], normalize=True
            )
            buffer.append((document, score, ranker_score))

        buffer.sort(key=lambda x: x[2], reverse=True)
        return buffer

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({"model": self.model})
        return base_dict


if __name__ == "__main__": # pragma: no cover
    pass