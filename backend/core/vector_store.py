"""
Vector store module.
Handles document storage and similarity search.
"""
from typing import List, Protocol
from langchain.schema import Document
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_pinecone import PineconeVectorStore


class VectorStoreProtocol(Protocol):
    """Protocol defining vector store interface."""
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store."""
        ...
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Search for similar documents."""
        ...
    
    def as_retriever(self, **kwargs):
        """Get a retriever interface."""
        ...


class VectorStoreFactory:
    """Factory for creating vector store instances."""
    
    @staticmethod
    def create(
        store_type: str,
        embeddings,
        index_name: str = None,
        **kwargs
    ) -> VectorStoreProtocol:
        """
        Create a vector store instance.
        
        Args:
            store_type: Type of vector store ("in_memory" or "pinecone")
            embeddings: Embeddings client
            index_name: Index name (required for Pinecone)
            **kwargs: Additional arguments
            
        Returns:
            Vector store instance
        """
        if store_type == "in_memory":
            return InMemoryVectorStore(embeddings)
        elif store_type == "pinecone":
            if not index_name:
                raise ValueError("index_name required for Pinecone vector store")
            return PineconeVectorStoreWrapper(embeddings, index_name)
        else:
            raise ValueError(f"Unknown vector store type: {store_type}")


class InMemoryVectorStore:
    """In-memory vector store wrapper."""
    
    def __init__(self, embeddings):
        """
        Initialize in-memory vector store.
        
        Args:
            embeddings: Embeddings client
        """
        self.embeddings = embeddings
        self.store = None
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store."""
        if self.store is None:
            self.store = DocArrayInMemorySearch.from_documents(
                documents, 
                self.embeddings
            )
        else:
            self.store.add_documents(documents)
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Search for similar documents."""
        if self.store is None:
            return []
        return self.store.similarity_search(query, k=k)
    
    def as_retriever(self, **kwargs):
        """Get a retriever interface."""
        if self.store is None:
            raise ValueError("Vector store is empty. Add documents first.")
        return self.store.as_retriever(**kwargs)


class PineconeVectorStoreWrapper:
    """Pinecone vector store wrapper."""
    
    def __init__(self, embeddings, index_name: str):
        """
        Initialize Pinecone vector store.
        
        Args:
            embeddings: Embeddings client
            index_name: Pinecone index name
        """
        self.embeddings = embeddings
        self.index_name = index_name
        self.store = None
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store."""
        if self.store is None:
            self.store = PineconeVectorStore.from_documents(
                documents,
                self.embeddings,
                index_name=self.index_name
            )
        else:
            self.store.add_documents(documents)
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Search for similar documents."""
        if self.store is None:
            return []
        return self.store.similarity_search(query, k=k)
    
    def as_retriever(self, **kwargs):
        """Get a retriever interface."""
        if self.store is None:
            raise ValueError("Vector store is empty. Add documents first.")
        return self.store.as_retriever(**kwargs)