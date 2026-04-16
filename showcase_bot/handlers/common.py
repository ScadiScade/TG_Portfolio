from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import WEB_APP_URL
from locales import get_text
import db

router = Router()

async def get_user_language(user) -> str:
    lang = await db.get_user_lang(user.id)
    return lang if lang else user.language_code

def get_main_menu_keyboard(lang: str):
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text("btn_shop", lang), callback_data="demo_shop")
    builder.button(text=get_text("btn_api", lang), callback_data="demo_currency")
    
    # URL button for TMA
    builder.button(text=get_text("btn_tma", lang), web_app=WebAppInfo(url=WEB_APP_URL))
    
    # Lang button
    builder.button(text=get_text("btn_lang", lang), callback_data="change_lang")
    
    builder.adjust(1)
    return builder.as_markup()

@router.message(Command("start"))
async def cmd_start(message: Message):
    lang = await get_user_language(message.from_user)
    await message.answer(
        get_text("main_welcome", lang),
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard(lang)
    )

@router.callback_query(F.data == "change_lang")
async def change_language(callback: CallbackQuery):
    current_lang = await get_user_language(callback.from_user)
    # Toggle logic: if ru -> en, else -> ru
    new_lang = "en" if current_lang == "ru" else "ru"
    
    await db.set_user_lang(callback.from_user.id, new_lang)
    
    await callback.message.edit_text(
        get_text("main_welcome", new_lang) + f"\n\n*( {get_text('lang_changed', new_lang)} )*",
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard(new_lang)
    )
