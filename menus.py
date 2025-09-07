from telegram import InlineKeyboardButton
from texts import BUTTONS

def build_main_menu(lang: str):
    return [
        [InlineKeyboardButton(BUTTONS[lang]["stats"], callback_data="stats")],
        [InlineKeyboardButton(BUTTONS[lang]["estimations"], callback_data="estimations")]
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
        [InlineKeyboardButton(BUTTONS[lang]["menu"], callback_data="menu")],
    ]
