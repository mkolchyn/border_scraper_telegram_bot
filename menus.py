from telegram import InlineKeyboardButton
from texts import BUTTONS

def build_main_menu(lang: str):
    return [
        [InlineKeyboardButton(BUTTONS[lang]["current"], callback_data="current")],
        [InlineKeyboardButton(BUTTONS[lang]["stats"], callback_data="stats")],
        [InlineKeyboardButton(BUTTONS[lang]["estimations"], callback_data="estimations")]
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
