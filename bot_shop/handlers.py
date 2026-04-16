from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import db

router = Router()

def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🛍 Catalog", callback_data="catalog")
    builder.button(text="🛒 Cart", callback_data="cart")
    builder.adjust(2)
    return builder.as_markup()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Welcome to our Telegram Shop! 🚀\n\nChoose an action below:",
        reply_markup=get_main_keyboard()
    )

@router.callback_query(F.data == "catalog")
async def show_catalog(callback: CallbackQuery):
    items = await db.get_items()
    if not items:
        await callback.message.edit_text("Catalog is empty.", reply_markup=get_main_keyboard())
        return

    builder = InlineKeyboardBuilder()
    for item in items:
        builder.button(text=f"{item['name']} - ${item['price']}", callback_data=f"item_{item['id']}")
    
    builder.button(text="🔙 Back", callback_data="back_main")
    builder.adjust(1)
    
    await callback.message.edit_text("Please select an item:", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("item_"))
async def show_item(callback: CallbackQuery):
    item_id = int(callback.data.split("_")[1])
    item = await db.get_item(item_id)
    
    if not item:
        await callback.answer("Item not found.")
        return

    builder = InlineKeyboardBuilder()
    builder.button(text="➕ Add to Cart", callback_data=f"add_{item['id']}")
    builder.button(text="🔙 Back to Catalog", callback_data="catalog")
    builder.adjust(1)
    
    text = f"**{item['name']}**\n\n{item['description']}\n\nPrice: ${item['price']}"
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("add_"))
async def add_to_cart(callback: CallbackQuery):
    item_id = int(callback.data.split("_")[1])
    await db.add_to_cart(callback.from_user.id, item_id)
    await callback.answer("Item added to cart! 🛒", show_alert=True)

@router.callback_query(F.data == "cart")
async def show_cart(callback: CallbackQuery):
    cart_items = await db.get_cart(callback.from_user.id)
    
    if not cart_items:
        await callback.message.edit_text("Your cart is empty.", reply_markup=get_main_keyboard())
        return
        
    text = "🛒 **Your Cart**:\n\n"
    total = 0
    for item in cart_items:
        cost = item['price'] * item['quantity']
        total += cost
        text += f"- {item['name']} (x{item['quantity']}) = ${cost}\n"
        
    text += f"\n**Total: ${total}**"
    
    builder = InlineKeyboardBuilder()
    builder.button(text="💳 Checkout", callback_data="checkout")
    builder.button(text="🗑 Clear Cart", callback_data="clear_cart")
    builder.button(text="🔙 Back", callback_data="back_main")
    builder.adjust(1)
    
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=builder.as_markup())

@router.callback_query(F.data == "clear_cart")
async def clear_cart(callback: CallbackQuery):
    await db.clear_cart(callback.from_user.id)
    await callback.answer("Cart cleared.")
    await show_catalog(callback)

@router.callback_query(F.data == "checkout")
async def checkout(callback: CallbackQuery):
    # Usually here we generate an invoice via Telegram Payments API or send info to admin
    await db.clear_cart(callback.from_user.id)
    await callback.message.edit_text(
        "🎉 Thank you for your order! This is a demo bot, so no real payment is required.\n\n"
        "Your order has been recorded.",
        reply_markup=get_main_keyboard()
    )

@router.callback_query(F.data == "back_main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "Welcome to our Telegram Shop! 🚀\n\nChoose an action below:",
        reply_markup=get_main_keyboard()
    )
