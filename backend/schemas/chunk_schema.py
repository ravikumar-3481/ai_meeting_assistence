"""
===============================================================================
SCHEMAS: MEETING CHUNKS & VECTOR EMBEDDINGS
===============================================================================
Pydantic schemas for text chunking, embedding vectors, and meeting_chunks DB records.
===============================================================================
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class ChunkMetadata(BaseModel):
    """Metadata representation for an individual transcript chunk."""
    chunk_index: int = Field(..., ge=0, description="Zero-based index of the chunk")
    meeting_id: str = Field(..., description="Parent meeting ID")
    vector_id: str = Field(..., description="Unique vector ID in Pinecone Cloud")
    content: Optional[str] = Field(None, description="Text snippet of the chunk")


class MeetingChunkCreate(BaseModel):
    """Schema for inserting chunk record into meeting_chunks table."""
    meeting_id: str = Field(..., description="Parent meeting ID")
    chunk_index: int = Field(..., ge=0, description="Chunk index number")
    vector_id: str = Field(..., description="Pinecone vector ID")


class MeetingChunkResponse(MeetingChunkCreate):
    """Schema returned from meeting_chunks table in Supabase."""
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="Unique UUID of the chunk entry")
    created_at: Optional[datetime] = Field(None, description="Insertion timestamp")


class BatchChunkEmbeddingRequest(BaseModel):
    """Request schema for batch chunk embedding generation."""
    chunks: List[str] = Field(..., min_length=1, description="List of text chunks to embed")
    meeting_id: str = Field(..., description="Meeting ID associated with the chunks")
