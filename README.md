# Border Scraper Telegram Bot

[Production bot](https://t.me/BY_BorderStats_bot)

## Overview

**Border Scraper Telegram Bot** helps travelers crossing from **Belarus to the EU** stay informed about border queue statuses in real time. It provides historical statistics, queue speed estimations, and personalized car tracking via a friendly Telegram interface.

This bot is designed for convenience, speed, and multilingual support (English, Russian). Whether you’re monitoring queues for personal travel, logistics, or simply want data-driven insights, this bot offers reliable border crossing intelligence.

---

## Features

- **Live Border Queue Tracking**
  - Instantly view the number of cars, trucks, buses, and motorcycles waiting at key Belarus-EU checkpoints.
  - Border points supported: Benyakoni, Brest BTS ("Varshavskiy Most"), Kamenny Log, Grigorovschina, Kozlovichi.

- **Historical Statistics**
  - Access statistics and trends for border queue lengths and speeds.
  - Visualize historical data by country, year, and month.

- **Queue Speed Estimations**
  - Estimate your approximate waiting time based on queue position and average speed.

- **Personal Car Tracking & Notifications**
  - Track your car’s queue status by license plate.
  - Receive notifications when your vehicle is summoned or passes key checkpoints.
  - Configure notification preferences and car types.

- **Multilingual Support**
  - Choose between English and Russian for all menus and responses.

- **Dockerized Deployment**
  - Easy, lightweight deployment using Docker.

---

## Getting Started

### Prerequisites

- **Python 3.13+**
- Telegram Bot token from [BotFather](https://core.telegram.org/bots#botfather)
- PostgreSQL database for advanced statistics

### Setup

1. **Clone the Repository**
   ```sh
   git clone https://github.com/mkolchyn/border_scraper_telegram_bot.git
   cd border_scraper_telegram_bot
   ```

2. **Configure Environment**
   - Copy `.env.example` to `.env` and set your Telegram bot token (`BOT_TOKEN`) and database credentials.

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the Bot**
   ```sh
   python main.py
   ```
   Or use Docker:
   ```sh
   docker build -t border-scraper-bot .
   docker run -d --env-file .env border-scraper-bot
   ```

---

## Usage

- **Start the Bot:** Message your bot on Telegram and use the `/start` command.
- **Navigate Menus:** Choose language, view queues, check statistics, estimate wait times, or set up car tracking.
- **Get Notifications:** Register your vehicle to receive push notifications about your queue status.

---

## Technologies

- **Python** (telegram-ext, requests, SQLAlchemy)
- **Docker**
- **PostgreSQL** (for historical/statistics data)
- **Telegram Bot API**

---

## Contributing

PRs and suggestions are welcome! For major changes, please open an issue first to discuss your ideas.
