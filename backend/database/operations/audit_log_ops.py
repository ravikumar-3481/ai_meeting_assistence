from database.client import get_admin_client
from utils.logger import Logger

log = Logger().get_logger()


def insert_audit_log(
    user_id: str | None = None,
    meeting_id: str | None = None,
    action: str = "",
    result: str = "allowed",
) -> dict:
    """Insert an entry into public.access_audit_log."""
    if not action or not action.strip():
        raise ValueError("action description is required")

    data = {
        "user_id": user_id,
        "meeting_id": meeting_id,
        "action": action.strip(),
        "result": result.strip() if result else "allowed",
    }

    try:
        supabase = get_admin_client()
        response = supabase.table("access_audit_log").insert(data).execute()
        inserted = response.data[0] if response.data else {}
        log.info(f"Inserted audit log: action='{action}', result='{result}'.")
        return inserted
    except Exception as e:
        log.error(f"Failed to insert audit log entry: {e}")
        raise


def get_audit_logs_by_user(user_id: str, limit: int = 50) -> list[dict]:
    """Fetch access audit logs for a given user_id."""
    if not user_id or not user_id.strip():
        raise ValueError("user_id is required")

    try:
        supabase = get_admin_client()
        response = (
            supabase.table("access_audit_log")
            .select("id, user_id, meeting_id, action, accessed_at, result")
            .eq("user_id", user_id)
            .order("accessed_at", desc=True)
            .limit(limit)
            .execute()
        )
        logs = response.data or []
        log.info(f"Fetched {len(logs)} audit log records for user '{user_id}'.")
        return logs
    except Exception as e:
        log.error(f"Failed to fetch audit logs for user '{user_id}': {e}")
        raise


def get_audit_logs_by_meeting(meeting_id: str, limit: int = 50) -> list[dict]:
    """Fetch access audit logs for a given meeting_id."""
    if not meeting_id or not meeting_id.strip():
        raise ValueError("meeting_id is required")

    try:
        supabase = get_admin_client()
        response = (
            supabase.table("access_audit_log")
            .select("id, user_id, meeting_id, action, accessed_at, result")
            .eq("meeting_id", meeting_id)
            .order("accessed_at", desc=True)
            .limit(limit)
            .execute()
        )
        logs = response.data or []
        log.info(f"Fetched {len(logs)} audit log records for meeting '{meeting_id}'.")
        return logs
    except Exception as e:
        log.error(f"Failed to fetch audit logs for meeting '{meeting_id}': {e}")
        raise


def get_recent_audit_logs(limit: int = 50) -> list[dict]:
    """Fetch recent global access audit log records."""
    try:
        supabase = get_admin_client()
        response = (
            supabase.table("access_audit_log")
            .select("id, user_id, meeting_id, action, accessed_at, result")
            .order("accessed_at", desc=True)
            .limit(limit)
            .execute()
        )
        logs = response.data or []
        log.info(f"Fetched {len(logs)} recent audit log records.")
        return logs
    except Exception as e:
        log.error(f"Failed to fetch recent audit logs: {e}")
        raise


class AuditLogOperations:
    """Class wrapper providing methods for public.access_audit_log table operations."""

    @staticmethod
    def insert_log(
        user_id: str | None = None,
        meeting_id: str | None = None,
        action: str = "",
        result: str = "allowed",
    ) -> dict:
        return insert_audit_log(user_id, meeting_id, action, result)

    @staticmethod
    def get_by_user(user_id: str, limit: int = 50) -> list[dict]:
        return get_audit_logs_by_user(user_id, limit)

    @staticmethod
    def get_by_meeting(meeting_id: str, limit: int = 50) -> list[dict]:
        return get_audit_logs_by_meeting(meeting_id, limit)

    @staticmethod
    def get_recent(limit: int = 50) -> list[dict]:
        return get_recent_audit_logs(limit)
