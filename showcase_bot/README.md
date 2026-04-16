# Unified Showcase Bot 🤖

This is the crown jewel of the portfolio. It combines all freelance skills into a single, modular Telegram bot built with `aiogram 3.x`.

## Features
- **Modular Architecture**: Uses `Router` to separate logic into `handlers/common.py`, `handlers/shop.py`, and `handlers/currency.py`.
- **FSM (Finite State Machine)**: Uses states to manage the currency converter input without colliding with other bot commands.
- **Async Database**: Full `aiosqlite` integration for the shop catalog and cart.
- **External API**: Connects to `aiohttp` for live data.
- **Telegram Mini App**: Serves a Web App (TMA) directly via an Inline Button.

## How to run
1. Clone this repository.
2. Go to this directory: `cd showcase_bot`
3. Create virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
4. Create `.env` file based on the config:
   ```env
   BOT_TOKEN=your_bot_token
   EXCHANGE_API_KEY=demo
   WEB_APP_URL=https://your-hosted-tma-url.com
   ```
5. Run the bot:
   ```bash
   python bot.py
   ```
