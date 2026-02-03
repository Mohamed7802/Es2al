"""
Video processing service.
Handles YouTube video download, transcription, and RAG pipeline management.
"""
import tempfile
import os
import whisper
import yt_dlp
from typing import Optional, Dict, Any

from config.settings import settings
from core.document_processor import DocumentProcessor
from core.embeddings_manager import EmbeddingsManager
from core.llm_client import LLMClient
from pipeline.rag_pipeline import RAGPipeline


class VideoRAGService:
    """
    Singleton service for managing video processing and RAG pipeline.
    Maintains state across API requests.
    """
    
    _instance = None
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(VideoRAGService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the service (only once due to singleton)."""
        if not self._initialized:
            self.pipeline: Optional[RAGPipeline] = None
            self.whisper_model: Optional[Any] = None
            self.current_video_url: Optional[str] = None
            self.transcription_text: Optional[str] = None
            self.video_title: Optional[str] = None
            self._initialized = True
    
    def _load_whisper_model(self):
        """Load Whisper model lazily."""
        if self.whisper_model is None:
            self.whisper_model = whisper.load_model("base")
        return self.whisper_model
    
    def process_video(self, video_url: str) -> Dict[str, Any]:
        """
        Download, transcribe, and process a YouTube video.
        
        Args:
            video_url: YouTube video URL
            
        Returns:
            Dictionary with processing results and status
        """
        try:
            # Download audio using yt-dlp
            with tempfile.TemporaryDirectory() as tmpdir:
                audio_file = os.path.join(tmpdir, "audio.%(ext)s")
                
                # yt-dlp options
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': audio_file,
                    'quiet': True,
                    'no_warnings': True,
                    'extract_audio': True,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
                
                # Download video and extract info
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=True)
                    self.video_title = info.get('title', 'Unknown')
                    
                    # Get the actual downloaded file
                    downloaded_file = os.path.join(tmpdir, "audio.mp3")
                
                # Transcribe audio
                model = self._load_whisper_model()
                result = model.transcribe(downloaded_file, fp16=False)
                self.transcription_text = result["text"].strip()
            
            # Initialize RAG pipeline
            self._initialize_pipeline()
            
            # Ingest transcription
            num_chunks = self.pipeline.ingest_documents(text=self.transcription_text)
            
            self.current_video_url = video_url
            
            return {
                "success": True,
                "video_title": self.video_title,
                "transcription_length": len(self.transcription_text),
                "chunks_created": num_chunks
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _initialize_pipeline(self):
        """Initialize the RAG pipeline components."""
        # Create pipeline components
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
        self.pipeline = RAGPipeline(
            document_processor=doc_processor,
            embeddings_manager=embeddings_manager,
            vector_store_type=settings.vector_store.store_type,
            llm_client=llm_client,
            index_name=settings.vector_store.index_name,
            top_k=settings.vector_store.top_k
        )
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        Answer a question using the RAG pipeline.
        
        Args:
            question: User question
            
        Returns:
            Dictionary with answer and status
        """
        if self.pipeline is None:
            return {
                "success": False,
                "answer": "",
                "error": "No video has been processed yet. Please process a video first."
            }
        
        try:
            answer = self.pipeline.query(question)
            return {
                "success": True,
                "answer": answer
            }
        except Exception as e:
            return {
                "success": False,
                "answer": "",
                "error": str(e)
            }
    
    def search_chunks(self, query: str, num_chunks: int = 3) -> Dict[str, Any]:
        """
        Search for similar document chunks.
        
        Args:
            query: Search query
            num_chunks: Number of chunks to retrieve
            
        Returns:
            Dictionary with chunks and status
        """
        if self.pipeline is None:
            return {
                "success": False,
                "chunks": [],
                "error": "No video has been processed yet."
            }
        
        try:
            docs = self.pipeline.search_similar(query, k=num_chunks)
            chunks = [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in docs
            ]
            return {
                "success": True,
                "chunks": chunks
            }
        except Exception as e:
            return {
                "success": False,
                "chunks": [],
                "error": str(e)
            }
    
    def get_transcription(self) -> Dict[str, Any]:
        """
        Get the current transcription.
        
        Returns:
            Dictionary with transcription and status
        """
        if not self.transcription_text:
            return {
                "success": False,
                "transcription": "",
                "error": "No transcription available."
            }
        
        return {
            "success": True,
            "transcription": self.transcription_text
        }
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current service status.
        
        Returns:
            Dictionary with status information
        """
        return {
            "initialized": self.pipeline is not None,
            "video_url": self.current_video_url,
            "transcription_available": self.transcription_text is not None
        }