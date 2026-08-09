"""
===============================================================================
SCHEMAS: MEETING & INGESTION
===============================================================================
Pydantic schemas for meeting creation, ingestion requests, metadata storage,
and database query outputs.
===============================================================================
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from schemas.common_schema import MeetingStatusEnum, MeetingLanguageEnum


class MeetingBase(BaseModel):
    """Base meeting attributes."""
    title: str = Field(..., max_length=255, description="Meeting title")
    source_url: Optional[str] = Field(None, description="YouTube URL or file transcript source")
    language: MeetingLanguageEnum = Field(MeetingLanguageEnum.ENGLISH, description="Meeting language")
    status: MeetingStatusEnum = Field(MeetingStatusEnum.READY, description="Meeting processing status")


class MeetingProcessRequest(BaseModel):
    """Payload sent by backend clients to process a new meeting source."""
    url_or_path: str = Field(..., description="YouTube URL or local file path to transcript (.txt)")
    user_id: str = Field("default_user", description="User ID associated with the meeting")
    language: MeetingLanguageEnum = Field(MeetingLanguageEnum.ENGLISH, description="Target language")


class MeetingLoadRequest(BaseModel):
    """Payload sent to load an existing meeting session."""
    meeting_id: str = Field(..., description="Meeting ID or Pinecone namespace")
    user_id: str = Field("default_user", description="User ID associated with the meeting")


class MeetingCreate(MeetingBase):
    """Schema for inserting a new meeting record into Supabase DB."""
    id: str = Field(..., max_length=150, description="App-generated meeting ID")
    user_id: str = Field(..., description="Supabase UUID of the meeting owner")
    pinecone_namespace: str = Field(..., max_length=150, description="Pinecone vector database namespace")
    total_chunks: int = Field(0, ge=0, description="Total text chunks generated")
    duration_seconds: Optional[int] = Field(None, ge=0, description="Audio duration in seconds")


class MeetingResponse(MeetingBase):
    """Complete meeting record returned from Supabase DB."""
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="Meeting ID")
    user_id: str = Field(..., description="User ID of the meeting owner")
    pinecone_namespace: str = Field(..., description="Pinecone vector namespace")
    total_chunks: int = Field(0, description="Number of vector chunks")
    duration_seconds: Optional[int] = Field(None, description="Audio duration in seconds")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")


class MeetingListResponse(BaseModel):
    """Response payload containing a list of meetings."""
    meetings: List[MeetingResponse] = Field(default_factory=list, description="List of meeting records")
    total_count: int = Field(0, description="Total number of meetings returned")
