"""
Embeddings management module.
Handles creation and management of text embeddings.
"""
from typing import List
from langchain_openai.embeddings import OpenAIEmbeddings


class EmbeddingsManager:
    """Manages text embeddings using OpenAI."""
    
    def __init__(self, model: str = "text-embedding-ada-002", api_key: str = None):
        """
        Initialize the embeddings manager.
        
        Args:
            model: OpenAI embedding model name
            api_key: OpenAI API key
        """
        self.embeddings = OpenAIEmbeddings(
            model=model,
            openai_api_key=api_key
        )
    
    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a single query.
        
        Args:
            query: Text query to embed
            
        Returns:
            Embedding vector
        """
        return self.embeddings.embed_query(query)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple documents.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        return self.embeddings.embed_documents(texts)
    
    def get_embeddings_client(self):
        """Get the underlying embeddings client for vector store integration."""
        return self.embeddings