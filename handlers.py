import time
import httpx
from io import BytesIO
from telegram import InlineKeyboardMarkup, InputMediaPhoto, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from texts import TEXTS, language_menu
from menus import build_main_menu, build_country_menu
from user_utils import log_user_action, get_user_lang, set_user_lang
from callbacks import CALLBACK_MAP
import os
from dotenv import load_dotenv

load_dotenv()

SERVER_ADDRESS = os.getenv("SERVER_ADDRESS")

# Send or edit photo
async def send_or_edit_photo(query, path_prefix, file_suffix, caption, keyboard, use_bytes=False):
    url = f"http://{SERVER_ADDRESS}/{path_prefix}/{file_suffix}"

    if use_bytes:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            resp.raise_for_status()
            media = InputMediaPhoto(media=BytesIO(resp.content), caption=caption)
    else:
        url_with_ts = f"{url}?{int(time.time())}"
        media = InputMediaPhoto(media=url_with_ts, caption=caption)

    await query.edit_message_media(
        media=media,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        log_user_action(update.message.from_user, "start")
        await update.message.reply_text(
            "Please choose your language / Пожалуйста, выберите язык:",
            reply_markup=InlineKeyboardMarkup(language_menu)
        )

# /restart command
async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        log_user_action(update.message.from_user, "restart")
        await update.message.reply_text(
            "Please choose your language / Пожалуйста, выберите язык:",
            reply_markup=InlineKeyboardMarkup(language_menu)
        )

# Button handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    log_user_action(query.from_user, query.data)

    data = query.data
    user_lang = get_user_lang(query.from_user.id)

    if data in ("lang_en", "lang_ru"):
        lang = "en" if data == "lang_en" else "ru"
        set_user_lang(query.from_user, lang)
        await query.edit_message_text(
            TEXTS[lang]["welcome"],
            reply_markup=InlineKeyboardMarkup(build_main_menu(lang)),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        return

    if data == "main":
        await query.message.delete()
        reply_markup = InlineKeyboardMarkup(build_main_menu(user_lang))
        await query.message.chat.send_message(TEXTS[user_lang]["choose_country"], reply_markup=reply_markup)

    elif data in ("lithuania", "latvia", "poland"):
        menu = build_country_menu(data, user_lang)
        await query.edit_message_text(TEXTS[user_lang]["choose_range"], reply_markup=InlineKeyboardMarkup(menu))

    elif data in CALLBACK_MAP:
        path_prefix, file_suffix = CALLBACK_MAP[data]
        time_key = data.split("_")[1]
        caption = TEXTS[user_lang]["captions"][time_key]
        menu = build_country_menu(path_prefix, user_lang)
        await send_or_edit_photo(query, path_prefix, file_suffix, caption, menu, use_bytes=True)

    elif data == "exit":
        await query.edit_message_text(TEXTS[user_lang]["goodbye"])
    else:
        await query.edit_message_text(f"You selected: {data.capitalize()}")
