from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import WEB_APP_URL
from locales import get_text

router = Router()

def get_main_menu_keyboard(lang: str):
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text("btn_shop", lang), callback_data="demo_shop")
    builder.button(text=get_text("btn_api", lang), callback_data="demo_currency")
    
    # URL button for TMA
    builder.button(text=get_text("btn_tma", lang), web_app=WebAppInfo(url=WEB_APP_URL))
    builder.adjust(1)
    return builder.as_markup()

@router.message(Command("start"))
async def cmd_start(message: Message):
    lang = message.from_user.language_code
    await message.answer(
        get_text("main_welcome", lang),
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard(lang)
    )
