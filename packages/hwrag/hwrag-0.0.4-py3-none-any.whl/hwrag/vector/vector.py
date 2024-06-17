from abc import ABC, abstractmethod
from langchain_core.documents import Document
import os
from hwrag.fusion.fusion import AutoContext

class VectorDB(ABC):
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
    def add_documents(self, documents: list[Document]):
        """
        Store a list of vectors with associated metadata.
        """
        pass

    @abstractmethod
    def invoke(self, query: str, top_k: int = 5):
        pass


class MilvusDB(VectorDB):
    def __init__(
        self,
        host: str = None,
        port: str = None,
        collection_name: str = "",
        embedding=None,
    ):
        from langchain_community.vectorstores import Milvus

        self.embedding = embedding
        self.host = host
        self.port = port
        self.collection_name = collection_name
        self.vector_store = Milvus(
            self.embedding,
            connection_args={"host": self.host, "port": self.port},
            collection_name=self.collection_name,
            auto_id=True,
        )

    def add_documents(self, documents: list[Document]):
        self.vector_store.add_documents(documents, embedding=self.embedding)

    def invoke(self, query: str, top_k: int = 5) -> list[Document, float]:
        results = self.vector_store.similarity_search_with_score(query, k=top_k)
        return results

    def to_dict(self):
        return {
            **super().to_dict(),
            "embedding": self.embedding,
            "host": self.host,
            "port": self.port,
            "collection_name": self.collection_name,
        }

class HwMilvusWithParentDB(VectorDB):
    def __init__(
        self,
        host: str = "",
        port: str = "",
        parent_collection_name: str = "",
        collection_name: str = "",
        embedding=None,
    ):
        import os,sys
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
        from hwrag.utils.hw_milvus import HWMilvus
        from hwrag.llm.llm import OllamaLLM
        from hwrag.fusion.fusion import AutoContext
        self.llm = OllamaLLM(model='qwen:14b-chat')
        self.auto_context = AutoContext(self.llm)
        self.embedding = embedding
        self.host = host
        self.port = port
        self.collection_name = collection_name
        self.parent_collection_name = parent_collection_name
        self.vector_store = HWMilvus(
            self.embedding,
            connection_args={"host": self.host, "port": self.port},
            collection_name=self.collection_name,
            auto_id=True,
        )
        self.parent_vector_store = HWMilvus(
            self.embedding,
            connection_args={"host": self.host, "port": self.port},
            collection_name=self.parent_collection_name,
            auto_id=True,
        )
        
    def add_documents(self, documents: list[Document]):
        import os,sys
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
        import hashlib
        from hwrag.splitter.splitter import ChineseSplitter
        text_spliter = ChineseSplitter(chunk_size=100)
        i = 0
        for document in documents:
            p_id_str = hashlib.md5(document.metadata['source'].encode('utf-8')).hexdigest()
            i += 1
            docs = text_spliter.invoke([document])
            file_id = p_id_str + f'_{i}'
            document.metadata['file_id'] = file_id
            for doc in docs:
                doc.metadata['parent_id'] = file_id
            self.vector_store.add_documents(docs, embedding=self.embedding)
        documents = self.auto_context.invoke(documents)
        self.parent_vector_store.add_documents(documents, embedding=self.embedding)

    def invoke(self, query: str, top_k: int = 5) -> list[Document, float]:
        results = self.vector_store.similarity_search_with_score(query, k=top_k)
        ids = []
        for result in results:
            parent_id = result[0].metadata['parent_id']
            if parent_id not in ids:
                ids.append(parent_id)
        parent_results = []
        for parent_id in ids:
            for item in self._find_parent(parent_id):
                parent_results.append((Document(page_content=item['text'], metadata={'source': item['source']}), 0))
        return parent_results
    
    def _find_parent(self, file_id: str):
        return self.parent_vector_store.aquery(expr=f"file_id == \"{file_id}\" ")

    def to_dict(self):
        return {
            **super().to_dict(),
            "embedding": self.embedding,
            "host": self.host,
            "port": self.port,
            "collection_name": self.collection_name,
        }

class ESDB(VectorDB):
    def __init__(
        self, host: str = None, port: str = None, collection_name: str = ""
    ):
        from elasticsearch import Elasticsearch

        self.host = host
        self.port = port
        self.collection_name = collection_name
        self.vector_store = Elasticsearch(
            hosts=[f"http://{host}:{port}"], use_ssl=False
        )

    # docs=[]
    def add_documents(self, documents: list[Document]):
        docs = []
        if not self.vector_store.indices.exists(self.collection_name):
            self.vector_store.indices.create(
                index=self.collection_name,
                body={
                    "settings": {
                        "analysis": {"analyzer": {"default": {"type": "ik_smart"}}}
                    },
                    "mappings": {
                        "properties": {
                            "title": {"type": "text", "analyzer": "ik_max_word"},
                            "content": {
                                "type": "text",
                                "analyzer": "ik_smart",
                                "similarity": "BM25",
                            },
                        }
                    },
                },
            )
        for doc in documents:
            title = doc.metadata["source"].split("/")[-1].split(".")[0]
            content = doc.page_content
            self.vector_store.index(
                index=self.collection_name,
                document={"title": title, "content": content},
            )

    def invoke(self, query: str, top_k: int = 5) -> list[Document, float]:
        results = self.vector_store.search(
            index=self.collection_name,
            query={"bool": {"must": [{"match": {"content": query}}]}},
            size=top_k,
        )
        similary_results = []
        for item in results["hits"]["hits"]:
            doc = Document(page_content=item["_source"]["content"], metadata={'source': item["_source"]["title"]})
            similary_results.append((doc, item["_score"]))
        return similary_results

    def to_dict(self):
        return {
            **super().to_dict(),
            "host": self.host,
            "port": self.port,
            "collection_name": self.collection_name,
        }
