from abc import ABC, abstractmethod
from langchain_core.documents import Document


class Splitter(ABC):
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
    def invoke(self, documents: list[Document]) -> list[Document]:
        pass


class ChineseSplitter(Splitter):
    def __init__(self, chunk_size: int = 100):
        from hwrag.utils.chinese_text_splitter import ChineseTextSplitter

        self.chunk_size = chunk_size
        self.text_splitter = ChineseTextSplitter(
            pdf=False, sentence_size=self.chunk_size
        )

    def invoke(self, documents: list[Document]) -> list[Document]:
        return self.text_splitter.split_documents(documents)

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({"chunk_size": self.chunk_size})
        return base_dict


class CharacterSplitter(Splitter):
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 0):
        from langchain.text_splitter import CharacterTextSplitter

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = CharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )

    def invoke(self, documents: list[Document]) -> list[Document]:
        return self.text_splitter.split_documents(documents)

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update(
            {"chunk_size": self.chunk_size, "chunk_overlap": self.chunk_overlap}
        )
        return base_dict


class RecursiveWithTikTokenSplitter(Splitter):
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 0):
        from langchain.text_splitter import RecursiveCharacterTextSplitter

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )

    def invoke(self, documents: list[Document]) -> list[Document]:
        return self.text_splitter.split_documents(documents)

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update(
            {"chunk_size": self.chunk_size, "chunk_overlap": self.chunk_overlap}
        )
        return base_dict
