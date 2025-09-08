from telegram import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from db_functions import SessionLocal
from models import DBUser, UserAction
from datetime import datetime, timezone

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
