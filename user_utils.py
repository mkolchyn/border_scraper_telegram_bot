from telegram import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from db_functions import SessionLocal
from models import DBUser, UserAction

def log_user_action(user: User, action: str):
    """Log a user action into Postgres."""
    session: Session = SessionLocal()
    try:
        # Lookup by telegram_id, not surrogate id
        db_user = session.query(DBUser).filter_by(telegram_id=user.id).order_by(DBUser.surr_id.desc()).first()
        if not db_user:
            db_user = DBUser(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
            )
            session.add(db_user)
            session.flush()  # ensures surrogate id is available

        # Save action, link to surrogate id
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
    """Return stored language for user, default 'en' if not set."""
    session: Session = SessionLocal()
    try:
        db_user = session.query(DBUser).filter_by(telegram_id=user_id).order_by(DBUser.surr_id.desc()).first()
        return db_user.lang if db_user and db_user.lang else "en"
    finally:
        session.close()

def set_user_lang(user: User, lang: str):
    """Set or update language preference for user."""
    session: Session = SessionLocal()
    try:
        db_user = session.query(DBUser).filter_by(telegram_id=user.id).order_by(DBUser.surr_id.desc()).first()
        if db_user:
            db_user.lang = lang
        else:
            db_user = DBUser(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                lang=lang
            )
            session.add(db_user)
        session.commit()
    finally:
        session.close()
