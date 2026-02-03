"""
Configuration settings for the RAG system.
Centralizes all configuration parameters.
"""
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class ModelConfig:
    """LLM and embedding model configuration."""
    llm_model: str = "gpt-3.5-turbo"
    embedding_model: str = "text-embedding-ada-002"
    temperature: float = 0.0
    max_tokens: int = 1000


@dataclass
class ChunkingConfig:
    """Document chunking configuration."""
    chunk_size: int = 1000
    chunk_overlap: int = 20


@dataclass
class VectorStoreConfig:
    """Vector store configuration."""
    store_type: str = "pinecone"  # or "in_memory"
    index_name: str = "es2al-index"
    top_k: int = 4


@dataclass
class Settings:
    """Main settings class."""
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    pinecone_api_key: str = os.getenv("PINECONE_API_KEY", "")

    model: ModelConfig = field(default_factory=ModelConfig)
    chunking: ChunkingConfig = field(default_factory=ChunkingConfig)
    vector_store: VectorStoreConfig = field(default_factory=VectorStoreConfig)

    def validate(self):
        """Validate required settings."""
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        if self.vector_store.store_type == "pinecone" and not self.pinecone_api_key:
            raise ValueError("PINECONE_API_KEY required for Pinecone vector store")


# Global settings instance
settings = Settings()
