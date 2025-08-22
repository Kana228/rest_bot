from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.translations import TRANSLATIONS

def get_cart_keyboard(cart_items: list, user_id: int, user_languages: dict, is_modify_view: bool = False) -> InlineKeyboardMarkup:
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
            [InlineKeyboardButton(
                text=TRANSLATIONS[lang]["clear_all"],
                callback_data="clear_cart"
            )],
            [InlineKeyboardButton(
                text=TRANSLATIONS[lang]["back_to_cart"],
                callback_data="view_cart"
            )]
        ])
    else:
        keyboard.extend([
            [InlineKeyboardButton(
                text=TRANSLATIONS[lang]["modify_cart"],
                callback_data="modify_cart"
            )],
            [InlineKeyboardButton(
                text=TRANSLATIONS[lang]["back_to_menu"],
                callback_data="back_to_menu"
            )],
            [InlineKeyboardButton(
                text=TRANSLATIONS[lang]["place_order"],
                callback_data="place_order"
            )]
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard) 