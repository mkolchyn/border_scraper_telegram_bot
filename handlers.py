import re
from telegram import InlineKeyboardMarkup, InputMediaPhoto, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from texts import MAIN_MENU, STATS, CURRENT, ESTIMATIONS, CARTRACKING, language_menu
from menus import (
    build_car_tracking_menu_only,  
    build_main_menu, 
    build_current_menu, 
    build_stats_menu, 
    build_car_tracking_menu, 
    build_country_menu, 
    build_estimations_menu, 
    build_month_menu, 
    build_year_menu
)
from user_utils import (
    log_user_action, 
    get_user_lang, 
    set_user_lang, 
    send_or_edit_photo, 
    get_queue_length_current,
    set_user_car_into_db,
    remove_user_car_from_db
)
from db_functions import (
    get_queue_speed, 
    create_queue_table_image
)
from callbacks import CALLBACK_MAP, CALLBACK_MAP_ARCHIVE, CALLBACK_MAP_CURRENT


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

# /menu command
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        log_user_action(update.message.from_user, "menu")
        user_lang = get_user_lang(update.message.from_user.id)
        await update.message.reply_text(
            MAIN_MENU[user_lang]["welcome"], 
            reply_markup=InlineKeyboardMarkup(build_main_menu(user_lang)),
            parse_mode=ParseMode.HTML
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
            MAIN_MENU[lang]["welcome"],
            reply_markup=InlineKeyboardMarkup(build_main_menu(lang)),
            parse_mode=ParseMode.HTML
        )
        return

    if data == "current":
        await query.edit_message_text(
            CURRENT[user_lang]["current_info"],
            reply_markup=InlineKeyboardMarkup(build_current_menu(user_lang)),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        return

    if data == "stats":
        await query.edit_message_text(
            STATS[user_lang]["welcome"],
            reply_markup=InlineKeyboardMarkup(build_stats_menu(user_lang)),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        return

    if data == "estimations":
        await query.edit_message_text(
            ESTIMATIONS[user_lang]["choose_border_point"],
            reply_markup=InlineKeyboardMarkup(build_estimations_menu(user_lang))
        )
        return

    if data == "car_tracking":
        await query.edit_message_text(
            CARTRACKING[user_lang]["car_tracking_intro"],
            reply_markup=InlineKeyboardMarkup(build_car_tracking_menu(query,user_lang)),
            parse_mode=ParseMode.HTML
        )
        return
    
    elif data == "add_car":
        await query.edit_message_text(
            CARTRACKING[user_lang]["add_car_prompt"],
            reply_markup=InlineKeyboardMarkup(build_car_tracking_menu_only(user_lang)),
            parse_mode=ParseMode.HTML
        )
        # Mark that next text from this user should be treated as a plate number
        context.user_data["expecting_plate"] = True
        return
    
    elif data.startswith("remove_"):
        plate = data.replace("remove_", "", 1)  # extract the plate number
        user_id = query.from_user.id
        remove_user_car_from_db(user_id, plate)
        await query.edit_message_text(
            CARTRACKING[user_lang]["car_removed"].format(plate),
            reply_markup=InlineKeyboardMarkup(build_car_tracking_menu(query, user_lang)),
            parse_mode="HTML"
        )
        return

    if data in ("benyakoni", "brest_bts", "kamenny_log", "grigorovschina"):
        border_point_id = ESTIMATIONS[user_lang]["border_points_id"][data]
        
        # Fetch the latest queue speed data from the remote DB
        rows = get_queue_speed(border_point_id)
        
        # Create a table image
        img_bytes = create_queue_table_image(rows, title=f"Queue Speed at {data.replace('_', ' ').title()}")
        
        if img_bytes:
            await query.edit_message_media(
                media=InputMediaPhoto(
                    media=img_bytes,
                    caption=ESTIMATIONS[user_lang]["column_explanation"],
                    parse_mode=ParseMode.HTML
                ),
                reply_markup=InlineKeyboardMarkup(build_estimations_menu(user_lang))
            )
        else:
            await query.edit_message_text(
                "No data available.",
                reply_markup=InlineKeyboardMarkup(build_estimations_menu(user_lang))
            )
        return

    elif data == "menu":
        await query.message.delete()
        reply_markup = InlineKeyboardMarkup(build_main_menu(user_lang))
        await query.message.chat.send_message(
            MAIN_MENU[user_lang]["welcome"], 
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    elif data in ("lithuania", "latvia", "poland"):
        menu = build_country_menu(data, user_lang)
        await query.edit_message_text(STATS[user_lang]["choose_range"], reply_markup=InlineKeyboardMarkup(menu))

    elif data in ("lithuania_archive", "latvia_archive", "poland_archive"):
        await query.message.delete()
        country = data[:2]
        menu = build_year_menu(country, user_lang)
        await query.message.chat.send_message(STATS[user_lang]["choose_year"], reply_markup=InlineKeyboardMarkup(menu))

    elif data in ("li_2024", "la_2024", "po_2024", "li_2025", "la_2025", "po_2025"):
        country = data[:2]
        year = data.split("_")[1]
        menu = build_month_menu(country, year, user_lang)
        await query.edit_message_text(STATS[user_lang]["choose_month"], reply_markup=InlineKeyboardMarkup(menu))

    elif data in CALLBACK_MAP:
        path_prefix, file_suffix = CALLBACK_MAP[data]
        time_key = data.split("_")[1]
        caption = STATS[user_lang]["captions"][time_key]
        menu = build_country_menu(path_prefix, user_lang)
        await send_or_edit_photo(query, path_prefix, file_suffix, caption, menu, use_bytes=True)

    elif data in CALLBACK_MAP_ARCHIVE:
        path_prefix, file_suffix = CALLBACK_MAP_ARCHIVE[data]
        time_key = "_".join(data.split("_")[1:])
        year = data.split("_")[1]
        caption = STATS[user_lang]["captions"][time_key]
        menu = build_month_menu(path_prefix, year, user_lang)
        await send_or_edit_photo(query, path_prefix, file_suffix, caption, menu, use_bytes=True, archive=True)

    elif data in CALLBACK_MAP_CURRENT:
        checkpoint_id, border_points_names = CALLBACK_MAP_CURRENT[data]
        countCar, countTruck, countBus, countMotorcycle = get_queue_length_current(checkpoint_id)

        message = ESTIMATIONS[user_lang]["border_points_names"][border_points_names] + "\n\n"
        message += f"🚗 {countCar}    🚚 {countTruck}    🚌 {countBus}    🏍️ {countMotorcycle}\n\n"

        await query.edit_message_text(
            message,
            reply_markup=InlineKeyboardMarkup(build_current_menu(user_lang)),
            parse_mode=ParseMode.HTML
        )
        return

    elif data == "exit":
        await query.edit_message_text(STATS[user_lang]["goodbye"])
    else:
        await query.edit_message_text(f"You selected: {data.capitalize()}")


async def handle_plate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("expecting_plate"):
        return  # ignore text not related to add_car flow

    PLATE_PATTERN = re.compile(r'^(?=.*[A-Z])(?=.*\d)[A-Z0-9]{1,7}$')
    plate = update.message.text.strip().upper()
    user_lang = get_user_lang(update.message.from_user.id)

    if PLATE_PATTERN.match(plate):
        set_user_car_into_db(update.message.from_user, plate, user_lang)
        await update.message.reply_text(
            CARTRACKING[user_lang]["car_added"].format(plate),
            reply_markup=InlineKeyboardMarkup(build_car_tracking_menu(update.message, user_lang)),
            parse_mode="HTML"
        )
        
        context.user_data["expecting_plate"] = False
    else:
        await update.message.reply_text(
            CARTRACKING[user_lang]["car_added_error"],
            reply_markup=InlineKeyboardMarkup(build_car_tracking_menu(update.message, user_lang)),
            parse_mode="HTML"
        )