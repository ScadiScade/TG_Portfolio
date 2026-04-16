import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN provided in .env file.")

# For Currency API Demo
API_KEY = os.getenv("EXCHANGE_API_KEY", "demo")
REQUIRED_CHANNEL = os.getenv("REQUIRED_CHANNEL", "")

# For TMA Demo
WEB_APP_URL = os.getenv("WEB_APP_URL", "https://scadi.github.io/portfolio/mini_app/dist")
