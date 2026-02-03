"""
Document processing module.
Handles loading, splitting, and preprocessing of documents.
"""
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document


class DocumentProcessor:
    """Handles document loading and chunking."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 20):
        """
        Initialize the document processor.
        
        Args:
            chunk_size: Size of each text chunk
            chunk_overlap: Overlap between consecutive chunks
        """
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    def load_from_file(self, file_path: str) -> List[Document]:
        """
        Load and chunk a text file.
        
        Args:
            file_path: Path to the text file
            
        Returns:
            List of document chunks
        """
        loader = TextLoader(file_path)
        documents = loader.load()
        return self.split_documents(documents)
    
    def load_from_text(self, text: str) -> List[Document]:
        """
        Load and chunk raw text.
        
        Args:
            text: Raw text string
            
        Returns:
            List of document chunks
        """
        document = Document(page_content=text)
        return self.split_documents([document])
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks.
        
        Args:
            documents: List of documents to split
            
        Returns:
            List of document chunks
        """
        return self.splitter.split_documents(documents)