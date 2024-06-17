from abc import ABC, abstractmethod
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_correctness


class Evaluator(ABC):
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
        self, query: str, answer: str, context: str = None, ground_truth: str = None
    ) -> float:
        pass


class RagasEvaluator(Evaluator):
    def invoke(
        self, query: str, answer: str, context: str = None, ground_truth: str = None
    ) -> float:
        dataset = Dataset.from_dict(
            {
                "question": [query],
                "answer": [answer],
                "contexts": [[context]],
                "ground_truth": [ground_truth],
            }
        )
        score = evaluate(dataset, metrics=[faithfulness, answer_correctness])
        return score["answer_correctness"]

    def to_dict(self):
        return super().to_dict()


class BCEEvaluator(Evaluator):

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
        self, query: str, answer: str, context: str = None, ground_truth: str = None
    ) -> float:
        ranker_score = self.reranker.predict([[query, answer]])[0]
        return ranker_score

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({"model": self.model})
        return base_dict


class BAAIEvaluator(Evaluator):

    def __init__(self, model: str = "BAAI/bge-reranker-v2-m3"):
        self.model = model

        from FlagEmbedding import FlagReranker
        import torch

        self.reranker = FlagReranker(
            model, use_fp16=True, device="cuda" if torch.cuda.is_available() else "cpu"
        )

    def invoke(
        self, query: str, answer: str, context: str = None, ground_truth: str = None
    ) -> float:
        ranker_score = self.reranker.compute_score([query, answer], normalize=True)
        return ranker_score

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({"model": self.model})
        return base_dict
