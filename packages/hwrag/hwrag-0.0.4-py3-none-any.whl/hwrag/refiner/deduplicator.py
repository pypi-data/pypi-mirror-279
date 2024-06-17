from abc import ABC, abstractmethod
from langchain_core.documents import Document


class Deduplicator(ABC):
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
        self, documents_1: list[Document, float], documents_2: list[Document, float]
    ) -> list[Document, float]:
        pass


class RRFDeduplicator(Deduplicator):
    """
    Reciprocal Rank Fusion (RRF) algorithm, refer to https://dl.acm.org/doi/10.1145/1571941.1572114
    """

    def __init__(self): ...

    def invoke(
        self, documents_1: list[Document, float], documents_2: list[Document, float]
    ) -> list[Document, float]:
        documents_1 = self._documents_deduplication(documents_1)
        documents_2 = self._documents_deduplication(documents_2)

        common_contents = self._find_common_elements(documents_1, documents_2)

        # 如果没有重复元素，直接合并数组并返回
        merged_array = []
        if not common_contents:
            merged_array = documents_1 + documents_2
        else:
            # 创建两个新的数组来存放重复元素
            new_array1 = [
                item for item in documents_1 if item[0].page_content in common_contents
            ]
            new_array2 = [
                item for item in documents_2 if item[0].page_content in common_contents
            ]

            # 按照元组中的分数倒序排列
            new_array1.sort(key=lambda x: x[1], reverse=True)
            new_array2.sort(key=lambda x: x[1], reverse=True)

            # 计算分值
            new_scores = {}
            for content in common_contents:
                idx1 = [
                    i
                    for i, item in enumerate(new_array1)
                    if item[0].page_content == content
                ][0]
                idx2 = [
                    i
                    for i, item in enumerate(new_array2)
                    if item[0].page_content == content
                ][0]
                score1 = (idx1 + 1) / len(new_array1)
                score2 = (idx2 + 1) / len(new_array2)
                new_scores[content] = score1 + score2

            # 合并原始数组，并更新相同content的分值
            merged_array = []
            for item in documents_1 + documents_2:
                content = item[0].page_content
                if content in new_scores:
                    merged_array.append((item[0], new_scores[content]))
                else:
                    merged_array.append(item)
        return merged_array

    def _find_common_elements(
        self, arr1: list[Document, float], arr2: list[Document, float]
    ) -> list[Document, float]:
        common_elements = set()
        for item1 in arr1:
            for item2 in arr2:
                if item1[0].page_content == item2[0].page_content:
                    common_elements.add(item1[0].page_content)
        return common_elements

    def _documents_deduplication(
        self, documents: list[Document, float]
    ) -> list[Document, float]:
        seen_contents = {}
        unique_documents = []
        for doc in documents:
            if doc[0].page_content not in seen_contents:
                seen_contents[doc[0].page_content] = doc
                unique_documents.append(doc)
        return unique_documents


class NoDeduplicator(Deduplicator):

    def __init__(self): ...

    def invoke(
        self, documents_1: list[Document, float], documents_2: list[Document, float]
    ) -> list[Document, float]:
        merged_array = documents_1 + documents_2
        return merged_array
