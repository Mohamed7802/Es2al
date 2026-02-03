"""
Main entry point for the RAG system.
Demonstrates usage of the production RAG pipeline.
"""
from config.settings import settings
from core.document_processor import DocumentProcessor
from core.embeddings_manager import EmbeddingsManager
from core.llm_client import LLMClient
from pipeline.rag_pipeline import RAGPipeline


def create_rag_pipeline() -> RAGPipeline:
    """
    Create and configure the RAG pipeline.
    
    Returns:
        Configured RAG pipeline instance
    """
    # Validate settings
    settings.validate()
    
    # Initialize components
    doc_processor = DocumentProcessor(
        chunk_size=settings.chunking.chunk_size,
        chunk_overlap=settings.chunking.chunk_overlap
    )
    
    embeddings_manager = EmbeddingsManager(
        model=settings.model.embedding_model,
        api_key=settings.openai_api_key
    )
    
    llm_client = LLMClient(
        model=settings.model.llm_model,
        api_key=settings.openai_api_key,
        temperature=settings.model.temperature,
        max_tokens=settings.model.max_tokens
    )
    
    # Create pipeline
    pipeline = RAGPipeline(
        document_processor=doc_processor,
        embeddings_manager=embeddings_manager,
        vector_store_type=settings.vector_store.store_type,
        llm_client=llm_client,
        index_name=settings.vector_store.index_name,
        top_k=settings.vector_store.top_k
    )
    
    return pipeline


def main():
    """Main execution function."""
    
    # Create pipeline
    print("Initializing RAG pipeline...")
    pipeline = create_rag_pipeline()
    
    # Ingest documents
    print("Ingesting documents...")
    file_path = "transcription.txt"
    num_chunks = pipeline.ingest_documents(file_path=file_path)
    print(f"Processed {num_chunks} document chunks")
    
    # Example queries
    queries = [
        "What is synthetic intelligence?",
        "What is Hollywood going to start doing?",
        "What advice does the speaker give to researchers?",
    ]
    
    print("\n" + "="*80)
    print("Running example queries...")
    print("="*80 + "\n")
    
    for query in queries:
        print(f"Q: {query}")
        answer = pipeline.query(query)
        print(f"A: {answer}\n")
        print("-"*80 + "\n")
    
    # Example similarity search
    print("\nSimilarity search example:")
    print("-"*80)
    query = "What are neural networks?"
    similar_docs = pipeline.search_similar(query, k=2)
    
    print(f"Query: {query}\n")
    print(f"Found {len(similar_docs)} similar chunks:\n")
    for i, doc in enumerate(similar_docs, 1):
        print(f"{i}. {doc.page_content[:200]}...\n")


if __name__ == "__main__":
    main()