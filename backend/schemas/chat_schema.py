"""
===============================================================================
SCHEMAS: CHAT & AGENT INTERACTIONS
===============================================================================
Pydantic schemas for chat queries, message roles, conversation histories,
and agent responses.
===============================================================================
"""

from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Individual chat message within conversation history."""
    role: str = Field(..., description="Role of the sender ('human', 'ai', or 'system')")
    content: str = Field(..., description="Text content of the message")
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Timestamp of message")


class ChatQueryRequest(BaseModel):
    """Payload sent by clients to ask the Meeting AI Agent a question."""
    question: str = Field(..., min_length=1, description="User question about the meeting")
    meeting_id: str = Field(..., description="Active meeting ID")
    user_id: str = Field("default_user", description="User ID")
    chat_history: List[ChatMessage] = Field(default_factory=list, description="Prior conversation history")


class ChatQueryResponse(BaseModel):
    """Response returned by the Meeting AI Agent."""
    answer: str = Field(..., description="Agent's generated answer")
    meeting_id: str = Field(..., description="Active meeting ID")
    session_id: str = Field(..., description="Active session ID ('user_id:meeting_id')")
    updated_history: List[ChatMessage] = Field(default_factory=list, description="Updated conversation history")


class ActiveSessionState(BaseModel):
    """Active transcript and vector session state maintained in memory."""
    session_id: str = Field(..., description="Active session key")
    meeting_id: str = Field(..., description="Meeting ID")
    pinecone_namespace: str = Field(..., description="Pinecone namespace target")
    total_chunks: int = Field(0, description="Total chunks loaded in session")
