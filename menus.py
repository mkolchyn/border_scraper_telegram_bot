from telegram import InlineKeyboardButton
from texts import BUTTONS
from user_utils import (
    get_user_cars_from_db,
    get_user_car_notifications_from_db
)


def build_main_menu(lang: str):
    return [
        [InlineKeyboardButton(BUTTONS[lang]["current"], callback_data="current")],
        [InlineKeyboardButton(BUTTONS[lang]["stats"], callback_data="stats")],
        [InlineKeyboardButton(BUTTONS[lang]["estimations"], callback_data="estimations")],
        [InlineKeyboardButton(BUTTONS[lang]["car_tracking"], callback_data="car_tracking")],
    ]

def build_current_menu(lang: str):
    return [
        [InlineKeyboardButton(BUTTONS[lang]["kamenny_log"], callback_data="curr_kamenny_log")],
        [InlineKeyboardButton(BUTTONS[lang]["benyakoni"], callback_data="curr_benyakoni")],
        [InlineKeyboardButton(BUTTONS[lang]["brest_bts"], callback_data="curr_brest_bts")],
        [InlineKeyboardButton(BUTTONS[lang]["kozlovichi"], callback_data="curr_kozlovichi")],
        [InlineKeyboardButton(BUTTONS[lang]["grigorovschina"], callback_data="curr_grigorovschina")],
        [InlineKeyboardButton(BUTTONS[lang]["menu"], callback_data="menu")],
    ]

def build_stats_menu(lang: str):
    return [
        [InlineKeyboardButton(BUTTONS[lang]["country_lt"], callback_data="lithuania")],
        [InlineKeyboardButton(BUTTONS[lang]["country_lv"], callback_data="latvia")],
        [InlineKeyboardButton(BUTTONS[lang]["country_pl"], callback_data="poland")],
        [InlineKeyboardButton(BUTTONS[lang]["menu"], callback_data="menu")],
    ]

def build_estimations_menu(lang: str):
    return [
        [InlineKeyboardButton(BUTTONS[lang]["kamenny_log"], callback_data="kamenny_log")],
        [InlineKeyboardButton(BUTTONS[lang]["benyakoni"], callback_data="benyakoni")],
        [InlineKeyboardButton(BUTTONS[lang]["brest_bts"], callback_data="brest_bts")],
        [InlineKeyboardButton(BUTTONS[lang]["grigorovschina"], callback_data="grigorovschina")],
        [InlineKeyboardButton(BUTTONS[lang]["menu"], callback_data="menu")],
    ]

def build_country_menu(country: str, lang: str):
    return [
        [InlineKeyboardButton(BUTTONS[lang]["3h"], callback_data=f"{country[:2]}_3h"),
         InlineKeyboardButton(BUTTONS[lang]["24h"], callback_data=f"{country[:2]}_24h")],
        [InlineKeyboardButton(BUTTONS[lang]["7d"], callback_data=f"{country[:2]}_7d"),
         InlineKeyboardButton(BUTTONS[lang]["30d"], callback_data=f"{country[:2]}_30d")],
        [InlineKeyboardButton(BUTTONS[lang]["archive"], callback_data=f"{country}_archive")],
        [InlineKeyboardButton(BUTTONS[lang]["stats_back"], callback_data="stats_back")],
        [InlineKeyboardButton(BUTTONS[lang]["menu"], callback_data="menu")],
    ]

def build_year_menu(country: str, lang: str):
    return [
        [InlineKeyboardButton(BUTTONS[lang]["2024"], callback_data=f"{country[:2]}_2024"),
         InlineKeyboardButton(BUTTONS[lang]["2025"], callback_data=f"{country[:2]}_2025")],
        [InlineKeyboardButton(BUTTONS[lang]["menu"], callback_data="menu")],
    ]

