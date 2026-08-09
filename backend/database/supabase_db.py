import sys
from dotenv import load_dotenv

load_dotenv()

from database.client import get_user_client
from utils.logger import Logger

log = Logger().get_logger()


def signup(email: str, password: str, full_name: str | None = None) -> dict:
    """Register a new user using Supabase Authentication."""
    client = get_user_client()
    credentials = {"email": email.strip().lower(), "password": password}
    if full_name:
        credentials["options"] = {"data": {"full_name": full_name}}

    try:
        response = client.auth.sign_up(credentials)
        user = response.user
        if not user:
            raise RuntimeError("Signup response did not contain user object.")

        log.info(f"[bold green]✔ Supabase Signup Successful![/bold green]")
        log.info(f"User ID: [cyan]{user.id}[/cyan]")
        log.info(f"Email: [cyan]{user.email}[/cyan]")
        return {"user_id": user.id, "email": user.email}
    except Exception as e:
        log.error(f"[bold red]✘ Supabase Signup Failed:[/bold red] {e}")
        raise


def login(email: str, password: str) -> dict:
    """Log in an existing user using Supabase Authentication."""
    client = get_user_client()
    try:
        response = client.auth.sign_in_with_password({
            "email": email.strip().lower(),
            "password": password,
        })
        user = response.user
        session = response.session
        if not user:
            raise RuntimeError("Login response did not contain user object.")

        log.info(f"[bold green]✔ Supabase Login Successful![/bold green]")
        log.info(f"User ID: [cyan]{user.id}[/cyan]")
        log.info(f"Email: [cyan]{user.email}[/cyan]")
        if session:
            log.info(f"Access Token: [dim]{session.access_token[:30]}...[/dim]")

        return {
            "user_id": user.id,
            "email": user.email,
            "access_token": session.access_token if session else None,
        }
    except Exception as e:
        log.error(f"[bold red]✘ Supabase Login Failed:[/bold red] {e}")
        raise


def prompt_menu():
    print("\n" + "=" * 60)
    print(" SUPABASE AUTHENTICATION CLI TEST")
    print("=" * 60)
    print(" 1. Sign Up a new user")
    print(" 2. Log In an existing user")
    print(" 0. Exit")
    return input("\nSelect an option: ").strip()


def main():
    while True:
        choice = prompt_menu()

        if choice == "1":
            email = input("Enter Email: ").strip()
            password = input("Enter Password (min 6 chars): ").strip()
            full_name = input("Enter Full Name (optional): ").strip() or None

            if not email or not password:
                log.warning("Email and Password are required.")
                continue

            try:
                signup(email=email, password=password, full_name=full_name)
            except Exception:
                pass

        elif choice == "2":
            email = input("Enter Email: ").strip()
            password = input("Enter Password: ").strip()

            if not email or not password:
                log.warning("Email and Password are required.")
                continue

            try:
                login(email=email, password=password)
            except Exception:
                pass

        elif choice == "0":
            log.info("Exiting Supabase Auth CLI.")
            break
        else:
            log.warning("Invalid option. Try again.")



