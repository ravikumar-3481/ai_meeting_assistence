from database.client import get_admin_client
from utils.logger import Logger

log = Logger().get_logger()


def get_user_profile(user_id: str) -> dict | None:
    """Fetch user profile by user_id from public.users table."""
    if not user_id or not user_id.strip():
        raise ValueError("user_id is required")

    try:
        supabase = get_admin_client()
        response = (
            supabase.table("users")
            .select("id, email, full_name, created_at, updated_at")
            .eq("id", user_id)
            .execute()
        )
        data = response.data or []
        if data:
            log.info(f"Fetched user profile for user_id '{user_id}'.")
            return data[0]
        else:
            log.warning(f"No user profile found for user_id '{user_id}'.")
            return None
    except Exception as e:
        log.error(f"Failed to fetch user profile for '{user_id}': {e}")
        raise


def get_user_by_email(email: str) -> dict | None:
    """Fetch user profile by email from public.users table."""
    if not email or not email.strip():
        raise ValueError("email is required")

    try:
        supabase = get_admin_client()
        response = (
            supabase.table("users")
            .select("id, email, full_name, created_at, updated_at")
            .eq("email", email.strip().lower())
            .execute()
        )
        data = response.data or []
        if data:
            log.info(f"Fetched user profile for email '{email}'.")
            return data[0]
        else:
            log.warning(f"No user profile found for email '{email}'.")
            return None
    except Exception as e:
        log.error(f"Failed to fetch user profile for email '{email}': {e}")
        raise


def update_user_profile(
    user_id: str,
    full_name: str | None = None,
    email: str | None = None,
) -> dict:
    """Update user profile fields (full_name, email) in public.users table."""
    if not user_id or not user_id.strip():
        raise ValueError("user_id is required")

    update_fields = {}
    if full_name is not None:
        update_fields["full_name"] = full_name
    if email is not None:
        update_fields["email"] = email.strip().lower()

    if not update_fields:
        raise ValueError("At least one field (full_name or email) must be provided to update.")

    try:
        supabase = get_admin_client()
        response = (
            supabase.table("users")
            .update(update_fields)
            .eq("id", user_id)
            .execute()
        )
        data = response.data or []
        if data:
            log.info(f"Updated user profile for user_id '{user_id}'.")
            return data[0]
        else:
            log.warning(f"No user profile updated for user_id '{user_id}'.")
            return {}
    except Exception as e:
        log.error(f"Failed to update user profile for '{user_id}': {e}")
        raise


def delete_user_profile(user_id: str) -> bool:
    """Delete user profile from public.users table."""
    if not user_id or not user_id.strip():
        raise ValueError("user_id is required")

    try:
        supabase = get_admin_client()
        response = supabase.table("users").delete().eq("id", user_id).execute()
        log.info(f"Deleted user profile for user_id '{user_id}'.")
        return bool(response.data)
    except Exception as e:
        log.error(f"Failed to delete user profile for '{user_id}': {e}")
        raise


def list_users(limit: int = 50, offset: int = 0) -> list[dict]:
    """List user profiles with pagination."""
    try:
        supabase = get_admin_client()
        response = (
            supabase.table("users")
            .select("id, email, full_name, created_at, updated_at")
            .range(offset, offset + limit - 1)
            .order("created_at", desc=True)
            .execute()
        )
        users = response.data or []
        log.info(f"Fetched {len(users)} user profiles.")
        return users
    except Exception as e:
        log.error(f"Failed to list user profiles: {e}")
        raise


class UserOperations:
    """Class wrapper providing methods for public.users table operations."""

    @staticmethod
    def get_profile(user_id: str) -> dict | None:
        return get_user_profile(user_id)

    @staticmethod
    def get_by_email(email: str) -> dict | None:
        return get_user_by_email(email)

    @staticmethod
    def update_profile(user_id: str, full_name: str | None = None, email: str | None = None) -> dict:
        return update_user_profile(user_id, full_name, email)

    @staticmethod
    def delete_profile(user_id: str) -> bool:
        return delete_user_profile(user_id)

    @staticmethod
    def list_all(limit: int = 50, offset: int = 0) -> list[dict]:
        return list_users(limit, offset)
