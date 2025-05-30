import asyncio
from aiogram import Bot as TelegramBot, Dispatcher as TelegramDispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from typing import Dict, List
import tempfile
import os
from aiogram.types import FSInputFile
import logging
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
path = "/Users/kana/Desktop/git_proj/rest_bot/menu/menu.xlsx"

# Menu item mapping for shorter callback data
menu_item_map = {}  # Will store {category_item_id: (category, item_name)}
menu_item_counter = 0

def load_menu_from_excel(file_path: str = path) -> Dict:
    """Load menu from Excel file and convert to dictionary format"""
    global menu_item_counter, menu_item_map
    try:
        df = pd.read_excel(file_path)
        menu = {}
        menu_item_map.clear()  # Clear existing mapping
        menu_item_counter = 0  # Reset counter
        
        # Group by category and convert to list of dictionaries
        for category, group in df.groupby('Category'):
            menu[category] = []
            for _, row in group.iterrows():
                item = {
                    "english": row['English'],
                    "russian": row['Russian'],
                    "price": float(row['Price']),
                    "id": menu_item_counter
                }
                menu[category].append(item)
                # Store mapping for callback data
                menu_item_map[menu_item_counter] = (category, row['English'])
                menu_item_counter += 1
        
        return menu
    except Exception as e:
        print(f"Error loading menu: {e}")
        # Return a default menu if file can't be loaded
        return {
            "Error": [{"english": "Menu unavailable", "russian": "Меню недоступно", "price": 0.00, "id": 0}]
        }

# Load menu from Excel
MENU = load_menu_from_excel()

# Store user carts
user_carts: Dict[int, List[dict]] = {}

# Store user language preferences
user_languages: Dict[int, str] = {}

bot = TelegramBot(os.getenv("MY_API_KEY"))
telegram_dp = TelegramDispatcher()

# Translations dictionary
TRANSLATIONS = {
    "English": {
        "welcome": "Welcome to our Restaurant Bot! 🍽️\n\nPlease choose your language:",
        "menu_title": "🍽️ *Our Menu*\n\nPlease select a category:",
        "empty_cart": "Your cart is empty! Use /menu to start ordering.",
        "cart_title": "🛒 *Your Cart*\n\n",
        "total": "Total: ${:.2f}",
        "modify_cart_title": "✏️ *Modify Your Cart*\n\n",
        "select_items": "Select items to remove or clear all items:",
        "cart_cleared": "Your cart has been cleared!",
        "order_placed": "✅ *Order Placed!*\n\n",
        "thank_you": "Thank you for your order! We'll prepare it right away.",
        "help_text": """*Available Commands:*\n\n
/start - Start the bot
/menu - View the menu
/cart - View your cart
/help - Show this help message\n\n
You can also use the buttons in the menu to navigate.""",
        "back_to_menu": "🔙 Back to Menu",
        "view_cart": "🛒 View Cart",
        "modify_cart": "✏️ Modify Cart",
        "place_order": "✅ Place Order",
        "clear_all": "🗑 Clear All Items",
        "back_to_cart": "🔙 Back to Cart",
        "remove": "Remove"
    },
    "Russian": {
        "welcome": "Добро пожаловать в наш Ресторанный Бот! 🍽️\n\nПожалуйста, выберите язык:",
        "menu_title": "🍽️ *Наше Меню*\n\nПожалуйста, выберите категорию:",
        "empty_cart": "Ваша корзина пуста! Используйте /menu для начала заказа.",
        "cart_title": "🛒 *Ваша Корзина*\n\n",
        "total": "Итого: ${:.2f}",
        "modify_cart_title": "✏️ *Изменить Корзину*\n\n",
        "select_items": "Выберите товары для удаления или очистите корзину:",
        "cart_cleared": "Ваша корзина очищена!",
        "order_placed": "✅ *Заказ Размещен!*\n\n",
        "thank_you": "Спасибо за ваш заказ! Мы начнем его готовить прямо сейчас.",
        "help_text": """*Доступные Команды:*\n\n
/start - Начать работу с ботом
/menu - Просмотреть меню
/cart - Просмотреть корзину
/help - Показать это сообщение помощи\n\n
Вы также можете использовать кнопки в меню для навигации.""",
        "back_to_menu": "🔙 Назад в Меню",
        "view_cart": "🛒 Просмотр Корзины",
        "modify_cart": "✏️ Изменить Корзину",
        "place_order": "✅ Оформить Заказ",
        "clear_all": "🗑 Очистить Все",
        "back_to_cart": "🔙 Назад в Корзину",
        "remove": "Удалить"
    }
}

