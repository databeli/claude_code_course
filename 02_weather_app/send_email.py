"""Fake email 'sender' used as a Claude Code hook for notifications.

Instead of sending a real email, it writes an email.txt file with a
dummy subject/body so it can be wired up as a lightweight notification hook.
"""

from datetime import datetime
from pathlib import Path

OUTPUT_FILE = Path(__file__).parent / "email.txt"

SUBJECT = "Claude needs your input"
BODY = "Claude needs your input. Please check your session and respond."


def send_email(subject: str = SUBJECT, body: str = BODY) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = (
        f"To: databeli13@gmail.com\n"
        f"Subject: {subject}\n"
        f"Date: {timestamp}\n"
        f"\n"
        f"{body}\n"
    )
    OUTPUT_FILE.write_text(content, encoding="utf-8")
    print(f"Wrote dummy email to {OUTPUT_FILE}")


if __name__ == "__main__":
    send_email()