def build_month_menu(country: str, year: str, lang: str):
    months = [
        ("jan", "january"),
        ("feb", "february"),
        ("mar", "march"),
        ("apr", "april"),
        ("may", "may"),
        ("jun", "june"),
        ("jul", "july"),
        ("aug", "august"),
        ("sep", "september"),
        ("oct", "october"),
        ("nov", "november"),
        ("dec", "december"),
    ]

    # If you want to hide some months for 2024 (like Jan–Mar)
    if year == "2024":
        months = months[3:]  # from April onward
    elif year == "2025":
        months = months[:8]   # January → August

    keyboard = []
    for i in range(0, len(months), 2):  # 2 per row
        row = []
        for code, key in months[i:i+2]:
            row.append(
                InlineKeyboardButton(
                    BUTTONS[lang][key], 
                    callback_data=f"{country[:2]}_{year}_{code}"
                )
            )
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton(BUTTONS[lang]["menu"], callback_data="menu")])
    return keyboard

def build_car_type_menu(lang: str):
    return [
        [InlineKeyboardButton(BUTTONS[lang]["car_type_passenger"], callback_data="car_type_passenger"),
         InlineKeyboardButton(BUTTONS[lang]["car_type_freight"], callback_data="car_type_freight")],
        [InlineKeyboardButton(BUTTONS[lang]["menu"], callback_data="menu")]
    ]

def build_car_tracking_menu_only(lang: str):
    return [
        [InlineKeyboardButton(BUTTONS[lang]["car_tracking"], callback_data="car_tracking")]
    ]

def build_car_tracking_menu(query, car_type: str, lang: str):
    user_id = query.from_user.id
    cars = get_user_cars_from_db(user_id, car_type)

    keyboard = []
    # Create a button for each car
    if cars:
        for car in cars:
            keyboard.append(
                [InlineKeyboardButton(car, callback_data=f"track_{car}"),
                InlineKeyboardButton(BUTTONS[lang]["settings_car"], callback_data=f"settings_{car}"),
                InlineKeyboardButton(BUTTONS[lang]["remove_car"], callback_data=f"remove_car_{car}")]
            )
        if len(cars) < 5:  # Limit to 5 cars
            keyboard.append([InlineKeyboardButton(BUTTONS[lang]["add_car"], callback_data="add_car")])
    else:
        keyboard.append([InlineKeyboardButton(BUTTONS[lang]["add_car"], callback_data="add_car")])
        
    keyboard.append([InlineKeyboardButton(BUTTONS[lang]["car_tracking_back"], callback_data="car_tracking")])
    keyboard.append([InlineKeyboardButton(BUTTONS[lang]["menu"], callback_data="menu")])
        
    return keyboard

def build_car_settings_menu(user_id, car: str, lang: str):
    notifications = get_user_car_notifications_from_db(user_id, car, None, None)

    keyboard = []
    if notifications:
        for notification in notifications:
            if notification.notification_status:
                status = "🔔"
                command = "disable"
            else:
                status = "🔕"
                command = "enable"

            if notification.notification_type == "number-in-queue":
                button_name = BUTTONS[lang]["notification_type_number_in_queue"].format(notification.notification_value)
            elif notification.notification_type == "every-n-minutes":
                button_name = BUTTONS[lang]["notification_type_every_n_minutes"].format(notification.notification_value)
            elif notification.notification_type == "every-n-cars":
                button_name = BUTTONS[lang]["notification_type_every_n_cars"].format(notification.notification_value)
            elif notification.notification_type == "summoned":
                button_name = BUTTONS[lang]["notification_type_summoned"]

            keyboard.append(
                [InlineKeyboardButton(button_name + status, callback_data=command + f"_{notification.surr_id}_{notification.car_plate}"),
                InlineKeyboardButton(BUTTONS[lang]["remove_notification"], callback_data=f"remove_notification_{notification.surr_id}_{notification.car_plate}")]
            )
        if len(notifications) < 5:
            keyboard.append([InlineKeyboardButton(BUTTONS[lang]["add_notification"], callback_data=f"add_notification_{car}")])
            keyboard.append([InlineKeyboardButton(BUTTONS[lang]["car_tracking_back"], callback_data="car_tracking")])
    else:
        keyboard.append([InlineKeyboardButton(BUTTONS[lang]["add_notification"], callback_data=f"add_notification_{car}")])
        keyboard.append([InlineKeyboardButton(BUTTONS[lang]["car_tracking_back"], callback_data="car_tracking")])

    keyboard.append([InlineKeyboardButton(BUTTONS[lang]["menu"], callback_data="menu")])
    
    return keyboard

