import re
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from api_client import ExchangeAPIClient
from handlers.common import get_main_menu_keyboard

router = Router()
api = ExchangeAPIClient()

class CurrencyState(StatesGroup):
    waiting_for_amount = State()

def get_cancel_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Cancel & Back", callback_data="back_main")
    return builder.as_markup()

@router.callback_query(F.data == "demo_currency")
async def start_currency(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CurrencyState.waiting_for_amount)
    
    await callback.message.edit_text(
        "💱 **Currency API Demo**\n\n"
        "This demo uses `aiohttp` and FSM (Finite State Machine).\n"
        "Please send me the amount and currencies you want to convert in this format:\n\n"
        "`<Amount> <From> to <To>`\n\n"
        "Example: `100 USD to EUR`",
        parse_mode="Markdown",
        reply_markup=get_cancel_keyboard()
    )

@router.message(CurrencyState.waiting_for_amount)
async def process_currency_input(message: Message, state: FSMContext):
    text = message.text.upper()
    
    match = re.search(r'(\d+(?:\.\d+)?)\s*([A-Z]{3})(?:\s+TO\s+|\s+)([A-Z]{3})', text)
    if not match:
        await message.answer(
            "❌ Invalid format.\n\nPlease use: `<Amount> <From> to <To>`\n"
            "Example: `100 USD to EUR`\n\nOr click cancel:",
            parse_mode="Markdown",
            reply_markup=get_cancel_keyboard()
        )
        return
        
    amount_str, from_curr, to_curr = match.groups()
    amount = float(amount_str)
    
    msg = await message.answer("⏳ Converting via API...", reply_markup=get_cancel_keyboard())
    
    result = await api.convert(amount, from_curr, to_curr)
    
    if result is None:
        await msg.edit_text(
            "❌ Failed to get exchange rates. Please check if the currency codes are correct.",
            reply_markup=get_cancel_keyboard()
        )
        return
        
    await msg.edit_text(
        f"💱 **Exchange Result**\n\n"
        f"From: `{amount} {from_curr}`\n"
        f"To: `{result} {to_curr}`\n\n"
        f"Send another amount or go back:",
        parse_mode="Markdown",
        reply_markup=get_cancel_keyboard()
    )
