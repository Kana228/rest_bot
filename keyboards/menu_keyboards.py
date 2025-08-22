from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config.settings import CATEGORY_EMOJI_MAP, SUBCATEGORY_EMOJI
from models.menu import menu_manager
from utils.translations import TRANSLATIONS

def get_main_menu_keyboard(user_id: int, user_languages: dict) -> InlineKeyboardMarkup:
    """Create main menu keyboard with categories"""
    keyboard = []
    lang = user_languages.get(user_id, "English")
    categories = list(menu_manager.menu.keys())

    for i in range(0, len(categories), 2):
        row = []
        for category in categories[i:i+2]:
            emoji = CATEGORY_EMOJI_MAP.get(category, "")
            row.append(InlineKeyboardButton(
                text=f"{emoji} {category}",
                callback_data=f"category_{category}"
            ))
        keyboard.append(row)
    
    keyboard.append([
        InlineKeyboardButton(
            text=TRANSLATIONS[lang]["view_cart"],
            callback_data="view_cart"
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_category_keyboard(category: str, user_id: int, user_languages: dict) -> InlineKeyboardMarkup:
    """Create keyboard for subcategories of any category"""
    keyboard = []
    lang = user_languages.get(user_id, "English")
    subcategories = list(menu_manager.menu[category].keys())

    for i in range(0, len(subcategories), 2):
        row = []
        for subcat in subcategories[i:i+2]:
            emoji = SUBCATEGORY_EMOJI.get(subcat, "")
            row.append(InlineKeyboardButton(
                text=f"{emoji} {subcat}",
                callback_data=f"subcategory_{category}_{subcat}"
            ))
        keyboard.append(row)
    
    keyboard.append([
        InlineKeyboardButton(
            text=TRANSLATIONS[lang]["back_to_menu"],
            callback_data="back_to_menu"
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_subcategory_keyboard(category: str, subcategory: str, user_id: int, user_languages: dict) -> InlineKeyboardMarkup:
    """Create keyboard for items in a subcategory"""
    keyboard = []
    lang = user_languages.get(user_id, "English")
    items = menu_manager.menu[category][subcategory]

    for item in items:
        if lang == "Russian":
            button_text = f"{item['russian']} - ${item['price']:.2f}"
        else:
            button_text = f"{item['english']} - ${item['price']:.2f}"
        keyboard.append([
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"a{item['id']}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton(text="🔙 Back", callback_data=f"category_{category}"),
        InlineKeyboardButton(text="🏠 Home", callback_data="back_to_menu")
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard) 