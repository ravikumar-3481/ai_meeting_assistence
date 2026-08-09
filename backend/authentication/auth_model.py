from dataclasses import dataclass
from database.client import get_user_client
from utils.logger import Logger

log = Logger().get_logger()


@dataclass
class AuthResult:
    user_id: str
    email: str | None
    access_token: str
    refresh_token: str | None


class AuthService:
    def __init__(self):
        self._client = get_user_client()

    def sign_up(self, email: str, password: str, full_name: str | None = None) -> AuthResult:
        try:
            response = self._client.auth.sign_up(
                {
                    "email": email,
                    "password": password,
                    "options": {"data": {"full_name": full_name}} if full_name else {},
                }
            )
        except Exception as e:
            log.error(f"Sign up failed for {email}: {e}")
            raise

        session = response.session
        user = response.user

        if session is None:
            raise RuntimeError(
                "Signup succeeded but no session was returned. "
                "Check if email confirmation is required for this project."
            )

        return AuthResult(
            user_id=user.id,
            email=user.email,
            access_token=session.access_token,
            refresh_token=session.refresh_token,
        )

    def sign_in(self, email: str, password: str) -> AuthResult:
        try:
            response = self._client.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
        except Exception as e:
            log.error(f"Sign in failed for {email}: {e}")
            raise

        session = response.session
        user = response.user

        return AuthResult(
            user_id=user.id,
            email=user.email,
            access_token=session.access_token,
            refresh_token=session.refresh_token,
        )

    def sign_out(self, access_token: str) -> None:
        client = get_user_client(access_token)
        try:
            client.auth.sign_out()
        except Exception as e:
            log.warning(f"Sign out failed (non-fatal): {e}")