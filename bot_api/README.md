# API Integration Bot 💱

A Telegram bot demonstrating integration with a third-party REST API (`ExchangeRate-API`), implemented in Python with `aiogram 3.x`.

## Features
- **External API Connection**: Fetching live exchange rates via `aiohttp`.
- **Mandatory Subscription**: Validates user subscription to a sponsor channel before allowing access to the bot (a highly requested freelance feature).
- **Regex Parsing**: Validates and extracts user input effectively.

## Tech Stack
- Python 3.9+
- [aiogram 3.x](https://docs.aiogram.dev/en/latest/) - Async Telegram framework
- `aiohttp` - Async HTTP client
- Open ExchangeRate API (Free tier)

## How to run
1. Clone this repository.
2. Create virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
3. Set your environment variables in `.env`:
   ```env
   BOT_TOKEN=your_bot_token
   REQUIRED_CHANNEL=@your_channel_username
   ```
4. Run the bot:
   ```bash
   python bot.py
   ```
*Created as a demonstration of skills for freelance clients.*
