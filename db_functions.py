import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import math

# Load environment variables from .env file
load_dotenv()

# SQLAlchemy Base
Base = declarative_base()

def local_get_engine():
    """Create a SQLAlchemy engine."""
    db_url = (
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    return create_engine(db_url, pool_pre_ping=True, future=True)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=local_get_engine())

def remote_get_engine():
    """Engine for the Border Scraper DB"""
    db_url = (
        f"postgresql+psycopg2://{os.getenv('BS_DB_USER')}:{os.getenv('BS_DB_PASSWORD')}"
        f"@{os.getenv('BS_DB_HOST')}:{os.getenv('BS_DB_PORT')}/{os.getenv('BS_DB_NAME')}"
    )
    return create_engine(db_url, pool_pre_ping=True, future=True)

SessionRemote = sessionmaker(autocommit=False, autoflush=False, bind=remote_get_engine())


def get_queue_speed(buffer_zone_id: int):
    """Fetch the latest 5 queue speed records from the remote DB."""
    session = SessionRemote()
    try:
        result = session.execute(
            text("SELECT * FROM public.get_queue_speed(:buffer_zone_id)"),
            {"buffer_zone_id": buffer_zone_id}
        )
        return result.fetchall()
    finally:
        session.close()


def create_queue_table_image(rows, title="Queue Speed Table"):
    """
    Create a table image from DB rows.
    
    Returns a BytesIO object containing the PNG image.
    """
    if not rows:
        return None

    # Convert rows to DataFrame
    df = pd.DataFrame(rows, columns=[
        "Buffer ID", "Plate", "Registered", "Last Change",
        "Time in Queue (h)", "Cars in Queue", "Queue Speed (cars/h)"
    ])

    # Remove Buffer ID
    df = df.drop(columns=["Buffer ID"])

    # Format numeric columns
    def format_time_dhm(hours):
        """
        Convert decimal hours to 'Xd Yh Zm' format.
        """
        if hours is None:
            return ""
        
        total_minutes = int(round(hours * 60))
        days = total_minutes // (24 * 60)
        hours_remainder = (total_minutes % (24 * 60)) // 60
        minutes = total_minutes % 60

        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours_remainder > 0 or days > 0:
            parts.append(f"{hours_remainder}h")
        parts.append(f"{minutes}m")

        return " ".join(parts)

    df["Time in Queue (h)"] = df["Time in Queue (h)"].map(format_time_dhm)
    df["Cars in Queue"] = df["Cars in Queue"].map(lambda x: f"{int(x)}" if x is not None and not math.isnan(x) else "")
    df["Queue Speed (cars/h)"] = df["Queue Speed (cars/h)"].map(lambda x: f"{x:.2f}" if x is not None else "")

    # Create figure
    fig, ax = plt.subplots(figsize=(12, len(df)*0.5 + 1))
    ax.axis("off")
    ax.axis("tight")

    # Create table
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc="center",
        loc="center"
    )

    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.auto_set_column_width(col=list(range(len(df.columns))))
    table.scale(1, 2) # Scale height

    # Add title
    plt.title(title, fontsize=16, pad=20)

    # Save to BytesIO
    img_bytes = BytesIO()
    plt.savefig(img_bytes, format="png", bbox_inches="tight")
    plt.close(fig)
    img_bytes.seek(0)

    return img_bytes
