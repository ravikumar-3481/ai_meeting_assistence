import uuid
from database.client import get_admin_client
from utils.logger import Logger

log = Logger().get_logger()


def is_valid_uuid(val: str) -> bool:
    try:
        uuid.UUID(str(val))
        return True
    except (ValueError, TypeError, AttributeError):
        return False


def insert_meeting(
    meeting_id: str,
    user_id: str,
    title: str,
    source_url: str,
    pinecone_namespace: str,
    language: str = "english",
    total_chunks: int = 0,
    duration_seconds: int | None = None,
    status: str = "ready",
) -> str:
    if not meeting_id or not meeting_id.strip():
        raise ValueError("meeting_id is required")
    if not user_id or not user_id.strip():
        raise ValueError("user_id is required")
    if not title or not title.strip():
        raise ValueError("title is required")
    if not pinecone_namespace or not pinecone_namespace.strip():
        raise ValueError("pinecone_namespace is required")

    data = {
        "id": meeting_id,
        "user_id": user_id,
        "title": title,
        "source_url": source_url,
        "language": language,
        "status": status,
        "pinecone_namespace": pinecone_namespace,
        "total_chunks": total_chunks,
        "duration_seconds": duration_seconds,
    }

    try:
        supabase = get_admin_client()
        response = supabase.table("meetings").insert(data).execute()
        inserted_row = response.data[0] if response.data else {}
        db_id = inserted_row.get("id", meeting_id)
        log.info(f"Meeting '{meeting_id}' stored in Supabase database (DB id: {db_id}) for user '{user_id}'.")
        return meeting_id
    except Exception as e:
        log.error(f"Failed to insert meeting '{meeting_id}' into Supabase: {e}")
        raise


def get_user_meetings(user_id: str) -> list[dict]:
    """Fetch all meetings belonging to a specific user from Supabase database."""
    if not user_id or not user_id.strip():
        raise ValueError("user_id is required")

    try:
        supabase = get_admin_client()
        response = (
            supabase.table("meetings")
            .select("id, user_id, title, source_url, language, status, pinecone_namespace, total_chunks, duration_seconds, created_at")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        meetings = response.data or []
        for m in meetings:
            p_ns = m.get("pinecone_namespace")
            if p_ns:
                m["id"] = p_ns

        user_email = user_id
        try:
            user_res = supabase.table("users").select("email").eq("id", user_id).execute()
            if user_res.data and user_res.data[0].get("email"):
                user_email = user_res.data[0]["email"]
        except Exception:
            pass

        log.info(f"Fetched {len(meetings)} meetings for user [bold green]'{user_email}'[/bold green] from Supabase.")
        return meetings
    except Exception as e:
        log.error(f"Failed to fetch meetings for user '[bold green]{user_email}[/bold green]': {e}")
        raise


def get_user_meeting(user_id: str, meeting_id: str) -> dict | None:
    if not user_id or not user_id.strip():
        raise ValueError("user_id is required")
    if not meeting_id or not meeting_id.strip():
        raise ValueError("meeting_id is required")

    try:
        supabase = get_admin_client()
        query = (
            supabase.table("meetings")
            .select("id, user_id, title, source_url, language, status, pinecone_namespace, total_chunks, duration_seconds, created_at")
            .eq("user_id", user_id)
        )

        if is_valid_uuid(meeting_id):
            response = query.eq("id", meeting_id).execute()
        else:
            response = query.eq("pinecone_namespace", meeting_id).execute()

        data = response.data or []
        if data:
            log.info(f"Fetched meeting '{meeting_id}' for user '{user_id}'.")
            return data[0]
        else:
            log.warning(f"No meeting found with id/namespace '{meeting_id}' for user '{user_id}'.")
            return None
    except Exception as e:
        log.error(f"Failed to fetch meeting '{meeting_id}' for user '{user_id}': {e}")
        raise


# Alias to support both naming conventions (get_meeting_by_id and get_user_meeting)
get_meeting_by_id = get_user_meeting
