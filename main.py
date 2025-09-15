import os
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    CallbackQueryHandler, 
    MessageHandler, 
    filters
)
from handlers import start, restart, menu, button_handler, handle_plate
from user_utils import get_all_active_user_car_notifications_from_db, get_user_lang, get_user_car_types_from_db
from tracking_car import track_user_car
from multiprocessing import Process

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")

def main():
    # Activate all enabled car notifications on startup
    notifications = get_all_active_user_car_notifications_from_db()
    for notification in notifications:
        user_lang = get_user_lang(notification.telegram_id)
        car_type = get_user_car_types_from_db(notification.telegram_id, notification.car_plate)
        p = Process(target=track_user_car, args=(notification.surr_id, car_type, user_lang))
        p.start()

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("restart", restart))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_plate))
    app.run_polling()

if __name__ == "__main__":
    main()
