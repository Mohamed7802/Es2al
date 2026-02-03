"""
Pydantic models for API request/response validation.
"""
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional


class VideoProcessRequest(BaseModel):
    """Request model for video processing."""
    video_url: str = Field(..., description="YouTube video URL")
    
    class Config:
        json_schema_extra = {
            "example": {
                "video_url": "https://www.youtube.com/watch?v=cdiD-9MMpb0"
            }
        }


class VideoProcessResponse(BaseModel):
    """Response model for video processing."""
    success: bool
    message: str
    video_title: Optional[str] = None
    transcription_length: Optional[int] = None
    chunks_created: Optional[int] = None
    error: Optional[str] = None


class ChatRequest(BaseModel):
    """Request model for chat/question answering."""
    question: str = Field(..., min_length=1, description="User question")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is the main topic of this video?"
            }
        }


class ChatResponse(BaseModel):
    """Response model for chat/question answering."""
    answer: str
    success: bool
    error: Optional[str] = None


class SearchRequest(BaseModel):
    """Request model for chunk search."""
    query: str = Field(..., min_length=1, description="Search query")
    num_chunks: int = Field(default=3, ge=1, le=10, description="Number of chunks to retrieve")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "neural networks",
                "num_chunks": 3
            }
        }


class ChunkData(BaseModel):
    """Model for a single document chunk."""
    content: str
    metadata: dict = {}


class SearchResponse(BaseModel):
    """Response model for chunk search."""
    chunks: List[ChunkData]
    success: bool
    error: Optional[str] = None


class TranscriptionResponse(BaseModel):
    """Response model for transcription retrieval."""
    transcription: str
    success: bool
    error: Optional[str] = None


class StatusResponse(BaseModel):
    """Response model for system status."""
    initialized: bool
    video_url: Optional[str] = None
    transcription_available: bool