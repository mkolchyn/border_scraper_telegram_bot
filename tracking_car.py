import requests
import time
from typing import Optional
from user_utils import get_user_cars_current_status, deactivate_user_car_notification_in_db
import os
from dotenv import load_dotenv
from db_functions import get_local_session
from models import UserNotification
from texts import CARTRACKING

load_dotenv()
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")


def send_telegram_message(message: str, chat_id: int) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=10)
    except requests.RequestException as e:
        print(f"[WARN] Failed to send message to {chat_id}: {e}")


def sleep_with_stop(total_seconds: float, stop_event=None, check_every: float = 1.0) -> bool:
    """
    Sleep but wake early if stop_event.is_set(). Returns True if full sleep elapsed,
    False if interrupted by stop_event.
    """
    end = time.monotonic() + total_seconds
    while True:
        if stop_event is not None and getattr(stop_event, "is_set", lambda: False)():
            return False
        now = time.monotonic()
        remaining = end - now
        if remaining <= 0:
            return True
        time.sleep(min(check_every, remaining))


def fetch_notification(surr_id: int) -> Optional[UserNotification]:
    """
    Get the notification row using a session created in THIS process.
    Returns ORM object (detached) or None.
    """
    try:
        with get_local_session() as session:
            return session.query(UserNotification).filter(UserNotification.surr_id == surr_id).first()
    except Exception:
        # Let caller handle/log
        raise


def check_notification_active(surr_id: int) -> bool:
    """
    Check if a notification row exists and notification_status is True,
    using a fresh session for this single read.
    """
    try:
        with get_local_session() as session:
            row = session.query(UserNotification.notification_status).filter(
                UserNotification.surr_id == surr_id
            ).first()
            if not row:
                return False
            # row is a one-column Row; row[0] is the boolean field value
            return bool(row[0])
    except Exception as e:
        print(f"[ERROR] DB error while checking active status for {surr_id}: {e}")
        # Defensive choice: stop the worker if DB is flaky. Returning False will end loop.
        return False


