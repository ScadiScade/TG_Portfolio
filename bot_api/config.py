import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN provided in .env file.")

# For a real project, this would be an API key from an exchange rate provider
# (e.g., exchangeratesapi.io, fixer.io)
API_KEY = os.getenv("EXCHANGE_API_KEY", "demo")

# Required channel to subscribe to use the bot
REQUIRED_CHANNEL = os.getenv("REQUIRED_CHANNEL", "@my_sponsor_channel")
