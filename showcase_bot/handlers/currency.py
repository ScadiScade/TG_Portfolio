import re
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from api_client import ExchangeAPIClient
from handlers.common import get_main_menu_keyboard, get_user_language
from locales import get_text

router = Router()
api = ExchangeAPIClient()

class CurrencyState(StatesGroup):
    waiting_for_amount = State()

def get_cancel_keyboard(lang: str):
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text("btn_cancel", lang), callback_data="back_main")
    return builder.as_markup()

@router.callback_query(F.data == "demo_currency")
async def start_currency(callback: CallbackQuery, state: FSMContext):
    lang = await get_user_language(callback.from_user)
    await state.set_state(CurrencyState.waiting_for_amount)
    
    await callback.message.edit_text(
        get_text("currency_welcome", lang),
        parse_mode="Markdown",
        reply_markup=get_cancel_keyboard(lang)
    )

@router.message(CurrencyState.waiting_for_amount)
async def process_currency_input(message: Message, state: FSMContext):
    lang = await get_user_language(message.from_user)
    text = message.text.upper()
    
    # Matches: 100 USD TO EUR, 100 USD В EUR, 100 USD EUR
    match = re.search(r'(\d+(?:\.\d+)?)\s*([A-Z]{3})(?:\s+(?:TO|В)\s+|\s+)([A-Z]{3})', text, re.IGNORECASE)
    if not match:
        await message.answer(
            get_text("invalid_format", lang),
            parse_mode="Markdown",
            reply_markup=get_cancel_keyboard(lang)
        )
        return
        
    amount_str, from_curr, to_curr = match.groups()
    amount = float(amount_str)
    
    msg = await message.answer(get_text("converting", lang), reply_markup=get_cancel_keyboard(lang))
    
    result = await api.convert(amount, from_curr, to_curr)
    
    if result is None:
        await msg.edit_text(
            get_text("api_error", lang),
            reply_markup=get_cancel_keyboard(lang)
        )
        return
        
    await msg.edit_text(
        get_text("exchange_result", lang, amount=amount, from_curr=from_curr, result=result, to_curr=to_curr),
        parse_mode="Markdown",
        reply_markup=get_cancel_keyboard(lang)
    )