def track_user_car(surr_id: int, car_type: str, lang: str, stop_event=None) -> None:
    """
    Refactored tracker:
      - Uses short-lived DB sessions (get_local_session) for each DB access
        (prevents sharing connections across processes).
      - Uses an optional stop_event (multiprocessing.Event) to allow graceful shutdown.
    """
    try:
        notification = fetch_notification(surr_id)
    except Exception as e:
        print(f"[ERROR] Couldn't load notification {surr_id}: {e}")
        return

    if not notification:
        print(f"[WARN] Notification {surr_id} not found; nothing to track.")
        return

    car_type_icon = "🚗" if car_type == "passenger" else "🚚"
    user_id = notification.telegram_id
    car = notification.car_plate
    notification_type = notification.notification_type
    notification_value = notification.notification_value

    def stop_requested() -> bool:
        return stop_event is not None and getattr(stop_event, "is_set", lambda: False)()

    # ---------- "number-in-queue" ----------
    if notification_type == "number-in-queue":
        poll_interval = 60
        while True:
            if stop_requested():
                print(f"[INFO] stop requested; exiting tracker {surr_id}.")
                break

            if not check_notification_active(surr_id):
                print(f"[DEBUG] Notification {surr_id} for {user_id}/{car} is deactivated.")
                break

            current_status = get_user_cars_current_status(car, car_type)
            if current_status is None:
                send_telegram_message(car_type_icon + CARTRACKING[lang]["car_no_longer_in_queue"].format(car), user_id)
                try:
                    deactivate_user_car_notification_in_db(surr_id)
                except Exception as e:
                    print(f"[WARN] Failed to deactivate {surr_id}: {e}")
                break

            position = current_status[2]
            status_code = current_status[4]

            if position == notification_value:
                send_telegram_message(
                    car_type_icon + CARTRACKING[lang]["car_reached_position"].format(car, notification_value, current_status[0].capitalize()),
                    user_id
                )
                try:
                    deactivate_user_car_notification_in_db(surr_id)
                except Exception as e:
                    print(f"[WARN] Failed to deactivate {surr_id}: {e}")
                break

            if status_code == 3:  # summoned
                send_telegram_message(car_type_icon + CARTRACKING[lang]["car_summoned"].format(car), user_id)
                try:
                    deactivate_user_car_notification_in_db(surr_id)
                except Exception as e:
                    print(f"[WARN] Failed to deactivate {surr_id}: {e}")
                break

            if not sleep_with_stop(poll_interval, stop_event):
                break

    # ---------- "every-n-minutes" ----------
    elif notification_type == "every-n-minutes":
        # require at least 60s polling to avoid extremely small values
        poll_interval = max(notification_value * 60, 60)
        while True:
            if stop_requested():
                print(f"[INFO] stop requested; exiting tracker {surr_id}.")
                break

            if not check_notification_active(surr_id):
                print(f"[DEBUG] Notification {surr_id} for {user_id}/{car} has been deactivated.")
                break

            current_status = get_user_cars_current_status(car, car_type)
            if current_status is None:
                send_telegram_message(car_type_icon + CARTRACKING[lang]["car_no_longer_in_queue"].format(car), user_id)
                try:
                    deactivate_user_car_notification_in_db(surr_id)
                except Exception as e:
                    print(f"[WARN] Failed to deactivate {surr_id}: {e}")
                break

            status_code = current_status[4]
            if status_code == 2:
                send_telegram_message(
                    car_type_icon + CARTRACKING[lang]["car_current_position"].format(
                        current_status[1], current_status[2], current_status[0].capitalize()
                    ),
                    user_id
                )
            elif status_code == 3:
                send_telegram_message(car_type_icon + CARTRACKING[lang]["car_summoned"].format(car), user_id)
                try:
                    deactivate_user_car_notification_in_db(surr_id)
                except Exception as e:
                    print(f"[WARN] Failed to deactivate {surr_id}: {e}")
                break

            if not sleep_with_stop(poll_interval, stop_event):
                break

    # ---------- "every-n-cars" ----------
    elif notification_type == "every-n-cars":
        poll_interval = 60
        # snapshot of initial queue position
        current_status = get_user_cars_current_status(car, car_type)
        last_snapshot = current_status[2] if current_status else None

        while True:
            if stop_requested():
                print(f"[INFO] stop requested; exiting tracker {surr_id}.")
                break

            if not check_notification_active(surr_id):
                print(f"[DEBUG] Notification {surr_id} for {user_id}/{car} has been deactivated.")
                break

            current_status = get_user_cars_current_status(car, car_type)
            if current_status is None:
                send_telegram_message(car_type_icon + CARTRACKING[lang]["car_no_longer_in_queue"].format(car), user_id)
                try:
                    deactivate_user_car_notification_in_db(surr_id)
                except Exception as e:
                    print(f"[WARN] Failed to deactivate {surr_id}: {e}")
                break

            position = current_status[2]
            status_code = current_status[4]

            # moved forward by N cars since last snapshot
            if status_code == 2 and last_snapshot is not None and position <= last_snapshot - notification_value:
                send_telegram_message(
                    car_type_icon + CARTRACKING[lang]["car_current_position"].format(
                        current_status[1], current_status[2], current_status[0].capitalize()
                    ),
                    user_id
                )
                last_snapshot = position

            # reached absolute threshold
            if status_code == 2 and position < notification_value:
                send_telegram_message(car_type_icon + CARTRACKING[lang]["car_moved_forward"].format(car, position, current_status[0].capitalize()), user_id)
                try:
                    deactivate_user_car_notification_in_db(surr_id)
                except Exception as e:
                    print(f"[WARN] Failed to deactivate {surr_id}: {e}")
                break

            if status_code == 3:
                send_telegram_message(car_type_icon + CARTRACKING[lang]["car_summoned"].format(car), user_id)
                try:
                    deactivate_user_car_notification_in_db(surr_id)
                except Exception as e:
                    print(f"[WARN] Failed to deactivate {surr_id}: {e}")
                break

            if not sleep_with_stop(poll_interval, stop_event):
                break
        
    # ---------- "summoned" ----------
    elif notification_type == "summoned":
        poll_interval = 60
        while True:
            if stop_requested():
                print(f"[INFO] stop requested; exiting tracker {surr_id}.")
                break

            if not check_notification_active(surr_id):
                print(f"[DEBUG] Notification {surr_id} for {user_id}/{car} is deactivated.")
                break

            current_status = get_user_cars_current_status(car, car_type)
            if current_status is None:
                send_telegram_message(car_type_icon + CARTRACKING[lang]["car_no_longer_in_queue"].format(car), user_id)
                try:
                    deactivate_user_car_notification_in_db(surr_id)
                except Exception as e:
                    print(f"[WARN] Failed to deactivate {surr_id}: {e}")
                break

            status_code = current_status[4]

            if status_code == 3:  # summoned
                send_telegram_message(car_type_icon + CARTRACKING[lang]["car_summoned"].format(car), user_id)
                try:
                    deactivate_user_car_notification_in_db(surr_id)
                except Exception as e:
                    print(f"[WARN] Failed to deactivate {surr_id}: {e}")
                break

            if not sleep_with_stop(poll_interval, stop_event):
                break
    
    else:
        print(f"[WARN] Unknown notification type '{notification_type}' for surr_id={surr_id}.")

    print(f"[INFO] track_user_car {surr_id} finished.")
