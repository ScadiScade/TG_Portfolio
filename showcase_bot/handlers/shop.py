from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

import db
from handlers.common import get_main_menu_keyboard

router = Router()

def get_shop_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🛍 Catalog", callback_data="shop_catalog")
    builder.button(text="🛒 Cart", callback_data="shop_cart")
    builder.button(text="🔙 Back to Main", callback_data="back_main")
    builder.adjust(2, 1)
    return builder.as_markup()

@router.callback_query(F.data == "demo_shop")
async def start_shop(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "🛒 **Shop Demo**\n\n"
        "Here you can browse a dynamic catalog, add items to a cart, "
        "and proceed to a simulated checkout. Everything is saved in SQLite.",
        parse_mode="Markdown",
        reply_markup=get_shop_keyboard()
    )

@router.callback_query(F.data == "shop_catalog")
async def show_catalog(callback: CallbackQuery):
    items = await db.get_items()
    if not items:
        await callback.message.edit_text("Catalog is empty.", reply_markup=get_shop_keyboard())
        return

    builder = InlineKeyboardBuilder()
    for item in items:
        builder.button(text=f"{item['name']} - ${item['price']}", callback_data=f"shop_item_{item['id']}")
    
    builder.button(text="🔙 Back to Shop", callback_data="demo_shop")
    builder.adjust(1)
    
    await callback.message.edit_text("Please select an item:", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("shop_item_"))
async def show_item(callback: CallbackQuery):
    item_id = int(callback.data.split("_")[2])
    item = await db.get_item(item_id)
    
    if not item:
        await callback.answer("Item not found.")
        return

    builder = InlineKeyboardBuilder()
    builder.button(text="➕ Add to Cart", callback_data=f"shop_add_{item['id']}")
    builder.button(text="🔙 Catalog", callback_data="shop_catalog")
    builder.adjust(1)
    
    text = f"**{item['name']}**\n\n{item['description']}\n\nPrice: ${item['price']}"
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("shop_add_"))
async def add_to_cart(callback: CallbackQuery):
    item_id = int(callback.data.split("_")[2])
    await db.add_to_cart(callback.from_user.id, item_id)
    await callback.answer("Item added to cart! 🛒", show_alert=True)

@router.callback_query(F.data == "shop_cart")
async def show_cart(callback: CallbackQuery):
    cart_items = await db.get_cart(callback.from_user.id)
    
    if not cart_items:
        await callback.message.edit_text("Your cart is empty.", reply_markup=get_shop_keyboard())
        return
        
    text = "🛒 **Your Cart**:\n\n"
    total = 0
    for item in cart_items:
        cost = item['price'] * item['quantity']
        total += cost
        text += f"- {item['name']} (x{item['quantity']}) = ${cost}\n"
        
    text += f"\n**Total: ${total}**"
    
    builder = InlineKeyboardBuilder()
    builder.button(text="💳 Checkout", callback_data="shop_checkout")
    builder.button(text="🗑 Clear Cart", callback_data="shop_clear_cart")
    builder.button(text="🔙 Back to Shop", callback_data="demo_shop")
    builder.adjust(1)
    
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=builder.as_markup())

@router.callback_query(F.data == "shop_clear_cart")
async def clear_cart(callback: CallbackQuery):
    await db.clear_cart(callback.from_user.id)
    await callback.answer("Cart cleared.")
    await start_shop(callback, FSMContext(storage=None, key=None))

@router.callback_query(F.data == "shop_checkout")
async def checkout(callback: CallbackQuery):
    await db.clear_cart(callback.from_user.id)
    await callback.message.edit_text(
        "🎉 Thank you for your order! (Demo mode)\n\n"
        "Your order has been recorded. In a real bot, you would be redirected to a payment provider.",
        reply_markup=get_shop_keyboard()
    )

@router.callback_query(F.data == "back_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "👋 Welcome back to the Main Menu!\n\n"
        "Select a demo below:",
        reply_markup=get_main_menu_keyboard()
    )
