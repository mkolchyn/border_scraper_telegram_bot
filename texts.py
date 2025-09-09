from telegram import InlineKeyboardButton

# Language selection menu
language_menu = [
    [InlineKeyboardButton("English 🇬🇧", callback_data="lang_en")],
    [InlineKeyboardButton("Русский 🇷🇺", callback_data="lang_ru")],
]

MAIN_MENU = {
    "en": {
        "welcome": (
            "<b>Welcome to the Border Queue Bot!</b> 👋\n\n"
            "Here you can track border crossing queues from <b>Belarus ➝ EU</b> in real time, "
            "view historical statistics, and estimate the speed of passing through.\n\n"
            "➡️ Choose an option below to get started:"
        )
    },
    "ru": {
        "welcome": (
            "<b>Добро пожаловать в бота Очереди на границе!</b> 👋\n\n"
            "Здесь вы можете отслеживать очереди на границе из <b>Беларуси ➝ ЕС</b> в реальном времени, "
            "смотреть историческую статистику и оценивать скорость прохождения границы.\n\n"
            "➡️ Выберите действие ниже, чтобы начать:"
        )
    }   
}

# Translations for messages and captions
STATS = {
    "en": {
        "welcome": (
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
            "2024_jan": "Queue length in January 2024",
            "2024_feb": "Queue length in February 2024",
            "2024_mar": "Queue length in March 2024",
            "2024_apr": "Queue length in April 2024",
            "2024_may": "Queue length in May 2024",
            "2024_jun": "Queue length in June 2024",
            "2024_jul": "Queue length in July 2024",
            "2024_aug": "Queue length in August 2024",
            "2024_sep": "Queue length in September 2024",
            "2024_oct": "Queue length in October 2024",
            "2024_nov": "Queue length in November 2024",
            "2024_dec": "Queue length in December 2024",
            "2025_jan": "Queue length in January 2025",
            "2025_feb": "Queue length in February 2025",
            "2025_mar": "Queue length in March 2025",
            "2025_apr": "Queue length in April 2025",
            "2025_may": "Queue length in May 2025",
            "2025_jun": "Queue length in June 2025",
            "2025_jul": "Queue length in July 2025",
            "2025_aug": "Queue length in August 2025",
            "2025_sep": "Queue length in September 2025",
            "2025_oct": "Queue length in October 2025",
            "2025_nov": "Queue length in November 2025",
            "2025_dec": "Queue length in December 2025",
        },
        "choose_year": "Choose a year:",
        "choose_month": "Choose a month:"
    },
    "ru": {
        "welcome": (
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
            "2024_jan": "Очередь за январь 2024",
            "2024_feb": "Очередь за февраль 2024",
            "2024_mar": "Очередь за март 2024",
            "2024_apr": "Очередь за апрель 2024",
            "2024_may": "Очередь за май 2024",
            "2024_jun": "Очередь за июнь 2024",
            "2024_jul": "Очередь за июль 2024",
            "2024_aug": "Очередь за август 2024",
            "2024_sep": "Очередь за сентябрь 2024",
            "2024_oct": "Очередь за октябрь 2024",
            "2024_nov": "Очередь за ноябрь 2024",
            "2024_dec": "Очередь за декабрь 2024",
            "2025_jan": "Очередь за январь 2025",
            "2025_feb": "Очередь за февраль 2025",
            "2025_mar": "Очередь за март 2025",
            "2025_apr": "Очередь за апрель 2025",
            "2025_may": "Очередь за май 2025",
            "2025_jun": "Очередь за июнь 2025",
            "2025_jul": "Очередь за июль 2025",
            "2025_aug": "Очередь за август 2025",
            "2025_sep": "Очередь за сентябрь 2025",
            "2025_oct": "Очередь за октябрь 2025",
            "2025_nov": "Очередь за ноябрь 2025",
            "2025_dec": "Очередь за декабрь 2025"
        },
        "choose_year": "Выберите год:",
        "choose_month": "Выберите месяц:"
    },
}