def get_main_menu_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Create main menu keyboard with categories"""
    keyboard = []
    lang = user_languages.get(user_id, "English")
    for category in MENU.keys():
        keyboard.append([InlineKeyboardButton(text=category, callback_data=f"category_{category}")])
    keyboard.append([InlineKeyboardButton(text=TRANSLATIONS[lang]["view_cart"], callback_data="view_cart")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_category_keyboard(category: str, user_id: int) -> InlineKeyboardMarkup:
    """Create keyboard for specific category items in user's language"""
    keyboard = []
    lang = user_languages.get(user_id, "English")
    for item in MENU[category]:
        if lang == "Russian":
            button_text = f"{item['russian']} - ${item['price']:.2f}\n"
        else:
            button_text = f"{item['english']} - ${item['price']:.2f}\n"
        keyboard.append([
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"a{item['id']}"  # Shortened callback data
            )
        ])
    keyboard.append([InlineKeyboardButton(text=TRANSLATIONS[lang]["back_to_menu"], callback_data="back_to_menu")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_cart_keyboard(cart_items: List[dict], user_id: int, is_modify_view: bool = False) -> InlineKeyboardMarkup:
    """Create keyboard for cart view with different options based on view type"""
    keyboard = []
    lang = user_languages.get(user_id, "English")
    
    if is_modify_view:
        for idx, item in enumerate(cart_items, 1):
            keyboard.append([
                InlineKeyboardButton(
                    text=f"❌ {TRANSLATIONS[lang]['remove']} {idx}. {item['english']}",
                    callback_data=f"remove_{idx-1}"
                )
            ])
        keyboard.extend([
            [InlineKeyboardButton(text=TRANSLATIONS[lang]["clear_all"], callback_data="clear_cart")],
            [InlineKeyboardButton(text=TRANSLATIONS[lang]["back_to_cart"], callback_data="view_cart")]
        ])
    else:
        keyboard.extend([
            [InlineKeyboardButton(text=TRANSLATIONS[lang]["modify_cart"], callback_data="modify_cart")],
            [InlineKeyboardButton(text=TRANSLATIONS[lang]["back_to_menu"], callback_data="back_to_menu")],
            [InlineKeyboardButton(text=TRANSLATIONS[lang]["place_order"], callback_data="place_order")]
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

@telegram_dp.message(Command("start"))
async def start(message: types.Message):
    """Handle /start command and ask for language selection"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="English"), KeyboardButton(text="Русский")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(
        TRANSLATIONS["English"]["welcome"],
        reply_markup=keyboard
    )

@telegram_dp.message(lambda message: message.text in ["English", "Русский"])
async def set_language(message: types.Message):
    user_id = message.from_user.id
    lang = "English" if message.text == "English" else "Russian"
    user_languages[user_id] = lang
    await message.answer(
        f"Language set to {message.text}!\nYou can now use /menu to view the menu." if lang == "English" else f"Язык установлен на {message.text}!\nТеперь вы можете использовать /menu для просмотра меню.",
        reply_markup=types.ReplyKeyboardRemove() 
    )

@telegram_dp.message(Command("menu"))
async def show_menu(message: types.Message):
    """Show the main menu with categories"""
    user_id = message.from_user.id
    lang = user_languages.get(user_id, "English")
    await message.answer(
        TRANSLATIONS[lang]["menu_title"],
        reply_markup=get_main_menu_keyboard(user_id),
        parse_mode="Markdown"
    )

@telegram_dp.message(Command("cart"))
async def show_cart(message: types.Message):
    """Show user's cart"""
    user_id = message.from_user.id
    lang = user_languages.get(user_id, "English")
    
    if user_id not in user_carts or not user_carts[user_id]:
        await message.answer(TRANSLATIONS[lang]["empty_cart"])
        return

    cart_text = TRANSLATIONS[lang]["cart_title"]
    total = 0
    for idx, item in enumerate(user_carts[user_id], 1):
        item_name = item['russian'] if lang == "Russian" else item['english']
        cart_text += f"{idx}. {item_name} - ${item['price']:.2f}\n"
        total += item['price']
    
    cart_text += f"\n*{TRANSLATIONS[lang]['total'].format(total)}*"
    
    await message.answer(
        cart_text,
        reply_markup=get_cart_keyboard(user_carts[user_id], user_id, is_modify_view=False),
        parse_mode="Markdown"
    )

@telegram_dp.callback_query()
async def handle_callback(callback: CallbackQuery):
    """Handle all callback queries"""
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "English")
    
    if callback.data == "back_to_menu":
        await callback.message.edit_text(
            TRANSLATIONS[lang]["menu_title"],
            reply_markup=get_main_menu_keyboard(user_id),
            parse_mode="Markdown"
        )
    
    elif callback.data.startswith("category_"):
        category = callback.data.split("_")[1]
        category_text = f"*{category}*\n\n"
        for item in MENU[category]:
            if lang == "Russian":
                category_text += f"*{item['russian']}* - ${item['price']:.2f}\n"
            else:
                category_text += f"*{item['english']}* - ${item['price']:.2f}\n"
        
        await callback.message.edit_text(
            category_text,
            reply_markup=get_category_keyboard(category, user_id),
            parse_mode="Markdown"
        )
    
    elif callback.data.startswith("a"):  # Handle add item callback
        try:
            item_id = int(callback.data[1:])  # Remove 'a' prefix and convert to int
            if item_id in menu_item_map:
                category, _ = menu_item_map[item_id]
                item = next((i for i in MENU[category] if i["id"] == item_id), None)
                
                if item:
                    # Initialize cart if it doesn't exist
                    if user_id not in user_carts:
                        user_carts[user_id] = []
                    
                    # Add item to cart
                    user_carts[user_id].append(item)
                    item_name = item['russian'] if lang == "Russian" else item['english']
                    await callback.answer(f"Added {item_name} to cart!")
        except ValueError:
            await callback.answer("Invalid item selection!")
    
    elif callback.data == "modify_cart":
        if user_id not in user_carts or not user_carts[user_id]:
            await callback.answer(TRANSLATIONS[lang]["empty_cart"])
            return
        
        cart_text = TRANSLATIONS[lang]["modify_cart_title"]
        total = 0
        for idx, item in enumerate(user_carts[user_id], 1):
            cart_text += f"{idx}. {item['english']} - ${item['price']:.2f}\n"
            total += item['price']
        
        cart_text += f"\n*{TRANSLATIONS[lang]['total'].format(total)}*\n\n"
        cart_text += TRANSLATIONS[lang]["select_items"]
        
        await callback.message.edit_text(
            cart_text,
            reply_markup=get_cart_keyboard(user_carts[user_id], user_id, is_modify_view=True),
            parse_mode="Markdown"
        )
    
    elif callback.data == "view_cart":
        if user_id not in user_carts or not user_carts[user_id]:
            await callback.answer(TRANSLATIONS[lang]["empty_cart"])
            return
        
        cart_text = TRANSLATIONS[lang]["cart_title"]
        total = 0
        for idx, item in enumerate(user_carts[user_id], 1):
            cart_text += f"{idx}. {item['english']} - ${item['price']:.2f}\n"
            total += item['price']
        
        cart_text += f"\n*{TRANSLATIONS[lang]['total'].format(total)}*"
        
        await callback.message.edit_text(
            cart_text,
            reply_markup=get_cart_keyboard(user_carts[user_id], user_id, is_modify_view=False),
            parse_mode="Markdown"
        )
    
    elif callback.data.startswith("remove_"):
        if user_id not in user_carts or not user_carts[user_id]:
            await callback.answer(TRANSLATIONS[lang]["empty_cart"])
            return
        
        # Get the index of the item to remove
        idx = int(callback.data.split("_")[1])
        if 0 <= idx < len(user_carts[user_id]):
            removed_item = user_carts[user_id].pop(idx)
            await callback.answer(f"Removed {removed_item['english']} from cart!")
            
            # Update cart display in modify view
            if user_carts[user_id]:  # If cart is not empty
                cart_text = TRANSLATIONS[lang]["modify_cart_title"]
                total = 0
                for idx, item in enumerate(user_carts[user_id], 1):
                    cart_text += f"{idx}. {item['english']} - ${item['price']:.2f}\n"
                    total += item['price']
                
                cart_text += f"\n*{TRANSLATIONS[lang]['total'].format(total)}*\n\n"
                cart_text += TRANSLATIONS[lang]["select_items"]
                
                await callback.message.edit_text(
                    cart_text,
                    reply_markup=get_cart_keyboard(user_carts[user_id], user_id, is_modify_view=True),
                    parse_mode="Markdown"
                )
            else:  # If cart is now empty
                await callback.message.edit_text(
                    TRANSLATIONS[lang]["cart_cleared"],
                    reply_markup=get_main_menu_keyboard(user_id)
                )
        else:
            await callback.answer("Invalid item index!")
    
    elif callback.data == "clear_cart":
        if user_id in user_carts:
            user_carts[user_id] = []
        await callback.message.edit_text(
            TRANSLATIONS[lang]["cart_cleared"],
            reply_markup=get_main_menu_keyboard(user_id)
        )
    
    elif callback.data == "place_order":
        if user_id not in user_carts or not user_carts[user_id]:
            await callback.answer(TRANSLATIONS[lang]["empty_cart"])
            return
        
        order_text = TRANSLATIONS[lang]["order_placed"]
        total = 0
        for idx, item in enumerate(user_carts[user_id], 1):
            order_text += f"{idx}. {item['english']} - ${item['price']:.2f}\n"
            total += item['price']
        
        order_text += f"\n*{TRANSLATIONS[lang]['total'].format(total)}*\n\n"
        order_text += TRANSLATIONS[lang]["thank_you"]
        
        user_carts[user_id] = []
        
        await callback.message.edit_text(
            order_text,
            reply_markup=get_main_menu_keyboard(user_id),
            parse_mode="Markdown"
        )

@telegram_dp.message(Command("help"))
async def help_command(message: types.Message):
    """Show help message"""
    user_id = message.from_user.id
    lang = user_languages.get(user_id, "English")
    await message.answer(TRANSLATIONS[lang]["help_text"], parse_mode="Markdown")

async def main():
    await telegram_dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())




