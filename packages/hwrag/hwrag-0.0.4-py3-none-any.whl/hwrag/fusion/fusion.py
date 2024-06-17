from abc import ABC, abstractmethod
from langchain_core.documents import Document
from hwrag.llm.llm import LLM
import json

class Fusion(ABC):
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


class AutoContext(Fusion):

    def __init__(self, llm: LLM):
        self.PROMPT = """
        INSTRUCTIONS
        请问下列文件是什么，内容是关于什么的？
        您的回答应该是一句话，且不要过长。请不要回答任何其他内容。
        您必须在回答中包含文件名称（如果有的话），因为这是一条关键的信息。请尽可能具体和详细地描述文件名称。如果有的话，您甚至可以包括作者名称或出版日期等信息。请不要仅使用文件名作为文档名称。它需要是描述性的，人类可读的名称。
        您的回答应该采取“这份文件是：X，关于：Y”的形式。例如，如果文件是一本关于美国历史的书，名为《美国人的历史》，您的回答可能是“这份文件是：《美国人的历史》，关于从1776年到现在的美国历史。”如果文件是苹果公司2023年度的10-K表格，您的回答可能是“这份文件是：苹果公司2023财年10-K表格，关于：苹果公司在2023财年的财务表现和运营情况。”

        文件
        文件名：{document_title}

        {document}
        """.strip()

        self.llm = llm

    def _get_document_sumary(self, text: str, document_title: str):
        prompt = self.PROMPT.format(document=text, document_title=document_title)
        sumary = self.llm.make_llm_call([{"role": "user", "content": prompt}])
        return sumary

    def invoke(self, documents: list[Document]) -> list[Document]:
        for document in documents:
            title = document.metadata["source"].split("/")[-1].split(".")[0]
            content = document.page_content
            summary = self._get_document_sumary(text=content, document_title=title)
            document.metadata["summary"] = summary
            document.page_content = summary + "\n" + content
        return documents

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({"llm": self.llm})
        return base_dict


class QueryRewriting(Fusion):
    def __init__(self, llm: LLM):
        self.PROMPT = """
        您是一个中医药领域智能查询生成系统。请根据下方提供的问题，生成多条搜索查询（最多为{max_queries}条）。不要生成答案，不要回答问题，不要提供建议，只生成搜索查询。
        您生成的每个查询都将用于搜索知识库，以寻找可用于响应用户输入的信息。确保每个查询足够具体，可以返回相关信息。如果多条信息有用，您应该生成多个查询，每个所需的特定信息都有一个查询。
        返回的问题需要放在一个json格式的数组中，需要严格遵循返回的格式正确。
        返回的格式如下所示，需要严格遵守，不要有多余的返回：
        [
            "",
            "",
            "",
            ""
        ]
        问题：{question}
        """.strip()

        self.llm = llm
    def invoke(self, query: str, max_queries: int) -> str:
        prompt = self.PROMPT.format(question=query, max_queries=max_queries)
        queries = self.llm.make_llm_call([{"role": "user", "content": prompt}])
        try:
            arr = json.loads(queries)
            for a in arr:
                if type(a) != str:
                    return [query]
            return arr
        except Exception as e:
            print('---------------ee')
            return [query]

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({"llm": self.llm})
        return base_dict


class NoQueryRewriting(Fusion):
    def __init__(self):
        ...

    def invoke(self, query: str, max_queries: int) -> list[str]:
        return [query]

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({})
        return base_dict