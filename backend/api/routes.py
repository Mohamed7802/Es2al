"""
API routes for the Video RAG system.
Defines all REST endpoints.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from api.models import (
    VideoProcessRequest,
    VideoProcessResponse,
    ChatRequest,
    ChatResponse,
    SearchRequest,
    SearchResponse,
    TranscriptionResponse,
    StatusResponse
)
from services.video_service import VideoRAGService

# Create router
router = APIRouter()

# Get service instance (singleton)
video_service = VideoRAGService()


@router.post("/video/process", response_model=VideoProcessResponse)
async def process_video(request: VideoProcessRequest):
    """
    Process a YouTube video: download, transcribe, and create RAG index.
    
    This endpoint may take several minutes depending on video length.
    """
    if not request.video_url:
        raise HTTPException(status_code=400, detail="Video URL is required")
    
    result = video_service.process_video(request.video_url)
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))
    
    return VideoProcessResponse(
        success=True,
        message="Video processed successfully",
        video_title=result.get("video_title"),
        transcription_length=result.get("transcription_length"),
        chunks_created=result.get("chunks_created")
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Ask a question about the processed video.
    
    Returns an AI-generated answer based on the video content.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    result = video_service.query(request.question)
    
    if not result["success"]:
        return ChatResponse(
            answer="",
            success=False,
            error=result.get("error")
        )
    
    return ChatResponse(
        answer=result["answer"],
        success=True
    )


@router.post("/search", response_model=SearchResponse)
async def search_chunks(request: SearchRequest):
    """
    Search for relevant chunks in the transcription.
    
    Returns similar document chunks without generating an answer.
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    result = video_service.search_chunks(request.query, request.num_chunks)
    
    if not result["success"]:
        return SearchResponse(
            chunks=[],
            success=False,
            error=result.get("error")
        )
    
    return SearchResponse(
        chunks=result["chunks"],
        success=True
    )


@router.get("/transcription", response_model=TranscriptionResponse)
async def get_transcription():
    """
    Get the full transcription of the processed video.
    """
    result = video_service.get_transcription()
    
    if not result["success"]:
        return TranscriptionResponse(
            transcription="",
            success=False,
            error=result.get("error")
        )
    
    return TranscriptionResponse(
        transcription=result["transcription"],
        success=True
    )


@router.get("/status", response_model=StatusResponse)
async def get_status():
    """
    Get the current status of the RAG system.
    """
    status = video_service.get_status()
    return StatusResponse(**status)