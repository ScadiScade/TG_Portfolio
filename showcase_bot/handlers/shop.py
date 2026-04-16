from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

import db
from handlers.common import get_main_menu_keyboard, get_user_language
from locales import get_text

router = Router()

def get_shop_keyboard(lang: str):
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text("btn_catalog", lang), callback_data="shop_catalog")
    builder.button(text=get_text("btn_cart", lang), callback_data="shop_cart")
    builder.button(text=get_text("btn_back_main", lang), callback_data="back_main")
    builder.adjust(2, 1)
    return builder.as_markup()

@router.callback_query(F.data == "demo_shop")
async def start_shop(callback: CallbackQuery, state: FSMContext):
    lang = await get_user_language(callback.from_user)
    await state.clear()
    await callback.message.edit_text(
        get_text("shop_welcome", lang),
        parse_mode="Markdown",
        reply_markup=get_shop_keyboard(lang)
    )

@router.callback_query(F.data == "shop_catalog")
async def show_catalog(callback: CallbackQuery):
    lang = await get_user_language(callback.from_user)
    items = await db.get_items()
    if not items:
        await callback.message.edit_text(get_text("catalog_empty", lang), reply_markup=get_shop_keyboard(lang))
        return

    builder = InlineKeyboardBuilder()
    for item in items:
        builder.button(text=f"{item['name']} - ${item['price']}", callback_data=f"shop_item_{item['id']}")
    
    builder.button(text=get_text("btn_back_shop", lang), callback_data="demo_shop")
    builder.adjust(1)
    
    await callback.message.edit_text(get_text("select_item", lang), reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("shop_item_"))
async def show_item(callback: CallbackQuery):
    lang = await get_user_language(callback.from_user)
    item_id = int(callback.data.split("_")[2])
    item = await db.get_item(item_id)
    
    if not item:
        await callback.answer(get_text("item_not_found", lang))
        return

    builder = InlineKeyboardBuilder()
    builder.button(text=get_text("btn_add_cart", lang), callback_data=f"shop_add_{item['id']}")
    builder.button(text=get_text("btn_catalog", lang), callback_data="shop_catalog")
    builder.adjust(1)
    
    text = f"**{item['name']}**\n\n{item['description']}\n\nPrice: ${item['price']}"
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("shop_add_"))
async def add_to_cart(callback: CallbackQuery):
    lang = await get_user_language(callback.from_user)
    item_id = int(callback.data.split("_")[2])
    await db.add_to_cart(callback.from_user.id, item_id)
    await callback.answer(get_text("added_to_cart", lang), show_alert=True)

@router.callback_query(F.data == "shop_cart")
async def show_cart(callback: CallbackQuery):
    lang = await get_user_language(callback.from_user)
    cart_items = await db.get_cart(callback.from_user.id)
    
    if not cart_items:
        await callback.message.edit_text(get_text("cart_empty", lang), reply_markup=get_shop_keyboard(lang))
        return
        
    text = get_text("cart_header", lang)
    total = 0
    for item in cart_items:
        cost = item['price'] * item['quantity']
        total += cost
        text += f"- {item['name']} (x{item['quantity']}) = ${cost}\n"
        
    text += get_text("cart_total", lang, total=total)
    
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text("btn_checkout", lang), callback_data="shop_checkout")
    builder.button(text=get_text("btn_clear_cart", lang), callback_data="shop_clear_cart")
    builder.button(text=get_text("btn_back_shop", lang), callback_data="demo_shop")
    builder.adjust(1)
    
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=builder.as_markup())

@router.callback_query(F.data == "shop_clear_cart")
async def clear_cart(callback: CallbackQuery):
    lang = await get_user_language(callback.from_user)
    await db.clear_cart(callback.from_user.id)
    await callback.answer(get_text("cart_cleared", lang))
    await start_shop(callback, FSMContext(storage=None, key=None))

@router.callback_query(F.data == "shop_checkout")
async def checkout(callback: CallbackQuery):
    lang = await get_user_language(callback.from_user)
    await db.clear_cart(callback.from_user.id)
    await callback.message.edit_text(
        get_text("checkout_success", lang),
        reply_markup=get_shop_keyboard(lang)
    )

@router.callback_query(F.data == "back_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    lang = await get_user_language(callback.from_user)
    await state.clear()
    await callback.message.edit_text(
        get_text("welcome_back", lang),
        reply_markup=get_main_menu_keyboard(lang)
    )
