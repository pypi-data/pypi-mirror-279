from abc import ABC, abstractmethod
from hwrag.llm.llm import LLM
from langchain_core.documents import Document


class Generator(ABC):
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
    def invoke(self, query: str, docs: list[Document]) -> str:
        pass

    def final_invoke(self, query: str, arr: list) -> str:
        pass


class LLMGenerator(Generator):

    def __init__(self, llm: LLM):
        # from QAnything project
        # self.PROMPT = """参考信息：
        # {context}
        # ---
        # 我的问题或指令：
        # {question}
        # ---
        # 请根据上述参考信息回答我的问题或回复我的指令。前面的参考信息可能有用，也可能没用，你需要从我给出的参考信息中选出与我的问题最相关的那些，来为你的回答提供依据。回答一定要忠于原文，简洁但不丢信息，不要胡乱编造，不要包含有害信息。我的问题或指令是什么语种，你就用什么语种回复。
        # 你的回复："""

        self.PROMPT = """您是一位非常专业的人工智能助手。您将被提供一个用户问题，并需要撰写一个清晰、简洁且准确的答案。您被提供了一组与问题相关的上下文，每个都以[[citation:x]]这样的编号开头，x代表一个数字。请在适当的情况下在句子末尾引用上下文。答案必须正确、精确，并以专家的中立和职业语气撰写。不要提供与问题无关的信息，也不要重复。如果给出的上下文信息不足，请在相关主题后写上“信息缺失：”。请按照引用编号[citation:x]的格式在答案中对应部分引用上下文。如果一句话源自多个上下文，请列出所有相关的引用编号，例如[citation:3][citation:5]，不要将引用集中在最后返回，而是在答案对应部分列出。除非是代码、特定的名称或引用编号，答案的语言应与问题相同。以下是上下文的内容集：

        {context}

        记住，不要一字不差的重复上下文内容. 回答必须使用简体中文，如果回答很长，请尽量结构化、分段落总结。请按照引用编号[citation:x]的格式在答案中对应部分引用上下文。如果一句话源自多个上下文，请列出所有相关的引用编号，例如[citation:3][citation:5]，不要将引用集中在最后返回，而是在答案对应部分列出。下面是用户问题：

        {question}
        """
        self.llm = llm

    def invoke(self, query: str, documents: list[Document]) -> str:
        context = ""
        for doc in documents:
            content = doc[0].page_content
            context = context + "\n" + content
        prompt = self.PROMPT.format(context=context, question=query)
        result = self.llm.make_llm_call([{"role": "user", "content": prompt}])
        return {"answer": result, "context": context,"source": documents}

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({"llm": self.llm})
        return base_dict
