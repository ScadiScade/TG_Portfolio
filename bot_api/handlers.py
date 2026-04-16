import asyncio
import re
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from api_client import ExchangeAPIClient
from config import REQUIRED_CHANNEL

router = Router()
api = ExchangeAPIClient()

def get_channel_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="📢 Subscribe", url=f"https://t.me/{REQUIRED_CHANNEL.replace('@', '')}")
    builder.button(text="✅ Check Subscription", callback_data="check_sub")
    builder.adjust(1)
    return builder.as_markup()

async def check_subscription(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=REQUIRED_CHANNEL, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Sub check failed (bot might not be admin in channel): {e}")
        # If the bot is not an admin, we just let them pass for this demo.
        return True

@router.message(Command("start"))
async def cmd_start(message: Message, bot: Bot):
    is_sub = await check_subscription(bot, message.from_user.id)
    if not is_sub:
        await message.answer(
            f"Please subscribe to our channel {REQUIRED_CHANNEL} to use this bot!",
            reply_markup=get_channel_keyboard()
        )
        return
        
    await message.answer(
        "👋 Welcome to the Currency Exchange Bot!\n\n"
        "Send me a message in the format:\n"
        "`<Amount> <From> to <To>`\n\n"
        "Example:\n`100 USD to EUR`\n`50 GBP to JPY`",
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "check_sub")
async def process_sub_check(callback: CallbackQuery, bot: Bot):
    is_sub = await check_subscription(bot, callback.from_user.id)
    if is_sub:
        await callback.message.delete()
        await callback.message.answer("Thank you for subscribing! Send me a currency to convert.\nExample: `100 USD to EUR`", parse_mode="Markdown")
    else:
        await callback.answer("You are still not subscribed!", show_alert=True)

@router.message(F.text)
async def handle_convert(message: Message, bot: Bot):
    is_sub = await check_subscription(bot, message.from_user.id)
    if not is_sub:
        await message.answer("Please subscribe first.", reply_markup=get_channel_keyboard())
        return

    text = message.text.upper()
    
    # Simple regex to match "100 USD TO EUR" or "100 USD EUR"
    match = re.search(r'(\d+(?:\.\d+)?)\s*([A-Z]{3})(?:\s+TO\s+|\s+)([A-Z]{3})', text)
    if not match:
        await message.answer("❌ Invalid format.\n\nPlease use: `<Amount> <From> to <To>`\nExample: `100 USD to EUR`", parse_mode="Markdown")
        return
        
    amount_str, from_curr, to_curr = match.groups()
    amount = float(amount_str)
    
    msg = await message.answer("⏳ Converting...")
    
    result = await api.convert(amount, from_curr, to_curr)
    
    if result is None:
        await msg.edit_text("❌ Failed to get exchange rates. Please check if the currency codes are correct.")
        return
        
    await msg.edit_text(
        f"💱 **Exchange Result**\n\n"
        f"From: `{amount} {from_curr}`\n"
        f"To: `{result} {to_curr}`",
        parse_mode="Markdown"
    )
