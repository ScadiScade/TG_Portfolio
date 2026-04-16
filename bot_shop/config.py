import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN provided in .env file.")

ADMIN_ID = os.getenv("ADMIN_ID") # Optional for admin notifications
