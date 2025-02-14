import uuid
from datetime import time
from typing import Optional, List, Union
from src.preprocessing import embeddings, splitter
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents.base import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
)


class PineConeConfig:
    """
    A configuration class for managing Pinecone vector database operations.

    Attributes:
        api_key (str): Pinecone API key
        index_name (str): Name of the Pinecone index
        namespace (str, optional): Namespace for the index
        data (Any, optional): Raw data to be processed
        url (str, optional): URL or file path for document loading
        url_file_type (str, optional): Type of file to be loaded
    """

    SUPPORTED_FILE_TYPES = {"csv", "pdf", "txt"}
    DIMENSION = 1536
    METRIC = "cosine"
    CLOUD = "aws"
    REGION = "us-east-1"

    def __init__(
        self,
        api_key: str,
        index_name: str,
        namespace: Optional[str] = None,
        url: Optional[str] = None,
        url_file_type: Optional[str] = None,
    ):
        if not api_key or not index_name:
            raise ValueError("API key and index name are required")

        self.api_key = api_key
        self.pc = Pinecone(api_key=api_key)
        self.index_name = index_name
        self.namespace = namespace or str(uuid.uuid4())
        self.url = url
        self.url_file_type = url_file_type and url_file_type.lower()

        self._create_index_if_not_exist()
        self.index = self.pc.Index(index_name)
        self.vector_store = PineconeVectorStore(
            index=self.index, embedding=embeddings, namespace=self.namespace
        )

    def _create_index_if_not_exist(self) -> None:
        """Create a new index if it doesn't exist."""
        try:
            existing_indexes = {
                index_info["name"] for index_info in self.pc.list_indexes()
            }

            if self.index_name not in existing_indexes:
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.DIMENSION,
                    metric=self.METRIC,
                    spec=ServerlessSpec(cloud=self.CLOUD, region=self.REGION),
                )

                self._wait_for_index_ready()
        except Exception as e:
            raise RuntimeError(f"Failed to create index: {str(e)}")

    def _wait_for_index_ready(self, max_retries: int = 60) -> None:
        """Wait for index to be ready with timeout."""
        retries = 0
        while not self.pc.describe_index(self.index_name).status["ready"]:
            if retries >= max_retries:
                raise TimeoutError("Index creation timed out")
            time.sleep(1)
            retries += 1

    def add_documents(self) -> None:
        """Add documents from file to the vector store."""
        if not self.url:
            raise ValueError("File path not provided")

        if not self.url_file_type:
            raise ValueError("File type not specified")

        if self.url_file_type not in self.SUPPORTED_FILE_TYPES:
            raise ValueError(
                f"Unsupported file type. Supported types: {self.SUPPORTED_FILE_TYPES}"
            )

        docs = self.load_and_split_document()
        self.vector_store.add_documents(
            documents=docs, ids=[f"{self.namespace}_{i}" for i in range(len(docs))]
        )

    # def add_text(self) -> None:
    #     """Add text data to the vector store."""
    #     if not self.data:
    #         raise ValueError("No data provided")

    #     text_docs = self.get_text_chunks_langchain()
    #     self.vector_store.add_documents(
    #         documents=text_docs,
    #         ids=[f"{self.namespace}_{i}" for i in range(len(text_docs))]
    #     )

    def load_and_split_document(self) -> List[Document]:
        """Load and split document based on file type."""

        loaders = {
            "csv": CSVLoader,
            "pdf": PyPDFLoader,
            "txt": TextLoader,
        }

        loader_class = loaders.get(self.url_file_type)
        if not loader_class:
            raise ValueError(f"Unsupported file type: {self.url_file_type}")

        try:
            return loader_class(self.url).load_and_split(splitter)
        except Exception as e:
            raise RuntimeError(f"Error loading document: {str(e)}")

    # def get_text_chunks_langchain(self) -> List[Document]:
    #     """Convert text data into document chunks."""
    #     if not self.data:
    #         raise ValueError("No data provided")

    #     try:
    #         return [
    #             Document(page_content=x)
    #             for x in splitter.split_text(str(self.data))
    #         ]
    #     except Exception as e:
    #         raise RuntimeError(f"Error chunking text: {str(e)}")

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        score_threshold: Optional[float] = None,
        filter: Optional[dict] = None,
        include_metadata: bool = True,
    ) -> List[Union[Document, tuple[Document, float]]]:
        """
        Perform similarity search across all documents in the namespace.

        Args:
            query (str): The search query
            k (int): Number of results to return
            score_threshold (float, optional): Minimum similarity score threshold
            filter (dict, optional): Metadata filter conditions
            include_metadata (bool): Whether to include metadata in results

        Returns:
            List[Union[Document, tuple[Document, float]]]: List of documents or
            tuples of (document, score) if score_threshold is provided
        """
        if not query:
            raise ValueError("Query string is required")

        try:
            # If score threshold is provided, use similarity search with score
            if score_threshold is not None:
                results = self.vector_store.similarity_search_with_score(
                    query=query,
                    k=k,
                    filter=filter,
                )
                # Filter results based on score threshold
                filtered_results = [
                    doc.page_content
                    for doc, score in results
                    if score >= score_threshold
                ]
                return filtered_results

            # Otherwise, use regular similarity search
            results = self.vector_store.similarity_search(
                query=query, k=k, filter=filter, include_metadata=include_metadata
            )
            filtered_results = [doc.page_content for doc in results]
            return filtered_results

        except Exception as e:
            raise RuntimeError(f"Error performing similarity search: {str(e)}")

    def get_namespace_stats(self) -> dict:
        """Get statistics for the current namespace."""
        try:
            return self.index.describe_index_stats(namespace=self.namespace)
        except Exception as e:
            raise RuntimeError(f"Error getting namespace stats: {str(e)}")

    def delete_namespace(self) -> None:
        """Delete all vectors in the current namespace."""
        try:
            self.index.delete(delete_all=True, namespace=self.namespace)
        except Exception as e:
            raise RuntimeError(f"Error deleting namespace: {str(e)}")
