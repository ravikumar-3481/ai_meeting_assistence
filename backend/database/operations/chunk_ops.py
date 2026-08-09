from database.client import get_admin_client
from utils.logger import Logger

log = Logger().get_logger()


def insert_meeting_chunk(meeting_id: str, chunk_index: int, vector_id: str) -> dict:
    """Insert a single meeting chunk into public.meeting_chunks."""
    if not meeting_id or not meeting_id.strip():
        raise ValueError("meeting_id is required")
    if chunk_index is None or chunk_index < 0:
        raise ValueError("valid chunk_index is required")
    if not vector_id or not vector_id.strip():
        raise ValueError("vector_id is required")

    data = {
        "meeting_id": meeting_id,
        "chunk_index": chunk_index,
        "vector_id": vector_id,
    }

    try:
        supabase = get_admin_client()
        response = supabase.table("meeting_chunks").insert(data).execute()
        inserted = response.data[0] if response.data else {}
        log.info(f"Inserted meeting chunk index {chunk_index} for meeting '{meeting_id}'.")
        return inserted
    except Exception as e:
        log.error(f"Failed to insert meeting chunk for '{meeting_id}': {e}")
        raise


def bulk_insert_meeting_chunks(meeting_id: str, chunks: list[dict]) -> list[dict]:
    """
    Bulk insert meeting chunks into public.meeting_chunks.
    Each item in chunks should contain 'chunk_index' and 'vector_id'.
    """
    if not meeting_id or not meeting_id.strip():
        raise ValueError("meeting_id is required")
    if not chunks:
        log.warning(f"No chunks provided for bulk insert into meeting '{meeting_id}'.")
        return []

    records = []
    for c in chunks:
        c_idx = c.get("chunk_index")
        v_id = c.get("vector_id")
        if c_idx is None or not v_id:
            raise ValueError("Each chunk dict must contain 'chunk_index' and 'vector_id'")
        records.append({
            "meeting_id": meeting_id,
            "chunk_index": c_idx,
            "vector_id": v_id,
        })

    try:
        supabase = get_admin_client()
        response = supabase.table("meeting_chunks").insert(records).execute()
        inserted_records = response.data or []
        log.info(f"Bulk inserted {len(inserted_records)} chunks for meeting '{meeting_id}'.")
        return inserted_records
    except Exception as e:
        log.error(f"Failed to bulk insert meeting chunks for '{meeting_id}': {e}")
        raise


def get_chunks_by_meeting(meeting_id: str) -> list[dict]:
    """Fetch all meeting chunks for a given meeting_id, ordered by chunk_index."""
    if not meeting_id or not meeting_id.strip():
        raise ValueError("meeting_id is required")

    try:
        supabase = get_admin_client()
        response = (
            supabase.table("meeting_chunks")
            .select("id, meeting_id, chunk_index, vector_id, created_at")
            .eq("meeting_id", meeting_id)
            .order("chunk_index", desc=False)
            .execute()
        )
        chunks = response.data or []
        log.info(f"Fetched {len(chunks)} chunks for meeting '{meeting_id}'.")
        return chunks
    except Exception as e:
        log.error(f"Failed to fetch chunks for meeting '{meeting_id}': {e}")
        raise


def get_chunk_by_index(meeting_id: str, chunk_index: int) -> dict | None:
    """Fetch a specific chunk by meeting_id and chunk_index."""
    if not meeting_id or not meeting_id.strip():
        raise ValueError("meeting_id is required")
    if chunk_index is None or chunk_index < 0:
        raise ValueError("valid chunk_index is required")

    try:
        supabase = get_admin_client()
        response = (
            supabase.table("meeting_chunks")
            .select("id, meeting_id, chunk_index, vector_id, created_at")
            .eq("meeting_id", meeting_id)
            .eq("chunk_index", chunk_index)
            .execute()
        )
        data = response.data or []
        if data:
            return data[0]
        return None
    except Exception as e:
        log.error(f"Failed to fetch chunk index {chunk_index} for meeting '{meeting_id}': {e}")
        raise


def delete_chunks_by_meeting(meeting_id: str) -> bool:
    """Delete all chunks for a specific meeting_id."""
    if not meeting_id or not meeting_id.strip():
        raise ValueError("meeting_id is required")

    try:
        supabase = get_admin_client()
        response = supabase.table("meeting_chunks").delete().eq("meeting_id", meeting_id).execute()
        log.info(f"Deleted chunks for meeting '{meeting_id}'.")
        return bool(response.data)
    except Exception as e:
        log.error(f"Failed to delete chunks for meeting '{meeting_id}': {e}")
        raise


def delete_chunk_by_id(chunk_id: str) -> bool:
    """Delete a single meeting chunk by its UUID id."""
    if not chunk_id or not chunk_id.strip():
        raise ValueError("chunk_id is required")

    try:
        supabase = get_admin_client()
        response = supabase.table("meeting_chunks").delete().eq("id", chunk_id).execute()
        log.info(f"Deleted chunk '{chunk_id}'.")
        return bool(response.data)
    except Exception as e:
        log.error(f"Failed to delete chunk '{chunk_id}': {e}")
        raise


class ChunkOperations:
    """Class wrapper providing methods for public.meeting_chunks table operations."""

    @staticmethod
    def insert_chunk(meeting_id: str, chunk_index: int, vector_id: str) -> dict:
        return insert_meeting_chunk(meeting_id, chunk_index, vector_id)

    @staticmethod
    def bulk_insert(meeting_id: str, chunks: list[dict]) -> list[dict]:
        return bulk_insert_meeting_chunks(meeting_id, chunks)

    @staticmethod
    def get_by_meeting(meeting_id: str) -> list[dict]:
        return get_chunks_by_meeting(meeting_id)

    @staticmethod
    def get_by_index(meeting_id: str, chunk_index: int) -> dict | None:
        return get_chunk_by_index(meeting_id, chunk_index)

    @staticmethod
    def delete_by_meeting(meeting_id: str) -> bool:
        return delete_chunks_by_meeting(meeting_id)

    @staticmethod
    def delete_by_id(chunk_id: str) -> bool:
        return delete_chunk_by_id(chunk_id)
