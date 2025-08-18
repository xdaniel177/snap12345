import os

USERS_FILE = "users.txt"

def save_user(user_id: int, username: str = ""):
    """Speichert ID + Username (wenn vorhanden)"""
    if not os.path.exists(USERS_FILE):
        open(USERS_FILE, "w").close()

    with open(USERS_FILE, "r") as f:
        lines = f.read().splitlines()

    # Prüfen ob ID schon drin ist
    if any(line.startswith(str(user_id) + ",") for line in lines):
        return

    # Username leer -> nur ID speichern
    if username:
        entry = f"{user_id},{username}"
    else:
        entry = f"{user_id}"

    with open(USERS_FILE, "a") as f:
        f.write(entry + "\n")
