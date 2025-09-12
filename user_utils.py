from telegram import User, InputMediaPhoto, InlineKeyboardMarkup
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from db_functions import SessionLocal
from models import DBUser, UserAction, UserNotification
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
    session: Session = SessionLocal()
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
    session: Session = SessionLocal()
    try:
        db_user = session.query(DBUser)\
            .filter_by(telegram_id=user_id, is_current=True)\
            .order_by(DBUser.surr_id.desc()).first()
        return db_user.lang if db_user and db_user.lang else "en"
    finally:
        session.close()


def set_user_lang(user: User, lang: str):
    """Set or update language preference for user using SCD2."""
    session: Session = SessionLocal()
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
                    lang=lang,
                    car_1=db_user.car_1,
                    car_2=db_user.car_2,
                    car_3=db_user.car_3
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

def get_user_cars_current_status(car: str):
    """Check if 'car' is currently in any queue zones."""
    buffer_zones = {
        "benyakoni": "53d94097-2b34-11ec-8467-ac1f6bf889c0",
        "brest_bts": "a9173a85-3fc0-424c-84f0-defa632481e4",
        "kamenny_log": "b60677d4-8a00-4f93-a781-e129e1692a03",
        "grigorovschina": "ffe81c11-00d6-11e8-a967-b0dd44bde851",
    }

    for buffer_zone_name, checkpointID in buffer_zones.items():
        url = f"https://belarusborder.by/info/monitoring-new?token=test&checkpointId={checkpointID}"
        data = fetch_data_from_api(url)

        if not data:
            continue

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

    return None

def set_user_car_into_db(user: User, car: str, lang: str):
    """Set car for 'user' table using SCD2."""
    session = SessionLocal()
    try:
        db_user = (
            session.query(DBUser)
            .filter_by(telegram_id=user.id, is_current=True)
            .order_by(DBUser.surr_id.desc())
            .first()
        )

        if db_user:
            # Determine which car slot to fill
            if db_user.car_1 is None:
                slot = "car_1"
            elif db_user.car_2 is None:
                slot = "car_2"
            elif db_user.car_3 is None:
                slot = "car_3"
            else:
                # All slots full, maybe overwrite car_1 or return
                slot = None

            if slot:
                # Close old record
                db_user.valid_to = datetime.now(timezone.utc)
                db_user.is_current = False

                # Create new record with updated car
                new_user = DBUser(
                    telegram_id=user.id,
                    username=db_user.username,
                    first_name=db_user.first_name,
                    last_name=db_user.last_name,
                    joined_at=db_user.joined_at,
                    lang=lang,
                    car_1=db_user.car_1 if slot != "car_1" else car,
                    car_2=db_user.car_2 if slot != "car_2" else car,
                    car_3=db_user.car_3 if slot != "car_3" else car
                )
                session.add(new_user)
        else:
            # New user, insert record with car_1
            new_user = DBUser(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                joined_at=datetime.now(timezone.utc),
                lang=lang,
                car_1=car
            )
            session.add(new_user)

        session.commit()
    finally:
        session.close()

def get_user_cars_from_db(user_id: int):
    """Fetch all cars for a user using ORM (may include None)."""
    session: Session = SessionLocal()
    try:
        db_user = (
            session.query(DBUser)
            .filter(DBUser.telegram_id == user_id, DBUser.is_current == True)
            .order_by(DBUser.surr_id.desc())
            .first()
        )
        if db_user:
            return [db_user.car_1, db_user.car_2, db_user.car_3]
        return []
    finally:
        session.close()

def remove_user_car_from_db(user_id: int, car: str):
    """Remove a specific car from user's tracked cars using SCD2."""
    session = SessionLocal()
    try:
        db_user = session.query(DBUser)\
            .filter_by(telegram_id=user_id, is_current=True).first()

        if db_user and car in (db_user.car_1, db_user.car_2, db_user.car_3):
            # Close old record
            db_user.valid_to = datetime.now(timezone.utc)
            db_user.is_current = False

            # Create new record without the specified car
            new_user = DBUser(
                telegram_id=db_user.telegram_id,
                username=db_user.username,
                first_name=db_user.first_name,
                last_name=db_user.last_name,
                joined_at=db_user.joined_at,
                lang=db_user.lang,
                car_1=db_user.car_1 if db_user.car_1 != car else None,
                car_2=db_user.car_2 if db_user.car_2 != car else None,
                car_3=db_user.car_3 if db_user.car_3 != car else None
            )
            session.add(new_user)
            session.commit()
    finally:
        session.close()

def set_user_car_notification_in_db(user_id: int, car: str, notification_type: str, notification_value: int):
    """Set a notification for a user's car."""
    session = SessionLocal()
    try:
        db_user = session.query(DBUser)\
            .filter_by(telegram_id=user_id, is_current=True).first()

        if db_user and car in (db_user.car_1, db_user.car_2, db_user.car_3):
            new_notification = UserNotification(
                telegram_id=user_id,
                car_plate=car,
                notification_type=notification_type,
                notification_value=notification_value
            )
            session.add(new_notification)
        else:
            print(f"[WARN] User {user_id} does not track car {car}, cannot set notification.")

        session.commit()
        
    finally:
        session.close()

def get_user_car_notifications_from_db(user_id: int, car: str):
    """Fetch all active notifications for a user's specific car."""
    session = SessionLocal()
    try:
        notifications = session.query(UserNotification)\
            .filter_by(telegram_id=user_id, car_plate=car).all()
        return notifications
    finally:
        session.close()

def remove_user_car_notification_from_db(surr_id: int):
    """Remove a specific notification for a user's car."""
    session = SessionLocal()
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
    session = SessionLocal()
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

def activate_user_car_notification_in_db(surr_id: int, car: str):
    """Activate (set status to True) a specific notification for a user's car."""
    """Also checks if the car is currently in any queue."""

    current_status = get_user_cars_current_status(car)
    if not current_status:
        return False

    session = SessionLocal()
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