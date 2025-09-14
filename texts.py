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

CURRENT = {
    "en": {
        "current_info": (
            "Here you can find the current queue information for border crossing points "
            "from <b>Belarus ➝ EU</b>.\n\n"
            "The information is sourced from "
            "<a href='https://declarant.by'>declarant.by</a> "
            "and reflects the number of vehicles in <b>buffer zones</b>.\n\n"
            "➡️ <i>Choose a border crossing point:</i>"
        ),
        "choose_border_point": "Choose a border crossing point:",
    },
    "ru": {
        "current_info": (
            "Здесь вы можете найти актуальную информацию об очередях "
            "на пограничных пунктах пропуска из <b>Беларуси ➝ ЕС</b>.\n\n"
            "Информация берётся с сайта "
            "<a href='https://declarant.by'>declarant.by</a> "
            "и отражает количество автомобилей в <b>буферных зонах</b>.\n\n"
            "➡️ <i>Выберите пограничный пункт:</i>"
        ),
        "choose_border_point": "Выберите пограничный пункт:",

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
            "kozlovichi": "Kozlovichi",
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
            "kozlovichi": "Козловичи",
        }
    }   
}

CARTRACKING = {
    "en": {
        "car_tracking_intro": (
            "<b>Your Saved Cars</b>\n\n"
            "Here you can find the cars you've saved for tracking.\n"
            "Select a car to view its tracking information."
        ),
        "add_car_prompt": (
            "<b>Add a Car</b>\n\n"
            "To add a car for tracking, please send the license plate number in format with letters and numbers only.\n"
            "Make sure to use uppercase letters and no spaces or special characters."
        ),
        "car_added": (
            "<b>✅ Car Added</b>\n\n"
            "The car with license plate <code>{}</code> has been added for tracking."
        ),
        "car_removed": (
            "<b>✅ Car Removed</b>\n\n"
            "The car with license plate <code>{}</code> has been removed from tracking."
        ),
        "car_added_error": (
            "❌ Invalid plate format.\n\n"
            "Use up to 7 characters, only uppercase letters and numbers, "
            "with at least one digit (e.g. <b>ABC123</b>)."
        ),
        "car_found_in_queue": (
            "<b>Car Found in Queue!</b>\n\n"
            "The car with license plate <b>{}</b> is currently in the queue.\n"
        ),
        "car_not_found_in_queue": (
            "<b>Car Not Found in Queue</b>\n\n"
            "The car with license plate <b>{}</b> is not currently in any queue."
        ),
        "car_status_details": (
            "<b>Car Status Details</b>\n"
            "• Checkpoint: <b>{}</b>\n"
            "• License Plate: <b>{}</b>\n"
            "• Position in Queue: <b>{}</b>\n"
            "• Registered: <b>{}</b>\n"
        ),
        "car_notification_settings": (
            "<b>Notification settings for car <code>{}</code></b>"
        ),
        "notification_status_enabled": "Notification has been enabled.",
        "notification_status_disabled": "Notification has been disabled.",
        "notification_activation_failed": "Failed to activate notification. Most probably the car is not in the queue.",
        "notification_removed":"Notification has been removed",
        "add_notification_type": (
            "<b>Select notification type for car <code>{}</code></b>\n\n"
            "Choose the type of notification you want to set for this car:\n"
            "• Position in queue (e.g., notify when position = 'N')\n"
            "• Time interval (e.g., notify every 'N' minutes)\n"
            "• Number of cars passed (e.g., notify every 'N' cars)\n"
            "• Summoned to checkpoint (notify when the car is summoned to the border checkpoint)\n"
        ),
        "set_notification_value_number_in_queue": "Select value for notification type <b>Position in queue</b>",
        "set_notification_value_every_n_minutes": "Select value for notification type <b>Time interval</b>",
        "set_notification_value_every_n_cars": "Select value for notification type <b>Number of cars passed</b>",
        "notification_added": (
            "<b>✅ Notification Added</b>\n\n"
            "A new notification has been added for car <b>{}</b>.\n"
            "Check the icons 🔔 & 🔕 next to each notification.\nTap them to enable or disable the notification."
        ),
        "no_notification_found": "No notification found with surr_id {}.",
        "car_current_position": "<b>{}</b> is at position <b>{}</b> in the queue (<b>{}</b>).",
        "car_reached_position": (
            "<b>{}</b> has reached position <b>{}</b> in the queue (<b>{}</b>).\n"
            "🔕 <b>Notification has been disabled.</b>"
        ),
        "car_summoned": (
            "<b>{}</b> has been summoned to the border checkpoint.\n"
            "🔕 <b>Notification has been disabled.</b>"
        ),
        "car_summoned_short": (
            "<b>{}</b> has been summoned to the border checkpoint."
        ),
        "car_no_longer_in_queue": (
            "<b>{}</b> is no longer in any queue.\n"
            "🔕 <b>Notification has been disabled.</b>"
        ),
        "car_moved_forward": (
            "<b>{}</b> is at position <b>{}</b> in the queue (<b>{}</b>).\n"
            "Current position is less than the one selected in the notification.\n"
            "🔕 <b>Notification has been disabled.</b>"
        )
    },
    "ru": {
        "car_tracking_intro": (
            "<b>Ваши сохраненные машины</b>\n\n"
            "Здесь вы можете найти машины, которые вы сохранили для отслеживания.\n"
            "Выберите машину, чтобы просмотреть информацию об отслеживании."
        ),
        "add_car_prompt": (
            "<b>Добавить машину</b>\n\n"
            "Чтобы добавить машину для отслеживания, пожалуйста, отправьте номерной знак в формате с буквами и цифрами только.\n"
            "Убедитесь, что используете заглавные буквы без пробелов и специальных символов."
        ),
        "car_added": (
            "<b>✅ Машина добавлена</b>\n\n"
            "Машина с номером <code>{}</code> была добавлена для отслеживания."
        ),
        "car_removed": (
            "<b>✅ Машина удалена</b>\n\n"
            "Машина с номером <code>{}</code> была удалена из отслеживания."
        ),
        "car_added_error": (
            "❌ Неверный формат номера.\n\n"
            "Используйте до 7 символов, только заглавные буквы и цифры, "
            "с как минимум одной цифрой (например, <b>ABC123</b>)."
        ),
        "car_found_in_queue": (
            "<b>Машина найдена в очереди!</b>\n\n"
            "Машина с номером <b>{}</b> в данный момент находится в очереди.\n"
        ),
        "car_not_found_in_queue": (
            "<b>Машина не найдена в очереди</b>\n\n"
            "Машина с номером <b>{}</b> в данный момент не находится в какой-либо очереди."
        ),
        "car_status_details": (
            "<b>Статус машины</b>\n"
            "• Пункт пропуска: <b>{}</b>\n"
            "• Номерной знак: <b>{}</b>\n"
            "• Позиция в очереди: <b>{}</b>\n"
            "• Зарегистрирован: <b>{}</b>\n"
        ),
        "car_notification_settings": (
            "<b>Настройки уведомлений для машины <code>{}</code></b>"
        ),
        "notification_status_enabled": "Уведомление было включено.",
        "notification_status_disabled": "Уведомление было отключено.",
        "notification_activation_failed": "Не удалось активировать уведомление. Скорее всего, машина не в очереди.",
        "notification_removed": "Уведомление было удалено",
        "add_notification_type": (
            "<b>Выберите тип уведомления для машины <code>{}</code></b>:\n\n"
            "• <b>Позиция в очереди</b> (уведомлять, когда позиция = 'N')\n"
            "• <b>Интервал времени</b> (уведомлять каждые 'N' минут)\n"
            "• <b>Интервал машин</b> (уведомлять каждые 'N' машин)\n"
            "• <b>Вызов на контроль</b> (уведомлять, когда машина вызвана на пограничный контроль)\n"
        ),
        "set_notification_value_number_in_queue": "Выберите значение для типа уведомления <b>Позиция в очереди</b>",
        "set_notification_value_every_n_minutes": "Выберите значение для типа уведомления <b>Интервал времени</b>",
        "set_notification_value_every_n_cars": "Выберите значение для типа уведомления <b>Интервал машин</b>",
        "notification_added": (
            "<b>✅ Уведомление добавлено</b>\n\n"
            "Новое уведомление было добавлено для машины <b>{}</b>.\n"
            "Нажмите на иконку 🔔 или 🔕, чтобы включить или отключить уведомление."
        ),
        "no_notification_found": "Уведомление не найдено с surr_id {}.",
        "car_current_position": "<b>{}</b> находится на позиции <b>{}</b> в очереди (<b>{}</b>).",
        "car_reached_position": (
            "<b>{}</b> находится на позиции <b>{}</b> в очереди (<b>{}</b>).\n"
            "🔕 <b>Уведомление было отключено.</b>"
        ),
        "car_summoned": (
            "<b>{}</b> вызвана на пограничный контроль.\n"
            "🔕 <b>Уведомление было отключено.</b>"
        ),
        "car_summoned_short": (
            "<b>{}</b> вызвана на пограничный контроль."
        ),
        "car_no_longer_in_queue": (
            "<b>{}</b> больше не находится в очереди.\n"
            "🔕 <b>Уведомление было отключено.</b>"
        ),
        "car_moved_forward": (
            "<b>{}</b> находится на позиции <b>{}</b> в очереди (<b>{}</b>).\n"
            "Текущая позиция меньше выбранной в уведомлении.\n"
            "🔕 <b>Уведомление было отключено.</b>"
        )
    }
}

