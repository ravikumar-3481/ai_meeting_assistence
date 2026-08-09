"""
===============================================================================
SCHEMAS: COMMON & BASE TYPES
===============================================================================
Shared enums, generic API response wrappers, and audit log schemas.
===============================================================================
"""

from enum import Enum
from datetime import datetime
from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field, ConfigDict


class MeetingStatusEnum(str, Enum):
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"
    ARCHIVED = "archived"


class MeetingLanguageEnum(str, Enum):
    ENGLISH = "english"
    HINGLISH = "hinglish"
    HINDI = "hindi"


class ActionItemStatusEnum(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class AuditResultEnum(str, Enum):
    ALLOWED = "allowed"
    DENIED = "denied"


T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Standard generic API envelope response."""
    success: bool = True
    message: str = "Operation successful"
    data: Optional[T] = None
    error: Optional[str] = None


class AccessAuditLogCreate(BaseModel):
    """Schema for recording user access audit log entry."""
    user_id: str = Field(..., description="UUID of the accessing user")
    meeting_id: Optional[str] = Field(None, description="Target meeting ID if applicable")
    action: str = Field(..., description="Action name (e.g. read_transcript, query_agent)")
    result: AuditResultEnum = Field(AuditResultEnum.ALLOWED, description="Access check result")


class AccessAuditLogResponse(AccessAuditLogCreate):
    """Schema for audit log record returned from database."""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Audit log entry ID")
    accessed_at: datetime = Field(..., description="Timestamp of access event")
