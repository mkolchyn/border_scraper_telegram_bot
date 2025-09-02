import os
import time
import json
from telegram import User
from dotenv import load_dotenv

load_dotenv()

USERS_LOG_FILE = os.getenv("USERS_LOG_FILE")

def load_users():
    if USERS_LOG_FILE and os.path.exists(USERS_LOG_FILE):
        with open(USERS_LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(users):
    if USERS_LOG_FILE:
        with open(USERS_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2, ensure_ascii=False)

def log_user_action(user: User, action: str):
    users = load_users()
    uid = str(user.id)
    if uid not in users:
        users[uid] = {
            "user_id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "joined_at": int(time.time()),
            "actions": []
        }
    users[uid]["actions"].append({
        "action": action,
        "timestamp": int(time.time())
    })
    save_users(users)
    # print(f"[LOG] {user.username or user.first_name} -> {action}")

def get_user_lang(user_id):
    users = load_users()
    uid = str(user_id)
    return users.get(uid, {}).get("lang", "en")

def set_user_lang(user: User, lang: str):
    users = load_users()
    uid = str(user.id)
    if uid not in users:
        users[uid] = {
            "user_id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "joined_at": int(time.time()),
            "actions": []
        }
    users[uid]["lang"] = lang
    save_users(users)