# Button labels
BUTTONS = {
    "en": {
        "current": "Current queue info",
        "stats":"Historical queue data",
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
        "kozlovichi": "Kozlovichi 🇵🇱",
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
        "december": "December",
        "car_tracking": "Track your saved cars",
        "car_tracking_back": "🔙 Track your saved cars",
        "add_car": "Add a car",
        "remove_car": "Remove",
        "settings_car": "Settings",
        "add_notification": "Add notification",
        "remove_notification": "Remove",
        "disable_notification": "Disable",
        "enable_notification": "Enable",
        "notification_type_number_in_queue": "position {}",
        "notification_type_every_n_minutes": "every {} min",
        "notification_type_every_n_cars": "every {} cars",
        "notification_type_summoned": "summoned",
        "set_notification_type_number_in_queue": "Position in queue",
        "set_notification_type_every_n_minutes": "Every 'N' minutes",
        "set_notification_type_every_n_cars": "Every 'N' cars",
        "set_notification_type_summoned": "Summoned to checkpoint",
        "selected_car_settings": "🔙 Selected car settings"
    },
    "ru": {
        "current": "Актуальная информация об очередях",
        "stats":"Исторические данные по очередям",
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
        "kozlovichi": "Козловичи  🇵🇱",
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
        "december": "Декабрь",
        "car_tracking": "Отслеживание сохраненных машин",
        "car_tracking_back": "🔙 Отслеживание сохраненных машин",
        "add_car": "Добавить машину",
        "remove_car": "Удалить",
        "settings_car": "Настройки",
        "add_notification": "Добавить уведомление",
        "remove_notification": "Удалить",
        "disable_notification": "Отключить",
        "enable_notification": "Включить",
        "notification_type_number_in_queue": "позиция {}",
        "notification_type_every_n_minutes": "каждые {} мин",
        "notification_type_every_n_cars": "каждые {} маш",
        "notification_type_summoned": "вызов на ПП",
        "set_notification_type_number_in_queue": "Позиция в очереди",
        "set_notification_type_every_n_minutes": "Интервал времени",
        "set_notification_type_every_n_cars": "Интервал машин",
        "set_notification_type_summoned": "Вызов на контроль",
        "selected_car_settings": "🔙 Настройки выбранной машины"
    }
}