"""
Database Operations Package

Contains functions and class methods for interacting with SQL database tables
defined in database/schema.sql:
- public.users
- public.meeting_chunks
- public.meeting_outputs_meta
- public.action_items
- public.access_audit_log
"""

from database.operations.user_ops import (
    get_user_profile,
    get_user_by_email,
    update_user_profile,
    delete_user_profile,
    list_users,
    UserOperations,
)
from database.operations.chunk_ops import (
    insert_meeting_chunk,
    bulk_insert_meeting_chunks,
    get_chunks_by_meeting,
    get_chunk_by_index,
    delete_chunks_by_meeting,
    delete_chunk_by_id,
    ChunkOperations,
)
from database.operations.output_meta_ops import (
    insert_output_meta,
    get_outputs_meta_by_meeting,
    get_latest_output_meta,
    delete_outputs_meta_by_meeting,
    OutputMetaOperations,
)
from database.operations.action_item_ops import (
    insert_action_item,
    bulk_insert_action_items,
    get_action_items_by_meeting,
    update_action_item,
    update_action_item_status,
    delete_action_item,
    delete_action_items_by_meeting,
    ActionItemOperations,
)
from database.operations.audit_log_ops import (
    insert_audit_log,
    get_audit_logs_by_user,
    get_audit_logs_by_meeting,
    get_recent_audit_logs,
    AuditLogOperations,
)

__all__ = [
    # User Ops
    "get_user_profile",
    "get_user_by_email",
    "update_user_profile",
    "delete_user_profile",
    "list_users",
    "UserOperations",
    # Chunk Ops
    "insert_meeting_chunk",
    "bulk_insert_meeting_chunks",
    "get_chunks_by_meeting",
    "get_chunk_by_index",
    "delete_chunks_by_meeting",
    "delete_chunk_by_id",
    "ChunkOperations",
    # Output Meta Ops
    "insert_output_meta",
    "get_outputs_meta_by_meeting",
    "get_latest_output_meta",
    "delete_outputs_meta_by_meeting",
    "OutputMetaOperations",
    # Action Item Ops
    "insert_action_item",
    "bulk_insert_action_items",
    "get_action_items_by_meeting",
    "update_action_item",
    "update_action_item_status",
    "delete_action_item",
    "delete_action_items_by_meeting",
    "ActionItemOperations",
    # Audit Log Ops
    "insert_audit_log",
    "get_audit_logs_by_user",
    "get_audit_logs_by_meeting",
    "get_recent_audit_logs",
    "AuditLogOperations",
]
