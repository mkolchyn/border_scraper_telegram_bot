from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime, func, Boolean
from db_functions import Base

class DBUser(Base):
    __tablename__ = "users"

    # Surrogate key
    surr_id = Column(Integer, primary_key=True, autoincrement=True)

    # Telegram user_id (unique natural key)
    telegram_id = Column(BigInteger, unique=False, index=True, nullable=False)

    username = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    lang = Column(String(5), default="en")

    # New car-related columns (nullable)
    car_1 = Column(String(10), nullable=True)
    car_2 = Column(String(10), nullable=True)
    car_3 = Column(String(10), nullable=True)

    # Slowly changing dimension fields
    valid_from = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    valid_to = Column(DateTime(timezone=True), nullable=True)  # NULL = still active
    is_current = Column(Boolean, default=True, nullable=False)

class UserAction(Base):
    __tablename__ = "user_actions"

    surr_id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, nullable=False)
    action = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class UserNotification(Base):
    __tablename__ = "user_notification"

    surr_id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, index=True, nullable=False)
    car_plate = Column(String(20), nullable=False)
    notification_type = Column(String(50), nullable=False)
    notification_value = Column(Integer, nullable=True)
    notification_status = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    changed_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )