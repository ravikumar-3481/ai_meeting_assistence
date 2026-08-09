from supabase import create_client, Client
from api.config import Config
from utils.logger import Logger

log = Logger().get_logger()
_config = Config()


def get_admin_client() -> Client:
    return create_client(
        _config.supabase_url,
        _config.supabase_service_role_key.get_secret_value(),
    )


def get_user_client(access_token: str | None = None) -> Client:
    client = create_client(
        _config.supabase_url,
        _config.supabase_anon_key.get_secret_value(),
    )
    if access_token:
        client.postgrest.auth(access_token)
    return client


supabase_admin: Client = get_admin_client()