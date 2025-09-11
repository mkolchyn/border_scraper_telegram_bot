-- Users table
CREATE TABLE IF NOT EXISTS users (
    surr_id SERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    joined_at TIMESTAMP NOT NULL DEFAULT NOW(),
    lang VARCHAR(5) DEFAULT 'en',
    car_1 VARCHAR(10),
    car_2 VARCHAR(10),
    car_3 VARCHAR(10),
    valid_from TIMESTAMP NOT NULL DEFAULT NOW(),
    valid_to TIMESTAMP,
    is_current BOOLEAN NOT NULL DEFAULT TRUE
);

-- Actions log table
CREATE TABLE IF NOT EXISTS user_actions (
    surr_id SERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL,
    action TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Notifications table
CREATE TABLE IF NOT EXISTS user_notification (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL,
    car_plate VARCHAR(20) NOT NULL,
    notification_type VARCHAR(50) NOT NULL,
    notification_value VARCHAR(100),
    notification_status BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    changed_at TIMESTAMP NOT NULL DEFAULT NOW()
);
