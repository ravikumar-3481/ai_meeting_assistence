from database.client import get_admin_client
from utils.logger import Logger

log = Logger().get_logger()


def insert_output_meta(meeting_id: str, output_type: str) -> dict:
    """Insert a record into public.meeting_outputs_meta table."""
    if not meeting_id or not meeting_id.strip():
        raise ValueError("meeting_id is required")
    if not output_type or not output_type.strip():
        raise ValueError("output_type is required")

    data = {
        "meeting_id": meeting_id,
        "output_type": output_type.strip(),
    }

    try:
        supabase = get_admin_client()
        response = supabase.table("meeting_outputs_meta").insert(data).execute()
        inserted = response.data[0] if response.data else {}
        log.info(f"Inserted output meta '{output_type}' for meeting '{meeting_id}'.")
        return inserted
    except Exception as e:
        log.error(f"Failed to insert output meta for meeting '{meeting_id}': {e}")
        raise


def get_outputs_meta_by_meeting(meeting_id: str) -> list[dict]:
    """Fetch all output metadata records for a given meeting_id."""
    if not meeting_id or not meeting_id.strip():
        raise ValueError("meeting_id is required")

    try:
        supabase = get_admin_client()
        response = (
            supabase.table("meeting_outputs_meta")
            .select("id, meeting_id, output_type, generated_at")
            .eq("meeting_id", meeting_id)
            .order("generated_at", desc=True)
            .execute()
        )
        records = response.data or []
        log.info(f"Fetched {len(records)} output meta records for meeting '{meeting_id}'.")
        return records
    except Exception as e:
        log.error(f"Failed to fetch output meta for meeting '{meeting_id}': {e}")
        raise


def get_latest_output_meta(meeting_id: str, output_type: str) -> dict | None:
    """Fetch the latest output metadata record for a specific output_type and meeting_id."""
    if not meeting_id or not meeting_id.strip():
        raise ValueError("meeting_id is required")
    if not output_type or not output_type.strip():
        raise ValueError("output_type is required")

    try:
        supabase = get_admin_client()
        response = (
            supabase.table("meeting_outputs_meta")
            .select("id, meeting_id, output_type, generated_at")
            .eq("meeting_id", meeting_id)
            .eq("output_type", output_type.strip())
            .order("generated_at", desc=True)
            .limit(1)
            .execute()
        )
        data = response.data or []
        if data:
            return data[0]
        return None
    except Exception as e:
        log.error(f"Failed to fetch latest output meta '{output_type}' for meeting '{meeting_id}': {e}")
        raise


def delete_outputs_meta_by_meeting(meeting_id: str) -> bool:
    """Delete all output metadata records for a given meeting_id."""
    if not meeting_id or not meeting_id.strip():
        raise ValueError("meeting_id is required")

    try:
        supabase = get_admin_client()
        response = supabase.table("meeting_outputs_meta").delete().eq("meeting_id", meeting_id).execute()
        log.info(f"Deleted output meta records for meeting '{meeting_id}'.")
        return bool(response.data)
    except Exception as e:
        log.error(f"Failed to delete output meta for meeting '{meeting_id}': {e}")
        raise


class OutputMetaOperations:
    """Class wrapper providing methods for public.meeting_outputs_meta table operations."""

    @staticmethod
    def insert_meta(meeting_id: str, output_type: str) -> dict:
        return insert_output_meta(meeting_id, output_type)

    @staticmethod
    def get_by_meeting(meeting_id: str) -> list[dict]:
        return get_outputs_meta_by_meeting(meeting_id)

    @staticmethod
    def get_latest(meeting_id: str, output_type: str) -> dict | None:
        return get_latest_output_meta(meeting_id, output_type)

    @staticmethod
    def delete_by_meeting(meeting_id: str) -> bool:
        return delete_outputs_meta_by_meeting(meeting_id)
