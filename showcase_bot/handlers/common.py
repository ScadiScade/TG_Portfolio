from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import WEB_APP_URL

router = Router()

def get_main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🛒 Demo: Shop", callback_data="demo_shop")
    builder.button(text="💱 Demo: API Converter", callback_data="demo_currency")
    
    # URL button for TMA
    builder.button(text="📱 Demo: Web App (TMA)", web_app=WebAppInfo(url=WEB_APP_URL))
    builder.adjust(1)
    return builder.as_markup()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Welcome to my **Portfolio Bot**!\n\n"
        "Here you can see different features that I can build for your business:\n"
        "1️⃣ **Shop Demo**: E-commerce with cart and inline catalogs.\n"
        "2️⃣ **API Demo**: Third-party REST API integration (Currency) with FSM.\n"
        "3️⃣ **Web App Demo**: Frontend Telegram Mini App on TypeScript.\n\n"
        "Select a demo below to start:",
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard()
    )
