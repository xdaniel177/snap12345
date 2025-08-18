import os

USERS_FILE = "users.txt"

def save_user(user_id: int, username: str = "", first_name: str = ""):
    """Speichert jeden User, der /start gemacht hat"""
    if not os.path.exists(USERS_FILE):
        open(USERS_FILE, "w").close()

    with open(USERS_FILE, "r") as f:
        lines = f.read().splitlines()

    # wenn ID schon gespeichert, nix tun
    if any(line.startswith(str(user_id) + ",") for line in lines):
        return  

    with open(USERS_FILE, "a") as f:
        f.write(f"{user_id},{username},{first_name}\n")
