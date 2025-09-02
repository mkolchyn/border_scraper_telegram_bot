from telegram import InlineKeyboardButton

# Translations for messages and captions
TEXTS = {
    "en": {
        "welcome": (
            "<b>Welcome!</b> 👋\n\n"
            "Here you can find <b>historical data</b> on queues at border crossing points "
            "from <b>Belarus ➝ EU</b>.\n\n"
            "The information is sourced from "
            "<a href='https://declarant.by'>declarant.by</a> "
            "and reflects the number of vehicles in <b>buffer zones</b>.\n\n"
            "➡️ <i>Choose a country:</i>"
        ),
        "choose_country": "Choose a country:",
        "choose_range": "Choose time range:",
        "goodbye": "Goodbye! 👋",
        "captions": {
            "3h": "Queue length in the last 3 hours",
            "24h": "Queue length in the last 24 hours",
            "7d": "Queue length in the last 7 days",
            "30d": "Queue length in the last 30 days",
        }
    },
    "ru": {
        "welcome": (
            "<b>Добро пожаловать!</b> 👋\n\n"
            "Здесь вы можете найти <b>исторические данные</b> об очередях "
            "на пограничных пунктах пропуска из <b>Беларуси ➝ ЕС</b>.\n\n"
            "Информация берётся с сайта "
            "<a href='https://declarant.by'>declarant.by</a> "
            "и отражает количество автомобилей в <b>буферных зонах</b>.\n\n"
            "➡️ <i>Выберите страну:</i>"
        ),
        "choose_country": "Выберите страну:",
        "choose_range": "Выберите период:",
        "goodbye": "До свидания! 👋",
        "captions": {
            "3h": "Очередь за последние 3 часа",
            "24h": "Очередь за последние 24 часа",
            "7d": "Очередь за последние 7 дней",
            "30d": "Очередь за последние 30 дней",
        }
    },
}

# Button labels
BUTTONS = {
    "en": {
        "country_lt": "Lithuania 🇱🇹",
        "country_lv": "Latvia 🇱🇻",
        "country_pl": "Poland 🇵🇱",
        "3h": "last 3 hours",
        "24h": "last 24 hours",
        "7d": "last 7 days",
        "30d": "last 30 days",
        "back": "Back 🔙",
    },
    "ru": {
        "country_lt": "Литва 🇱🇹",
        "country_lv": "Латвия 🇱🇻",
        "country_pl": "Польша 🇵🇱",
        "3h": "за 3 часа",
        "24h": "за 24 часа",
        "7d": "за 7 дней",
        "30d": "за 30 дней",
        "back": "Назад 🔙",
    },
}

# Language selection menu
language_menu = [
    [InlineKeyboardButton("English 🇬🇧", callback_data="lang_en")],
    [InlineKeyboardButton("Русский 🇷🇺", callback_data="lang_ru")],
]
