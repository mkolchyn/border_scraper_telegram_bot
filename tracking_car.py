import requests
import time
from user_utils import (
    get_user_cars_current_status,
    deactivate_user_car_notification_in_db
)
import os
from dotenv import load_dotenv
from db_functions import SessionLocal
from models import UserNotification
from texts import CARTRACKING

load_dotenv()

TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")

def send_telegram_message(message, chat_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=10)
    except requests.RequestException as e:
        print(f"Failed to send message to {chat_id}: {e}")


def track_user_car(surr_id: int, lang: str):
    """Helper function to track a car and send notification to user."""

    session = SessionLocal()
    try:
        notification = session.query(UserNotification).filter(UserNotification.surr_id == surr_id).first()
        if not notification:
            message = CARTRACKING[lang]["no_notification_found"].format(surr_id)
            send_telegram_message(message, user_id)
            return

        user_id = notification.telegram_id
        car = notification.car_plate
        notification_type = notification.notification_type
        notification_value = notification.notification_value

        current_status = get_user_cars_current_status(car)
        init_current_status = current_status[2]

        if notification_type == "number-in-queue":
            while True:
                notification_status = session.query(UserNotification).filter(
                    UserNotification.surr_id == surr_id,
                    UserNotification.notification_status == True
                ).first()
                if not notification_status:
                    message = f"[DEBUG] Notification {surr_id} for user {user_id} and car {car} is deactivated."
                    send_telegram_message(message, user_id)
                    break

                current_status = get_user_cars_current_status(car)

                if current_status and current_status[2] == notification_value:
                    message = CARTRACKING[lang]["car_reached_position"].format(car, notification_value, current_status[0].capitalize())
                    send_telegram_message(message, user_id)
                    deactivate_user_car_notification_in_db(surr_id)
                    break
                elif current_status and current_status[4] == 3:
                    message = CARTRACKING[lang]["car_summoned"].format(car)
                    send_telegram_message(message, user_id)
                    deactivate_user_car_notification_in_db(surr_id)
                    break
                elif not current_status:
                    message = CARTRACKING[lang]["car_no_longer_in_queue"].format(car)
                    send_telegram_message(message, user_id)
                    deactivate_user_car_notification_in_db(surr_id)
                    break

                time.sleep(60)

        elif notification_type == "every-n-minutes":
            while True:
                notification_status = session.query(UserNotification).filter(
                    UserNotification.surr_id == surr_id,
                    UserNotification.notification_status == True
                ).first()
                if not notification_status:
                    message = f"[DEBUG] Notification {surr_id} for user {user_id} and car {car} has been deactivated."
                    send_telegram_message(message, user_id)
                    break

                current_status = get_user_cars_current_status(car)

                if current_status and current_status[4] == 2:
                    message = CARTRACKING[lang]["car_found_in_queue"].format(car) + "\n" + \
                        CARTRACKING[lang]["car_status_details"].format(current_status[0].capitalize(), current_status[1], current_status[2], current_status[3])
                    send_telegram_message(message, user_id)
                elif current_status and current_status[4] == 3:
                    message = CARTRACKING[lang]["car_summoned"].format(car)
                    send_telegram_message(message, user_id)
                    deactivate_user_car_notification_in_db(surr_id)
                elif not current_status:
                    message = CARTRACKING[lang]["car_no_longer_in_queue"].format(car)
                    send_telegram_message(message, user_id)
                    deactivate_user_car_notification_in_db(surr_id)
                    break

                time.sleep(notification_value * 60)

        elif notification_type == "every-n-cars":
            while True:
                notification_status = session.query(UserNotification).filter(
                    UserNotification.surr_id == surr_id,
                    UserNotification.notification_status == True
                ).first()
                if not notification_status:
                    message = f"[DEBUG] Notification {surr_id} for user {user_id} and car {car} has been deactivated."
                    send_telegram_message(message, user_id)
                    break

                current_status = get_user_cars_current_status(car)

                if current_status[4] == 2 and current_status[2] < notification_value:
                    message = CARTRACKING[lang]["car_moved_forward"].format(car, notification_value, current_status[2], current_status[0])
                    send_telegram_message(message, user_id)
                    deactivate_user_car_notification_in_db(surr_id)
                    break

                elif current_status[4] == 2 and current_status[2] <= init_current_status - notification_value:
                    message = CARTRACKING[lang]["car_found_in_queue"].format(car) + "\n" + \
                        CARTRACKING[lang]["car_status_details"].format(current_status[0].capitalize(), current_status[1], current_status[2], current_status[3])
                    send_telegram_message(message, user_id)
                    init_current_status = current_status[2]
                    
                elif current_status and current_status[4] == 3:
                    message = CARTRACKING[lang]["car_summoned"].format(car)
                    send_telegram_message(message, user_id)
                    deactivate_user_car_notification_in_db(surr_id)
                    break
                elif not current_status:
                    message = CARTRACKING[lang]["car_no_longer_in_queue"].format(car)
                    send_telegram_message(message, user_id)
                    deactivate_user_car_notification_in_db(surr_id)
                    break
                
                time.sleep(60)
        else:
            print(f"[WARN] Unknown notification type {notification_type} for user {user_id}, car {car}.")

    finally:
        session.close()