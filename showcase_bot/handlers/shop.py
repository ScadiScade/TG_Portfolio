import json
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import db
from handlers.common import get_main_menu_keyboard, get_user_language
from locales import get_text

router = Router()

class ShopState(StatesGroup):
    viewing_item = State()

OPTIONS_PRICES = {
    "opt_admin": 5000,
    "opt_payment": 3000,
    "opt_deploy": 2000,
    "opt_multi": 4000,
}

def get_shop_keyboard(lang: str):
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text("btn_catalog", lang), callback_data="shop_catalog")
    builder.button(text=get_text("btn_cart", lang), callback_data="shop_cart")
    builder.button(text=get_text("btn_back_main", lang), callback_data="back_main")
    builder.adjust(2, 1)
    return builder.as_markup()

def format_price(amount: int, lang: str) -> str:
    if lang == "en":
        return f"${amount // 50}"
    return f"{amount} ₽"

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
async def show_catalog(callback: CallbackQuery, state: FSMContext):
    lang = await get_user_language(callback.from_user)
    await state.clear()
    
    items = await db.get_items()
    if not items:
        await callback.message.edit_text(get_text("catalog_empty", lang), reply_markup=get_shop_keyboard(lang))
        return

    builder = InlineKeyboardBuilder()
    for item in items:
        item_name = get_text(item['name'], lang)
        price_str = format_price(item['price'], lang)
        builder.button(text=f"{item_name} - {price_str}", callback_data=f"shop_item_{item['id']}")
    
    builder.button(text=get_text("btn_back_shop", lang), callback_data="demo_shop")
    builder.adjust(1)
    
    await callback.message.edit_text(get_text("select_item", lang), reply_markup=builder.as_markup())

async def render_item_menu(message, item, selected_options, lang):
    builder = InlineKeyboardBuilder()
    
    total_price = item['price']
    
    for opt_key, opt_price in OPTIONS_PRICES.items():
        is_selected = selected_options.get(opt_key, False)
        prefix = "✅ " if is_selected else "❌ "
        if is_selected:
            total_price += opt_price
            
        btn_text = prefix + get_text(opt_key, lang)
        builder.button(text=btn_text, callback_data=f"shop_toggle_{opt_key}")
    
    builder.button(
        text=get_text("btn_add_cart", lang, total=format_price(total_price, lang).replace(" ₽", "").replace("$", "")),
        callback_data="shop_do_add"
    )
    builder.button(text=get_text("btn_catalog", lang), callback_data="shop_catalog")
    builder.adjust(1)
    
    item_name = get_text(item['name'], lang)
    item_desc = get_text(item['description'], lang)
    price_str = format_price(item['price'], lang)
    
    text = f"**{item_name}**\n\n{item_desc}\n\nЦена / Price: {price_str}"
    await message.edit_text(text, parse_mode="Markdown", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("shop_item_"))
async def show_item(callback: CallbackQuery, state: FSMContext):
    lang = await get_user_language(callback.from_user)
    item_id = int(callback.data.split("_")[2])
    item = await db.get_item(item_id)
    
    if not item:
        await callback.answer(get_text("item_not_found", lang))
        return

    await state.set_state(ShopState.viewing_item)
    await state.update_data(item_id=item_id, options={})
    
    await render_item_menu(callback.message, item, {}, lang)

@router.callback_query(F.data.startswith("shop_toggle_"), ShopState.viewing_item)
async def toggle_option(callback: CallbackQuery, state: FSMContext):
    lang = await get_user_language(callback.from_user)
    opt_key = callback.data.replace("shop_toggle_", "")
    
    data = await state.get_data()
    options = data.get("options", {})
    options[opt_key] = not options.get(opt_key, False)
    await state.update_data(options=options)
    
    item = await db.get_item(data["item_id"])
    await render_item_menu(callback.message, item, options, lang)

@router.callback_query(F.data == "shop_do_add", ShopState.viewing_item)
async def add_to_cart_with_options(callback: CallbackQuery, state: FSMContext):
    lang = await get_user_language(callback.from_user)
    data = await state.get_data()
    item_id = data["item_id"]
    options = data.get("options", {})
    
    item = await db.get_item(item_id)
    if not item:
        return
        
    total_price = item['price']
    selected_opts_list = []
    for k, v in options.items():
        if v:
            total_price += OPTIONS_PRICES[k]
            selected_opts_list.append(get_text(k, lang))
            
    options_str = "\n  + " + "\n  + ".join(selected_opts_list) + "\n" if selected_opts_list else "\n"
    
    await db.add_to_cart(callback.from_user.id, item_id, options_str, total_price)
    await state.clear()
    
    await callback.answer(get_text("added_to_cart", lang), show_alert=True)
    await show_catalog(callback, state)

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
        opts = item['options'] or ""
        item_name = get_text(item['name'], lang)
        cost_str = format_price(cost, lang).replace(" ₽", "").replace("$", "")
        text += get_text("cart_item", lang, name=item_name, options=opts, quantity=item['quantity'], cost=cost_str)
        
    total_str = format_price(total, lang).replace(" ₽", "").replace("$", "")
    text += get_text("cart_total", lang, total=total_str)
    
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text("btn_checkout", lang), callback_data="shop_checkout")
    builder.button(text=get_text("btn_clear_cart", lang), callback_data="shop_clear_cart")
    builder.button(text=get_text("btn_back_shop", lang), callback_data="demo_shop")
    builder.adjust(1)
    
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=builder.as_markup())

@router.callback_query(F.data == "shop_clear_cart")
async def clear_cart(callback: CallbackQuery, state: FSMContext):
    lang = await get_user_language(callback.from_user)
    await db.clear_cart(callback.from_user.id)
    await callback.answer(get_text("cart_cleared", lang))
    await start_shop(callback, state)

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
