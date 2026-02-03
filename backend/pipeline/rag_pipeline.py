"""
RAG pipeline orchestration module.
Coordinates the entire RAG workflow.
"""
from typing import List
from langchain.schema import Document
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from core.document_processor import DocumentProcessor
from core.embeddings_manager import EmbeddingsManager
from core.vector_store import VectorStoreFactory
from core.llm_client import LLMClient


class RAGPipeline:
    """Orchestrates the RAG workflow."""
    
    def __init__(
        self,
        document_processor: DocumentProcessor,
        embeddings_manager: EmbeddingsManager,
        vector_store_type: str,
        llm_client: LLMClient,
        index_name: str = None,
        top_k: int = 4
    ):
        """
        Initialize the RAG pipeline.
        
        Args:
            document_processor: Document processor instance
            embeddings_manager: Embeddings manager instance
            vector_store_type: Type of vector store
            llm_client: LLM client instance
            index_name: Vector store index name
            top_k: Number of documents to retrieve
        """
        self.doc_processor = document_processor
        self.embeddings = embeddings_manager
        self.llm = llm_client
        self.top_k = top_k
        
        # Initialize vector store
        self.vector_store = VectorStoreFactory.create(
            store_type=vector_store_type,
            embeddings=embeddings_manager.get_embeddings_client(),
            index_name=index_name
        )
        
        self.chain = None
    
    def ingest_documents(self, file_path: str = None, text: str = None) -> int:
        """
        Ingest documents into the RAG system.
        
        Args:
            file_path: Path to document file
            text: Raw text to ingest
            
        Returns:
            Number of chunks processed
        """
        if file_path:
            chunks = self.doc_processor.load_from_file(file_path)
        elif text:
            chunks = self.doc_processor.load_from_text(text)
        else:
            raise ValueError("Either file_path or text must be provided")
        
        self.vector_store.add_documents(chunks)
        self._build_chain()
        
        return len(chunks)
    
    def _build_chain(self) -> None:
        """Build the RAG chain."""
        retriever = self.vector_store.as_retriever(
            search_kwargs={"k": self.top_k}
        )
        
        def format_docs(docs):
            """Format retrieved documents into a single string."""
            return "\n\n".join(doc.page_content for doc in docs)
        
        self.chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough()
            }
            | self.llm.get_prompt()
            | self.llm.get_model()
            | self.llm.get_parser()
        )
    
    def query(self, question: str) -> str:
        """
        Query the RAG system.
        
        Args:
            question: Question to answer
            
        Returns:
            Generated answer
        """
        if self.chain is None:
            raise ValueError("No documents ingested. Call ingest_documents first.")
        
        return self.chain.invoke(question)
    
    def search_similar(self, query: str, k: int = None) -> List[Document]:
        """
        Search for similar documents without LLM generation.
        
        Args:
            query: Search query
            k: Number of results (uses pipeline default if None)
            
        Returns:
            List of similar documents
        """
        k = k or self.top_k
        return self.vector_store.similarity_search(query, k=k)