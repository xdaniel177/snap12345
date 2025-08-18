import os

USERS_FILE = "users.txt"

def save_user(user_id: int, username: str = "", first_name: str = ""):
    """Speichert User in users.txt, wenn nicht schon vorhanden."""
    if not os.path.exists(USERS_FILE):
        open(USERS_FILE, "w").close()

    with open(USERS_FILE, "r") as f:
        lines = f.read().splitlines()

    if any(line.startswith(str(user_id) + ",") for line in lines):
        return  # schon gespeichert

    with open(USERS_FILE, "a") as f:
        f.write(f"{user_id},{username},{first_name}\n")
