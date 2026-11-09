import os
import time
import requests
from dotenv import load_dotenv

from user_utils import (
    get_all_active_queue_notifications_from_db,
    set_user_queue_notification_status_in_db,
    get_user_lang,
)
from callbacks import CALLBACK_MAP_CURRENT
from texts import NOTIFICATIONS, ESTIMATIONS
from tracking_car import send_telegram_message

load_dotenv()

POLL_INTERVAL = 60
CHECKPOINT_URL = "https://belarusborder.by/info/checkpoint?token=bts47d5f-6420-4f74-8f78-42e8e4370cc4"

# zone name -> (checkpoint id, field that holds the queue length)
ZONES = {
    name: (checkpoint_id, "countTruck" if name == "kozlovichi" else "countCar")
    for checkpoint_id, name in CALLBACK_MAP_CURRENT.values()
}


def fetch_queue_lengths() -> dict:
    """Return {zone_name: queue_length} for all zones, using one API request."""
    response = requests.get(CHECKPOINT_URL, timeout=15)
    response.raise_for_status()
    by_id = {cp["id"]: cp for cp in response.json()["result"]}
    lengths = {}
    for name, (checkpoint_id, field) in ZONES.items():
        cp = by_id.get(checkpoint_id)
        if cp is not None and cp.get(field) is not None:
            lengths[name] = int(cp[field])
    return lengths


def side(current: int, threshold: int) -> int:
    """-1 below threshold, 0 exactly at it, 1 above it."""
    return (current > threshold) - (current < threshold)


def check_once(baselines: dict) -> None:
    """One pass: notify once for every enabled notification whose threshold was reached."""
    notifications = get_all_active_queue_notifications_from_db()
    active_ids = {n.surr_id for n in notifications}
    for surr_id in list(baselines):
        if surr_id not in active_ids:  # disabled/removed -> forget so it re-baselines when re-enabled
            del baselines[surr_id]
    if not notifications:
        return

    lengths = fetch_queue_lengths()
    for n in notifications:
        current = lengths.get(n.buffer_zone)
        if current is None:
            continue
        current_side = side(current, n.queue_length)
        previous_side = baselines.get(n.surr_id)
        baselines[n.surr_id] = current_side

        # reached = exactly at threshold, or crossed it in either direction since last check
        if current_side == 0 or (previous_side is not None and current_side != previous_side):
            lang = get_user_lang(n.telegram_id)
            zone_name = ESTIMATIONS[lang]["border_points_names"][n.buffer_zone]
            send_telegram_message(
                NOTIFICATIONS[lang]["queue_notification_reached"].format(zone_name, n.queue_length, current),
                n.telegram_id,
            )
            set_user_queue_notification_status_in_db(n.surr_id, n.telegram_id, False)
            baselines.pop(n.surr_id, None)


def run_queue_checker() -> None:
    baselines: dict = {}
    while True:
        try:
            check_once(baselines)
        except Exception as e:
            print(f"[WARN] queue checker failed: {e}")
        time.sleep(POLL_INTERVAL)