ESTIMATIONS = {
    "en": {
        "welcome": (
            "<b>Estimate Border Speed</b> 🚦\n\n"
            "Here you can see the latest queue speed calculations based on data from buffer zones.\n"
            "This helps you estimate how quickly the line is moving and how long you might wait.\n\n"
            "➡️ Choose a border crossing point:"
        ),
        "column_explanation": ("<b>ℹ️ Explanation of columns:</b>\n"
            "• <b>Plate</b> — license plate of the car.\n"
            "• <b>Registered</b> — when the car <u>entered</u> the buffer zone.\n"
            "• <b>Last Change</b> — when the car <u>exited</u> the buffer zone.\n"
            "• <b>Time in Queue</b> — how long the car waited inside the buffer zone.\n"
            "• <b>Cars in Queue</b> — how many cars were ahead of this car when it entered the buffer zone.\n"
            "• <b>Queue Speed</b> — average speed of passing for this car (cars/hour).\n\n"
            "👉 <i>Tip:</i> Look at the <b>queue speed</b> of the last few cars that already left "
            "the buffer zone. You can use this value to estimate your own waiting time.\n"
            "For example, if your number in the queue is <b>N</b> and the speed is <b>S cars/hour</b>, "
            "then estimated waiting time ≈ N ÷ S hours."
        ),
        "choose_border_point": "Choose a border crossing point:",
        "border_points_id": {
            "benyakoni": 1,
            "brest_bts": 2,
            "kamenny_log": 3,
            "grigorovschina": 4,
        },
        "border_points_names": {
            "benyakoni": "Benyakoni",
            "brest_bts": "Brest BTS (\"Varshavskiy Most\")",
            "kamenny_log": "Kamenny Log",
            "grigorovschina": "Grigorovschina",
        }
    },
    "ru": {
        "welcome": (
            "<b>Оценка скорости прохождения границы</b> 🚦\n\n"
            "Здесь вы можете увидеть последние расчёты скорости очереди по данным из буферных зон.\n"
            "Это поможет вам понять, насколько быстро движется очередь и сколько времени займёт ожидание.\n\n"
            "➡️ Выберите пункт пропуска:"
        ),
        "column_explanation": ("<b>ℹ️ Объяснение колонок:</b>\n"
            "• <b>Номер</b> — госномер автомобиля.\n"
            "• <b>Зарегистрирован</b> — время <u>въезда</u> в буферную зону.\n"
            "• <b>Последнее изменение</b> — время, когда автомобиль <u>выехал</u> из буферной зоны.\n"
            "• <b>Время в очереди</b> — сколько автомобиль ждал в буферной зоне.\n"
            "• <b>Машин в очереди</b> — сколько автомобилей было впереди при въезде в буферную зону.\n"
            "• <b>Скорость очереди</b> — средняя скорость прохождения для данного автомобиля (машин/час).\n\n"
            "👉 <i>Совет:</i> Обратите внимание на <b>скорость очереди</b> последних машин, "
            "которые уже выехали из буферной зоны. По этому значению можно примерно оценить своё ожидание.\n"
            "Например, если ваш номер в очереди <b>N</b>, а скорость <b>S машин/час</b>, "
            "то примерное время ожидания ≈ N ÷ S часов."),
        "choose_border_point": "Выберите пограничный пункт:",
        "border_points_id": {
            "benyakoni": 1,
            "brest_bts": 2,
            "kamenny_log": 3,
            "grigorovschina": 4,
        },
        "border_points_names": {
            "benyakoni": "Бенякони",
            "brest_bts": "Брест БТС (\"Варшавский мост\")",
            "kamenny_log": "Каменный Лог",
            "grigorovschina": "Григоровщина",
        }
    }   
}

# Button labels
BUTTONS = {
    "en": {
        "stats":"Show border statistics",
        "estimations": "Estimate border speed",
        "country_lt": "Lithuania 🇱🇹",
        "country_lv": "Latvia 🇱🇻",
        "country_pl": "Poland 🇵🇱",
        "3h": "last 3 hours",
        "24h": "last 24 hours",
        "7d": "last 7 days",
        "30d": "last 30 days",
        "menu": "Main Menu",
        "benyakoni": "Benyakoni  🇱🇹",
        "kamenny_log": "Kamenny Log  🇱🇹",
        "brest_bts": "Brest BTS (\"Varshavskiy Most\") 🇵🇱",
        "grigorovschina": "Grigorovschina 🇱🇻",
        "archive": "Archive",
        "2024": "2024 year",
        "2025": "2025 year",
        "january": "January",
        "february": "February",
        "march": "March",
        "april": "April",
        "may": "May",
        "june": "June",
        "july": "July",
        "august": "August",
        "september": "September",
        "october": "October",
        "november": "November",
        "december": "December"
    },
    "ru": {
        "stats":"Показать статистику по границе",
        "estimations": "Оценить скорость прохождения границы",
        "country_lt": "Литва 🇱🇹",
        "country_lv": "Латвия 🇱🇻",
        "country_pl": "Польша 🇵🇱",
        "3h": "за 3 часа",
        "24h": "за 24 часа",
        "7d": "за 7 дней",
        "30d": "за 30 дней",
        "menu": "Главное меню",
        "benyakoni": "Бенякони  🇱🇹",
        "kamenny_log": "Каменный Лог  🇱🇹",
        "brest_bts": "Брест БТС (\"Варшавский мост\")  🇵🇱",
        "grigorovschina": "Григоровщина  🇱🇻",
        "archive": "Архив данных",
        "2024": "2024 год",
        "2025": "2025 год",
        "january": "Январь",
        "february": "Февраль",
        "march": "Март",
        "april": "Апрель",
        "may": "Май",
        "june": "Июнь",
        "july": "Июль",
        "august": "Август",
        "september": "Сентябрь",
        "october": "Октябрь",
        "november": "Ноябрь",
        "december": "Декабрь"
    },
}