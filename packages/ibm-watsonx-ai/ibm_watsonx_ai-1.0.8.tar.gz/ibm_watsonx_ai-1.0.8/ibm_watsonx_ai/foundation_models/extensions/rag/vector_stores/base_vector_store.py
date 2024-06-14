#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from abc import ABC, abstractmethod
from typing import Any

from ibm_watsonx_ai.foundation_models.embeddings import BaseEmbeddings


class BaseVectorStore(ABC):
    """Base abstract class for all vector store-like classes. Interface that support simple database operations."""

    @abstractmethod
    def set_embeddings(self, embedding_fn: BaseEmbeddings) -> None:
        """If possible, sets a default embedding function.
        Use types inheirted from ``BaseEmbeddings`` if you want to make it capable for ``RAGPattern`` deployment.
        Argument ``embedding_fn`` can be a langchain embeddings but issues with serialization will occur.

        :param embedding_fn: embedding function
        :type embedding_fn: BaseEmbeddings
        """
        raise NotImplementedError(
            "This vector store cannot have embedding function set up."
        )

    @abstractmethod
    def add_documents(
        self, content: list[str] | list[dict] | list, **kwargs: Any
    ) -> list[str]:
        """Add document to the RAG's vector store.
        List must contain either strings, dicts with a required field ``content`` of str type or langchain ``Document``.

        :param content: unstructured list of data to be added
        :type content: list[str] | list[dict] | list

        :return: list of ids
        :rtype: list[str]
        """
        pass

    @abstractmethod
    async def add_documents_async(
        self, content: list[str] | list[dict] | list, **kwargs: Any
    ) -> list[str]:
        """Add document to the RAG's vector store asynchronously.
        List must contain either strings, dicts with a required field ``content`` of str type or langchain ``Document``.

        :param content: unstructured list of data to be added
        :type content: list[str] | list[dict] | list

        :return: list of ids
        :rtype: list[str]
        """
        pass

    @abstractmethod
    def search(
        self,
        query: str,
        k: int,
        include_scores: bool = False,
        verbose: bool = False,
        **kwargs: Any,
    ) -> list:
        """Get documents that would fit the query.

        :param query: question asked by a user
        :type query: str

        :param k: max number of similar documents
        :type k: int

        :param include_scores: return scores for documents, defaults to False
        :type include_scores: bool, optional

        :param verbose: print formated response to the output, defaults to False
        :type verbose: bool, optional

        :return: list of found documents
        :rtype: list
        """
        pass

    @abstractmethod
    def delete(self, ids: list[str], **kwargs: Any) -> None:
        """Delete documents with provided ids.

        :param ids: IDs of documents to delete
        :type ids: list[str]
        """
        pass

    @abstractmethod
    def as_langchain_retreiver(self, **kwargs: Any) -> Any:
        """Creates a langchain retreiver from this vector store.

        :return: langchain retriever which can be used in langchain pipelines
        :rtype: langchain_core.vectorstores.VectorStoreRetriever
        """
        pass
