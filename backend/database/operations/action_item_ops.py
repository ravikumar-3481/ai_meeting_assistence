from database.client import get_admin_client
from utils.logger import Logger

log = Logger().get_logger()


def insert_action_item(
    meeting_id: str,
    task: str,
    owner: str | None = None,
    due_date: str | None = None,
    status: str = "open",
) -> dict:
    """Insert a single action item into public.action_items."""
    if not meeting_id or not meeting_id.strip():
        raise ValueError("meeting_id is required")
    if not task or not task.strip():
        raise ValueError("task description is required")

    data = {
        "meeting_id": meeting_id,
        "task": task.strip(),
        "owner": owner.strip() if owner else None,
        "due_date": due_date.strip() if due_date else None,
        "status": status.strip(),
    }

    try:
        supabase = get_admin_client()
        response = supabase.table("action_items").insert(data).execute()
        inserted = response.data[0] if response.data else {}
        log.info(f"Inserted action item for meeting '{meeting_id}': '{task[:30]}...'")
        return inserted
    except Exception as e:
        log.error(f"Failed to insert action item for meeting '{meeting_id}': {e}")
        raise


def bulk_insert_action_items(meeting_id: str, items: list[dict]) -> list[dict]:
    """
    Bulk insert action items into public.action_items.
    Each item in list should have at least 'task'. Optional: 'owner', 'due_date', 'status'.
    """
    if not meeting_id or not meeting_id.strip():
        raise ValueError("meeting_id is required")
    if not items:
        log.warning(f"No action items provided for bulk insert into meeting '{meeting_id}'.")
        return []

    records = []
    for item in items:
        task = item.get("task")
        if not task or not str(task).strip():
            raise ValueError("Each action item dict must contain a non-empty 'task'")
        records.append({
            "meeting_id": meeting_id,
            "task": str(task).strip(),
            "owner": item.get("owner"),
            "due_date": item.get("due_date"),
            "status": item.get("status", "open"),
        })

    try:
        supabase = get_admin_client()
        response = supabase.table("action_items").insert(records).execute()
        inserted_records = response.data or []
        log.info(f"Bulk inserted {len(inserted_records)} action items for meeting '{meeting_id}'.")
        return inserted_records
    except Exception as e:
        log.error(f"Failed to bulk insert action items for meeting '{meeting_id}': {e}")
        raise


def get_action_items_by_meeting(meeting_id: str, status: str | None = None) -> list[dict]:
    """Fetch action items for a given meeting_id, optionally filtered by status."""
    if not meeting_id or not meeting_id.strip():
        raise ValueError("meeting_id is required")

    try:
        supabase = get_admin_client()
        query = (
            supabase.table("action_items")
            .select("id, meeting_id, task, owner, due_date, status, created_at")
            .eq("meeting_id", meeting_id)
        )
        if status:
            query = query.eq("status", status.strip())

        response = query.order("created_at", desc=False).execute()
        items = response.data or []
        log.info(f"Fetched {len(items)} action items for meeting '{meeting_id}'.")
        return items
    except Exception as e:
        log.error(f"Failed to fetch action items for meeting '{meeting_id}': {e}")
        raise


def update_action_item(
    action_item_id: str,
    task: str | None = None,
    owner: str | None = None,
    due_date: str | None = None,
    status: str | None = None,
) -> dict:
    """Update fields of an action item in public.action_items."""
    if not action_item_id or not action_item_id.strip():
        raise ValueError("action_item_id is required")

    update_fields = {}
    if task is not None:
        update_fields["task"] = task.strip()
    if owner is not None:
        update_fields["owner"] = owner.strip()
    if due_date is not None:
        update_fields["due_date"] = due_date.strip()
    if status is not None:
        update_fields["status"] = status.strip()

    if not update_fields:
        raise ValueError("At least one field must be provided to update action item.")

    try:
        supabase = get_admin_client()
        response = (
            supabase.table("action_items")
            .update(update_fields)
            .eq("id", action_item_id)
            .execute()
        )
        data = response.data or []
        if data:
            log.info(f"Updated action item '{action_item_id}'.")
            return data[0]
        return {}
    except Exception as e:
        log.error(f"Failed to update action item '{action_item_id}': {e}")
        raise


def update_action_item_status(action_item_id: str, status: str) -> dict:
    """Helper method to update only the status of an action item."""
    return update_action_item(action_item_id=action_item_id, status=status)


def delete_action_item(action_item_id: str) -> bool:
    """Delete a single action item by ID."""
    if not action_item_id or not action_item_id.strip():
        raise ValueError("action_item_id is required")

    try:
        supabase = get_admin_client()
        response = supabase.table("action_items").delete().eq("id", action_item_id).execute()
        log.info(f"Deleted action item '{action_item_id}'.")
        return bool(response.data)
    except Exception as e:
        log.error(f"Failed to delete action item '{action_item_id}': {e}")
        raise


def delete_action_items_by_meeting(meeting_id: str) -> bool:
    """Delete all action items for a specific meeting_id."""
    if not meeting_id or not meeting_id.strip():
        raise ValueError("meeting_id is required")

    try:
        supabase = get_admin_client()
        response = supabase.table("action_items").delete().eq("meeting_id", meeting_id).execute()
        log.info(f"Deleted action items for meeting '{meeting_id}'.")
        return bool(response.data)
    except Exception as e:
        log.error(f"Failed to delete action items for meeting '{meeting_id}': {e}")
        raise


class ActionItemOperations:
    """Class wrapper providing methods for public.action_items table operations."""

    @staticmethod
    def insert_item(
        meeting_id: str,
        task: str,
        owner: str | None = None,
        due_date: str | None = None,
        status: str = "open",
    ) -> dict:
        return insert_action_item(meeting_id, task, owner, due_date, status)

    @staticmethod
    def bulk_insert(meeting_id: str, items: list[dict]) -> list[dict]:
        return bulk_insert_action_items(meeting_id, items)

    @staticmethod
    def get_by_meeting(meeting_id: str, status: str | None = None) -> list[dict]:
        return get_action_items_by_meeting(meeting_id, status)

    @staticmethod
    def update_item(
        action_item_id: str,
        task: str | None = None,
        owner: str | None = None,
        due_date: str | None = None,
        status: str | None = None,
    ) -> dict:
        return update_action_item(action_item_id, task, owner, due_date, status)

    @staticmethod
    def update_status(action_item_id: str, status: str) -> dict:
        return update_action_item_status(action_item_id, status)

    @staticmethod
    def delete_item(action_item_id: str) -> bool:
        return delete_action_item(action_item_id)

    @staticmethod
    def delete_by_meeting(meeting_id: str) -> bool:
        return delete_action_items_by_meeting(meeting_id)
