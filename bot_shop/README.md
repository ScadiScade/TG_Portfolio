# Telegram Shop Bot 🛒

This is a portfolio project demonstrating an e-commerce Telegram bot built with Python and `aiogram 3.x`.

## Features
- **Dynamic Catalog**: Fetching products from a SQLite database.
- **Cart System**: Users can add multiple items to their cart.
- **Checkout Process**: Mock checkout to demonstrate flow.
- **Async DB**: Uses `aiosqlite` for non-blocking database operations.

## Tech Stack
- Python 3.9+
- [aiogram 3.x](https://docs.aiogram.dev/en/latest/) - Async Telegram Bot API wrapper
- `aiosqlite` - Async SQLite wrapper

## How to run
1. Clone this repository.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your bot token:
   ```env
   BOT_TOKEN=your_telegram_bot_token_here
   ```
4. Run the bot:
   ```bash
   python bot.py
   ```

*Created as a demonstration of skills for freelance clients.*
