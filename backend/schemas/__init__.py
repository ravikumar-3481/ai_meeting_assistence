"""
===============================================================================
SCHEMAS PACKAGE ENTRY POINT
===============================================================================
Central package export for all application Pydantic schemas.
===============================================================================
"""

from schemas.common_schema import (
    MeetingStatusEnum,
    MeetingLanguageEnum,
    ActionItemStatusEnum,
    AuditResultEnum,
    APIResponse,
    AccessAuditLogCreate,
    AccessAuditLogResponse,
)

from schemas.user_schema import (
    UserBase,
    UserCreate,
    UserLogin,
    UserResetPassword,
    UserResponse,
    AuthTokenResponse,
)

from schemas.meeting_schema import (
    MeetingBase,
    MeetingProcessRequest,
    MeetingLoadRequest,
    MeetingCreate,
    MeetingResponse,
    MeetingListResponse,
)

from schemas.chunk_schema import (
    ChunkMetadata,
    MeetingChunkCreate,
    MeetingChunkResponse,
    BatchChunkEmbeddingRequest,
)

from schemas.action_item_schema import (
    ActionItemBase,
    ActionItemCreate,
    ActionItemUpdate,
    ActionItemResponse,
    MeetingOutputMetaResponse,
)

from schemas.chat_schema import (
    ChatMessage,
    ChatQueryRequest,
    ChatQueryResponse,
    ActiveSessionState,
)

__all__ = [
    # Common / Base
    "MeetingStatusEnum",
    "MeetingLanguageEnum",
    "ActionItemStatusEnum",
    "AuditResultEnum",
    "APIResponse",
    "AccessAuditLogCreate",
    "AccessAuditLogResponse",
    # User / Auth
    "UserBase",
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "AuthTokenResponse",
    # Meeting
    "MeetingBase",
    "MeetingProcessRequest",
    "MeetingLoadRequest",
    "MeetingCreate",
    "MeetingResponse",
    "MeetingListResponse",
    # Chunks
    "ChunkMetadata",
    "MeetingChunkCreate",
    "MeetingChunkResponse",
    "BatchChunkEmbeddingRequest",
    # Action Items
    "ActionItemBase",
    "ActionItemCreate",
    "ActionItemUpdate",
    "ActionItemResponse",
    "MeetingOutputMetaResponse",
    # Chat / Agent
    "ChatMessage",
    "ChatQueryRequest",
    "ChatQueryResponse",
    "ActiveSessionState",
]