def build_notification_type_menu(plate: str, lang: str):
    return [
        [InlineKeyboardButton(BUTTONS[lang]["set_notification_type_number_in_queue"], callback_data=f"set_notification_type_{plate}_number-in-queue")],
        [InlineKeyboardButton(BUTTONS[lang]["set_notification_type_every_n_minutes"], callback_data=f"set_notification_type_{plate}_every-n-minutes")],
        [InlineKeyboardButton(BUTTONS[lang]["set_notification_type_every_n_cars"], callback_data=f"set_notification_type_{plate}_every-n-cars")],
        [InlineKeyboardButton(BUTTONS[lang]["set_notification_type_summoned"], callback_data=f"set_notification_type_{plate}_summoned")],
        [InlineKeyboardButton(BUTTONS[lang]["selected_car_settings"], callback_data=f"settings_{plate}")],
        [InlineKeyboardButton(BUTTONS[lang]["menu"], callback_data="menu")]
    ]

def build_notification_number_in_queue_menu(plate: str, lang: str):
    return [
        [InlineKeyboardButton("1", callback_data=f"set_notification_value_{plate}_number-in-queue_1"),
         InlineKeyboardButton("5", callback_data=f"set_notification_value_{plate}_number-in-queue_5"),
         InlineKeyboardButton("10", callback_data=f"set_notification_value_{plate}_number-in-queue_10")],
        [InlineKeyboardButton("20", callback_data=f"set_notification_value_{plate}_number-in-queue_20"),
         InlineKeyboardButton("50", callback_data=f"set_notification_value_{plate}_number-in-queue_50"),
         InlineKeyboardButton("100", callback_data=f"set_notification_value_{plate}_number-in-queue_100")],
        [InlineKeyboardButton(BUTTONS[lang]["selected_car_settings"], callback_data=f"settings_{plate}")],
        [InlineKeyboardButton(BUTTONS[lang]["menu"], callback_data="menu")]
    ]

def build_notification_every_n_minutes_menu(plate: str, lang: str):
    return [
        [InlineKeyboardButton("5", callback_data=f"set_notification_value_{plate}_every-n-minutes_5"),
         InlineKeyboardButton("15", callback_data=f"set_notification_value_{plate}_every-n-minutes_15"),
         InlineKeyboardButton("30", callback_data=f"set_notification_value_{plate}_every-n-minutes_30")],
        [InlineKeyboardButton("60", callback_data=f"set_notification_value_{plate}_every-n-minutes_60"),
         InlineKeyboardButton("120", callback_data=f"set_notification_value_{plate}_every-n-minutes_120"),
         InlineKeyboardButton("240", callback_data=f"set_notification_value_{plate}_every-n-minutes_240")],
        [InlineKeyboardButton(BUTTONS[lang]["selected_car_settings"], callback_data=f"settings_{plate}")],
        [InlineKeyboardButton(BUTTONS[lang]["menu"], callback_data="menu")]
    ]

def build_notification_every_n_cars_menu(plate: str, lang: str):
    return [
        [InlineKeyboardButton("1", callback_data=f"set_notification_value_{plate}_every-n-cars_1"),
         InlineKeyboardButton("5", callback_data=f"set_notification_value_{plate}_every-n-cars_5"),
         InlineKeyboardButton("10", callback_data=f"set_notification_value_{plate}_every-n-cars_10")],
        [InlineKeyboardButton("20", callback_data=f"set_notification_value_{plate}_every-n-cars_20"),
         InlineKeyboardButton("50", callback_data=f"set_notification_value_{plate}_every-n-cars_50"),
         InlineKeyboardButton("100", callback_data=f"set_notification_value_{plate}_every-n-cars_100")],
        [InlineKeyboardButton(BUTTONS[lang]["selected_car_settings"], callback_data=f"settings_{plate}")],
        [InlineKeyboardButton(BUTTONS[lang]["menu"], callback_data="menu")]
    ]



