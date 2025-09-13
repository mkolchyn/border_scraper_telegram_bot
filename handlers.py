import re
from multiprocessing import Process
from telegram import InlineKeyboardMarkup, InputMediaPhoto, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from texts import MAIN_MENU, STATS, CURRENT, ESTIMATIONS, CARTRACKING, language_menu
from tracking_car import track_user_car
from menus import (
    build_car_tracking_menu_only,  
    build_main_menu, 
    build_current_menu, 
    build_stats_menu, 
    build_car_tracking_menu, 
    build_country_menu, 
    build_estimations_menu, 
    build_month_menu, 
    build_year_menu,
    build_car_settings_menu,
    build_notification_type_menu,
    build_notification_number_in_queue_menu,
    build_notification_every_n_minutes_menu,
    build_notification_every_n_cars_menu
)
from user_utils import (
    log_user_action, 
    get_user_lang, 
    set_user_lang, 
    send_or_edit_photo, 
    get_queue_length_current,
    set_user_car_into_db,
    remove_user_car_from_db,
    get_user_cars_current_status,
    set_user_car_notification_in_db,
    get_user_car_notifications_from_db,
    remove_all_user_car_notifications_from_db,
    remove_user_car_notification_from_db,
    deactivate_user_car_notification_in_db,
    activate_user_car_notification_in_db

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

    elif data == "current":
        await query.edit_message_text(
            CURRENT[user_lang]["current_info"],
            reply_markup=InlineKeyboardMarkup(build_current_menu(user_lang)),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        return

    elif data == "stats":
        await query.edit_message_text(
            STATS[user_lang]["welcome"],
            reply_markup=InlineKeyboardMarkup(build_stats_menu(user_lang)),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        return

    elif data == "estimations":
        await query.edit_message_text(
            ESTIMATIONS[user_lang]["choose_border_point"],
            reply_markup=InlineKeyboardMarkup(build_estimations_menu(user_lang))
        )
        return

    elif data == "car_tracking":
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
    
    elif data.startswith("remove_car"):
        parts = data.split("_", 2)
        plate = parts[2]  # extract the plate number
        user_id = query.from_user.id
        remove_user_car_from_db(user_id, plate)
        remove_all_user_car_notifications_from_db(user_id, plate)
        await query.edit_message_text(
            CARTRACKING[user_lang]["car_removed"].format(plate),
            reply_markup=InlineKeyboardMarkup(build_car_tracking_menu(query, user_lang)),
            parse_mode="HTML"
        )
        return

    elif data.startswith("track_"):
        plate = data.replace("track_", "", 1)  # extract the plate number
        user_id = query.from_user.id
        car_info = get_user_cars_current_status(plate)

        if car_info:
            buffer_zone_name, regnum, order_id, registration_date, status = car_info
            await query.edit_message_text(
                CARTRACKING[user_lang]["car_found_in_queue"].format(plate) + "\n" +
                CARTRACKING[user_lang]["car_status_details"].format(buffer_zone_name.capitalize(), regnum, order_id, registration_date),
                reply_markup=InlineKeyboardMarkup(build_car_tracking_menu(query, user_lang)),
                parse_mode="HTML"
            )
        else:
            await query.edit_message_text(
                CARTRACKING[user_lang]["car_not_found_in_queue"].format(plate),
                reply_markup=InlineKeyboardMarkup(build_car_tracking_menu(query, user_lang)),
                parse_mode="HTML"
            )
        return

    elif data.startswith("settings_"):
        plate = data.replace("settings_", "", 1)  # extract the plate number
        user_id = query.from_user.id

        await query.edit_message_text(
            CARTRACKING[user_lang]["car_notification_settings"].format(plate),
            reply_markup=InlineKeyboardMarkup(build_car_settings_menu(user_id, plate, user_lang)),
            parse_mode="HTML"
        )

    elif data.startswith("add_notification_"):
        parts = data.split("_", 3)
        car_plate = parts[2]
        user_id = query.from_user.id

        await query.edit_message_text(
            CARTRACKING[user_lang]["add_notification_type"].format(car_plate),
            reply_markup=InlineKeyboardMarkup(build_notification_type_menu(car_plate, user_lang)),
            parse_mode="HTML"
        )

    elif data.startswith("set_notification_type_"):
        parts = data.split("_")
        car_plate = parts[3]
        notification_type = parts[4]

        if notification_type == "number-in-queue":
            await query.edit_message_text(
                CARTRACKING[user_lang]["set_notification_value_number_in_queue"],
                reply_markup=InlineKeyboardMarkup(build_notification_number_in_queue_menu(car_plate, user_lang)),
                parse_mode="HTML"
            )
        elif notification_type == "every-n-minutes":
            await query.edit_message_text(
                CARTRACKING[user_lang]["set_notification_value_every_n_minutes"],
                reply_markup=InlineKeyboardMarkup(build_notification_every_n_minutes_menu(car_plate, user_lang)),
                parse_mode="HTML"
            )
        elif notification_type == "every-n-cars":
            await query.edit_message_text(
                CARTRACKING[user_lang]["set_notification_value_every_n_cars"],
                reply_markup=InlineKeyboardMarkup(build_notification_every_n_cars_menu(car_plate, user_lang)),
                parse_mode="HTML"
            )

    elif data.startswith("set_notification_value_"):
        parts = data.split("_")
        car_plate = parts[3]
        notification_type = parts[4]
        notification_value = parts[5]
        user_id = query.from_user.id
    
        set_user_car_notification_in_db(user_id, car_plate, notification_type, notification_value)

        await query.edit_message_text(
            CARTRACKING[user_lang]["notification_added"].format(car_plate),
            reply_markup=InlineKeyboardMarkup(build_car_settings_menu(user_id, car_plate, user_lang)),
            parse_mode="HTML"
        )


    elif data.startswith("remove_notification_"):
        parts = data.split("_", 3)
        notification_surr_id = parts[2] # exctract notification id
        car_plate = parts[3]  # extract the plate number
        remove_user_car_notification_from_db(notification_surr_id)
        await query.edit_message_text(
            CARTRACKING[user_lang]["notification_removed"].format(car_plate),
            reply_markup=InlineKeyboardMarkup(build_car_settings_menu(query.from_user.id, car_plate, user_lang)),
            parse_mode="HTML"
        )
        return

    elif data.startswith("enable_") or data.startswith("disable_"):
        action, notification_surr_id, car_plate = data.split("_", 2)
        if action == "enable":
            if activate_user_car_notification_in_db(notification_surr_id, car_plate):
                p = Process(target=track_user_car, args=(notification_surr_id, user_lang))
                p.start()
                message = CARTRACKING[user_lang]["notification_status_enabled"]
            else:
                message = CARTRACKING[user_lang]["notification_activation_failed"]
        else:
            deactivate_user_car_notification_in_db(notification_surr_id)
            message = CARTRACKING[user_lang]["notification_status_disabled"]

        await query.edit_message_text(
            message,
            reply_markup=InlineKeyboardMarkup(build_car_settings_menu(query.from_user.id, car_plate, user_lang)),
            parse_mode="HTML"
        )
        return

    elif data in ("benyakoni", "brest_bts", "kamenny_log", "grigorovschina"):
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

        if border_points_names in ("benyakoni", "kamenny_log", "grigorovschina"):
            message = ESTIMATIONS[user_lang]["border_points_names"][border_points_names] + "\n\n"
            message += f"🚗 {countCar}    🚚 {countTruck}    🚌 {countBus}    🏍️ {countMotorcycle}\n\n"
        elif border_points_names in ("brest_bts"):
            message = ESTIMATIONS[user_lang]["border_points_names"][border_points_names] + "\n\n"
            message += f"🚗 {countCar}    🚌 {countBus}    🏍️ {countMotorcycle}\n\n"
        elif border_points_names in ("kozlovichi"):
            message = ESTIMATIONS[user_lang]["border_points_names"][border_points_names] + "\n\n"
            message += f"🚚 {countTruck}"

        await query.edit_message_text(
            message,
            reply_markup=InlineKeyboardMarkup(build_current_menu(user_lang)),
            parse_mode=ParseMode.HTML
        )
        return

    elif data == "noop":
        await query.answer()  # silently ignore

    elif data == "exit":
        await query.edit_message_text(STATS[user_lang]["goodbye"])
    else:
        await query.edit_message_text(f"You selected: {data.capitalize()}")

async def handle_plate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("expecting_plate"):
        return  # ignore text not related to add_car flow

    PLATE_PATTERN = re.compile(r'^(?=.*[A-Z])(?=.*\d)[A-Z0-9]{1,10}$')
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