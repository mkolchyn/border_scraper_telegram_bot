import os
import time
import json
import httpx
from io import BytesIO
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Update, User
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode


TOKEN = os.getenv("BOT_TOKEN")
SERVER_ADDRESS = os.getenv("SERVER_ADDRESS")
USERS_LOG_FILE = os.getenv("USERS_LOG_FILE")

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")

# ---------- User logging helpers ----------
def load_users():
    if os.path.exists(USERS_LOG_FILE):
        with open(USERS_LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(users):
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
    print(f"[LOG] {user.username or user.first_name} -> {action}")


# Menu structure
main_menu = [
    [InlineKeyboardButton("Lithuania 🇱🇹", callback_data='lithuania')],
    [InlineKeyboardButton("Latvia 🇱🇻", callback_data='latvia')],
    [InlineKeyboardButton("Poland 🇵🇱", callback_data='poland')]
]

lithuania_stats = [
    [InlineKeyboardButton("last 3 hours", callback_data='lt_3h'),
     InlineKeyboardButton("last 24 hours", callback_data='lt_24h')],
    [InlineKeyboardButton("last 7 days", callback_data='lt_7d'),
     InlineKeyboardButton("last 30 days", callback_data='lt_30d')],
    [InlineKeyboardButton("Back 🔙", callback_data='main')],
]

latvia_stats = [
    [InlineKeyboardButton("last 3 hours", callback_data='lv_3h'),
     InlineKeyboardButton("last 24 hours", callback_data='lv_24h')],
    [InlineKeyboardButton("last 7 days", callback_data='lv_7d'),
     InlineKeyboardButton("last 30 days", callback_data='lv_30d')],
    [InlineKeyboardButton("Back 🔙", callback_data='main')],
]

poland_stats = [
    [InlineKeyboardButton("last 3 hours", callback_data='pl_3h'),
     InlineKeyboardButton("last 24 hours", callback_data='pl_24h')],
    [InlineKeyboardButton("last 7 days", callback_data='pl_7d'),
     InlineKeyboardButton("last 30 days", callback_data='pl_30d')],
    [InlineKeyboardButton("Back 🔙", callback_data='main')],
]

# Unified lookup table: callback_data → (path_prefix, file_suffix, caption, keyboard, use_bytes)
CALLBACK_MAP = {
    "lt_3h":    ("lithuania", "queue_length_visual_3_hours.png",  "Queue length in the last 3 hours", lithuania_stats, True),
    "lt_24h":   ("lithuania", "queue_length_visual_24_hours.png", "Queue length in the last 24 hours", lithuania_stats, True),
    "lt_7d":    ("lithuania", "queue_length_visual_1_week.png",   "Queue length in the last 7 days",  lithuania_stats, True),
    "lt_30d":   ("lithuania", "queue_length_visual_1_month.png",  "Queue length in the last 30 days", lithuania_stats, True),

    "lv_3h":    ("latvia", "queue_length_visual_3_hours.png",  "Queue length in the last 3 hours", latvia_stats, True),
    "lv_24h":   ("latvia", "queue_length_visual_24_hours.png", "Queue length in the last 24 hours", latvia_stats, True),
    "lv_7d":    ("latvia", "queue_length_visual_1_week.png",   "Queue length in the last 7 days",  latvia_stats, True),
    "lv_30d":   ("latvia", "queue_length_visual_1_month.png",  "Queue length in the last 30 days", latvia_stats, True),

    "pl_3h":    ("poland", "queue_length_visual_3_hours.png",  "Queue length in the last 3 hours", poland_stats, True),
    "pl_24h":   ("poland", "queue_length_visual_24_hours.png", "Queue length in the last 24 hours", poland_stats, True),
    "pl_7d":    ("poland", "queue_length_visual_1_week.png",   "Queue length in the last 7 days",  poland_stats, True),
    "pl_30d":   ("poland", "queue_length_visual_1_month.png",  "Queue length in the last 30 days", poland_stats, True),
}

# Helper function
async def send_or_edit_photo(query, path_prefix, file_suffix, caption, keyboard, use_bytes=False):
    if path_prefix:
        url = f"http://{SERVER_ADDRESS}/{path_prefix}/{file_suffix}"
    else:
        url = f"http://{SERVER_ADDRESS}/{file_suffix}"

    if use_bytes:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            resp.raise_for_status()
            media = InputMediaPhoto(media=BytesIO(resp.content), caption=caption)
    else:
        # add cache-busting timestamp
        url_with_ts = f"{url}?{int(time.time())}"
        media = InputMediaPhoto(media=url_with_ts, caption=caption)

    await query.edit_message_media(
        media=media,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        log_user_action(update.message.from_user, "start")

    reply_markup = InlineKeyboardMarkup(main_menu)
    text = (
        "<b>Welcome!</b> 👋\n\n"
        "Here you can find <b>historical data</b> on queues at border crossing points "
        "from <b>Belarus ➝ EU</b>.\n\n"
        "The information is sourced from "
        "<a href='https://declarant.by'>declarant.by</a> "
        "and reflects the number of vehicles in <b>buffer zones</b>.\n\n"
        "➡️ <i>Choose a country:</i>"
    )
    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        log_user_action(update.message.from_user, "restart")

        reply_markup = InlineKeyboardMarkup(main_menu)
        text = (
            "<b>Welcome!</b> 👋\n\n"
            "Here you can find <b>historical data</b> on queues at border crossing points "
            "from <b>Belarus ➝ EU</b>.\n\n"
            "The information is sourced from "
            "<a href='https://declarant.by'>declarant.by</a> "
            "and reflects the number of vehicles in <b>buffer zones</b>.\n\n"
            "➡️ <i>Choose a country:</i>"
        )
        await update.message.reply_text(
            text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )

# Button handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # log every button press
    log_user_action(query.from_user, query.data)

    data = query.data
    if data == "main":
        await query.message.delete()
        reply_markup = InlineKeyboardMarkup(main_menu)
        await query.message.chat.send_message("Choose a country:", reply_markup=reply_markup)
    elif data in ("lithuania", "latvia", "poland"):
        menus = {"lithuania": lithuania_stats, "latvia": latvia_stats, "poland": poland_stats}
        await query.edit_message_text("Choose time range:", reply_markup=InlineKeyboardMarkup(menus[data]))
    elif data in CALLBACK_MAP:
        path_prefix, file_suffix, caption, keyboard, use_bytes = CALLBACK_MAP[data]
        await send_or_edit_photo(query, path_prefix, file_suffix, caption, keyboard, use_bytes)
    elif data == "exit":
        await query.edit_message_text("Goodbye! 👋")
    else:
        await query.edit_message_text(f"You selected: {data.capitalize()}")

# Main function
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("restart", restart))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
