from telegram import User, InputMediaPhoto, InlineKeyboardMarkup
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from db_functions import get_local_session
from models import DBUser, UserAction, UserNotification, UserCars
from datetime import datetime, timezone
import time
import httpx
from io import BytesIO
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERVER_ADDRESS = os.getenv("SERVER_ADDRESS")

# Send or edit photo
async def send_or_edit_photo(query, path_prefix, file_suffix, caption, keyboard, use_bytes=False, archive=False):
    if archive:
        url = f"http://{SERVER_ADDRESS}/archive/{path_prefix}/{file_suffix}"
    else:
        url = f"http://{SERVER_ADDRESS}/{path_prefix}/{file_suffix}"

    if use_bytes:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            resp.raise_for_status()
            media = InputMediaPhoto(media=BytesIO(resp.content), caption=caption)
    else:
        url_with_ts = f"{url}?{int(time.time())}"
        media = InputMediaPhoto(media=url_with_ts, caption=caption)

    await query.edit_message_media(
        media=media,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def log_user_action(user: User, action: str):
    """Log a user action into Postgres."""
    session: Session = get_local_session()
    try:
        # Get current version of user
        db_user = session.query(DBUser)\
            .filter_by(telegram_id=user.id, is_current=True)\
            .order_by(DBUser.surr_id.desc()).first()

        if not db_user:
            # First-time user: insert new record
            db_user = DBUser(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
            )
            session.add(db_user)
            session.flush()  # ensures surr_id is available

        # Log action
        user_action = UserAction(
            telegram_id=db_user.telegram_id,
            action=action
        )
        session.add(user_action)
        session.commit()

    except IntegrityError as e:
        session.rollback()
        print(f"[ERROR] Failed to log action: {e}")
    finally:
        session.close()


def get_user_lang(user_id: int) -> str:
    """Return the latest language for the user, default 'en'."""
    session: Session = get_local_session()
    try:
        db_user = session.query(DBUser)\
            .filter_by(telegram_id=user_id, is_current=True)\
            .order_by(DBUser.surr_id.desc()).first()
        return db_user.lang if db_user and db_user.lang else "en"
    finally:
        session.close()


def set_user_lang(user: User, lang: str):
    """Set or update language preference for user using SCD2."""
    session: Session = get_local_session()
    try:
        db_user = session.query(DBUser)\
            .filter_by(telegram_id=user.id, is_current=True)\
            .order_by(DBUser.surr_id.desc()).first()

        if db_user:
            # If lang changed, close old record and insert new one
            if db_user.lang != lang:
                db_user.valid_to = datetime.now(timezone.utc)
                db_user.is_current = False

                new_user = DBUser(
                    telegram_id=user.id,
                    username=db_user.username,
                    first_name=db_user.first_name,
                    last_name=db_user.last_name,
                    joined_at=db_user.joined_at,
                    lang=lang
                )
                session.add(new_user)
        else:
            # First-time user
            new_user = DBUser(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                lang=lang
            )
            session.add(new_user)

        session.commit()
    finally:
        session.close()


def fetch_data_from_api(url):
    """Fetch JSON data from the provided API."""
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")

def get_queue_length_current(checkpoint_id: str):
    try:
        url = "https://belarusborder.by/info/checkpoint?token=bts47d5f-6420-4f74-8f78-42e8e4370cc4"

        data = fetch_data_from_api(url)

        # Loop through all data and insert based on the mapped zone
        for cp in data['result']:
            if cp['id'] == checkpoint_id:
                countCar = cp['countCar']
                countTruck = cp['countTruck']
                countBus = cp['countBus']
                countMotorcycle = cp['countMotorcycle']
        
        return countCar, countTruck, countBus, countMotorcycle
        
    except Exception as e:
        print(f"Error: {e}")

def get_user_cars_current_status(car: str, car_type: str):
    """Check if 'car' is currently in any queue zones."""
    buffer_zones = {
        "benyakoni": "53d94097-2b34-11ec-8467-ac1f6bf889c0",
        "brest_bts": "a9173a85-3fc0-424c-84f0-defa632481e4",
        "kamenny_log": "b60677d4-8a00-4f93-a781-e129e1692a03",
        "grigorovschina": "ffe81c11-00d6-11e8-a967-b0dd44bde851",
        "kozlovichi": "98b5be92-d3a5-4ba2-9106-76eb4eb3df49"
    }

    for buffer_zone_name, checkpointID in buffer_zones.items():
        url = f"https://belarusborder.by/info/monitoring-new?token=test&checkpointId={checkpointID}"
        data = fetch_data_from_api(url)

        if not data:
            continue
        if car_type == "passenger":
            car_live_queue = data.get("carLiveQueue", [])
            for car_entry in car_live_queue:
                if car_entry.get("regnum", "").upper() == car.upper():  # case-insensitive check
                    return (
                        buffer_zone_name,
                        car_entry["regnum"],
                        car_entry["order_id"],
                        car_entry["registration_date"],
                        car_entry["status"]
                    )
        elif car_type == "freight":
            truck_live_queue = data.get("truckLiveQueue", [])
            for truck_entry in truck_live_queue:
                if truck_entry.get("regnum", "").upper() == car.upper():  # case-insensitive check
                    return (
                        buffer_zone_name,
                        truck_entry["regnum"],
                        truck_entry["order_id"],
                        truck_entry["registration_date"],
                        truck_entry["status"]
                    )

    return None

def set_user_car_into_db(user_id: int, car: str, car_type: str):
    """Save a car into user cars table."""
    session = get_local_session()
    try:
        new_car = UserCars(
            telegram_id=user_id,
            plate=car,
            car_type=car_type
        )
        session.add(new_car)
        session.commit()

    except Exception as e:
        session.rollback()
        print(f"Error saving car: {e}")
    finally:
        session.close()

def get_user_cars_from_db(user_id: int, car_type: str):
    """Fetch all cars for a user using ORM (may include None)."""
    session: Session = get_local_session()
    try:
        db_cars = (
            session.query(UserCars)
            .filter(UserCars.telegram_id == user_id, UserCars.car_type == car_type)
            .order_by(UserCars.surr_id.desc())
            .all()
        )
        if db_cars:
            return [car.plate for car in db_cars]
        return []
    finally:
        session.close()

def remove_user_car_from_db(user_id: int, car: str):
    """Remove a specific car from user cars table."""
    session = get_local_session()
    try:
        db_car = session.query(UserCars)\
            .filter_by(telegram_id=user_id, plate=car).first()
        if db_car:
            session.delete(db_car)
            session.commit()

    except Exception as e:
        session.rollback()
        print(f"Error removing car: {e}")
    finally:
        session.close()

def set_user_car_notification_in_db(user_id: int, car: str, notification_type: str, notification_value: int):
    """Set a notification for a user's car."""
    session = get_local_session()
    try:
        new_notification = UserNotification(
            telegram_id=user_id,
            car_plate=car,
            notification_type=notification_type,
            notification_value=notification_value
        )
        session.add(new_notification)
        session.commit()

    except Exception as e:
        session.rollback()
        print(f"Error saving notification: {e}")
    finally:
        session.close()

def get_user_car_notifications_from_db(user_id: int, car: str, notification_type: str, notification_value: int):
    """Fetch notifications for a user's specific car, optionally filtered by type and value."""
    session = get_local_session()
    try:
        if notification_type and notification_value is not None:
            notifications = session.query(UserNotification)\
                .filter_by(telegram_id=user_id, car_plate=car, notification_type=notification_type, notification_value=notification_value).all()
            return notifications
        else:
            notifications = session.query(UserNotification)\
                .filter_by(telegram_id=user_id, car_plate=car).all()
            return notifications
    finally:
        session.close()

def get_all_active_user_car_notifications_from_db():
    """Fetch all active notifications for all users."""
    session = get_local_session()
    try:
        notifications = session.query(UserNotification)\
            .filter_by(notification_status=True).all()
        return notifications
    finally:
        session.close()

def remove_all_user_car_notifications_from_db(user_id: int, car: str):
    """Remove all notifications for a user's specific car."""
    session = get_local_session()
    try:
        notifications = session.query(UserNotification)\
            .filter_by(telegram_id=user_id, car_plate=car).all()

        for notification in notifications:
            session.delete(notification)

        session.commit()
        
    finally:
        session.close()

def remove_user_car_notification_from_db(surr_id: int):
    """Remove a specific notification for a user's car."""
    session = get_local_session()
    try:
        notification = session.query(UserNotification)\
            .filter_by(surr_id=surr_id)\
            .first()

        if notification:
            session.delete(notification)
            session.commit()
        else:
            print(f"[WARN] No active notification found for surr_id {surr_id}.")

    finally:
        session.close()

def deactivate_user_car_notification_in_db(surr_id: int):
    """Deactivate (set status to False) a specific notification for a user's car."""
    session = get_local_session()
    try:
        notification = session.query(UserNotification)\
            .filter_by(surr_id=surr_id, notification_status=True)\
            .first()

        if notification:
            notification.notification_status = False
            session.commit()
        else:
            print(f"[WARN] No active notification found for surr_id {surr_id}.")

    finally:
        session.close()

def activate_user_car_notification_in_db(surr_id: int, car: str, car_type: str):
    """Activate (set status to True) a specific notification for a user's car."""
    """Also checks if the car is currently in any queue."""

    current_status = get_user_cars_current_status(car, car_type)
    if not current_status:
        return False

    session = get_local_session()
    try:
        notification = session.query(UserNotification)\
            .filter_by(surr_id=surr_id, notification_status=False)\
            .first()

        if notification:
            notification.notification_status = True
            session.commit()
            return True
        else:
            print(f"[WARN] No inactive notification found for surr_id {surr_id}.")
            return False

    finally:
        session.close()

def get_user_car_types_from_db(user_id: int, car: str):
    """Fetch distinct car types for a user."""
    session: Session = get_local_session()
    try:
        car_types = (
            session.query(UserCars.car_type)
            .filter(UserCars.telegram_id == user_id, UserCars.plate == car)
            .first()
        )
        return car_types  # Extract car_type from tuples
    finally:
        session.close()