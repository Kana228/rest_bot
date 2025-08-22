from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove
from .base_handler import BaseHandler, user_languages
from keyboards.menu_keyboards import (
    get_main_menu_keyboard,
    get_category_keyboard,
    get_subcategory_keyboard
)
from utils.translations import TRANSLATIONS
from models.menu import menu_manager

class MenuHandler(BaseHandler):
    def register_handlers(self):
        """Register all menu-related handlers"""
        self.dp.message.register(self.start_command, Command("start"))
        self.dp.message.register(self.set_language, lambda m: m.text in ["English", "Русский"])
        self.dp.message.register(self.show_menu, Command("menu"))
        self.dp.callback_query.register(
            self.handle_menu_callback,
            lambda c: c.data == "back_to_menu" or c.data.startswith("category_") or c.data.startswith("subcategory_") or c.data.startswith("a")
        )

    async def start_command(self, message: Message):
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

    async def set_language(self, message: Message):
        """Set user's language preference"""
        user_id = message.from_user.id
        lang = "English" if message.text == "English" else "Russian"
        user_languages[user_id] = lang
        await message.answer(
            f"Language set to {message.text}!\nYou can now use /menu to view the menu." if lang == "English"
            else f"Язык установлен на {message.text}!\nТеперь вы можете использовать /menu для просмотра меню.",
            reply_markup=ReplyKeyboardRemove()
        )

    async def show_menu(self, message: Message):
        """Show the main menu with categories"""
        user_id = message.from_user.id
        lang = await self.get_user_language(user_id)
        await message.answer(
            TRANSLATIONS[lang]["menu_title"],
            reply_markup=get_main_menu_keyboard(user_id, user_languages),
            parse_mode="Markdown"
        )

    async def handle_menu_callback(self, callback: CallbackQuery):
        """Handle all menu-related callback queries"""
        user_id = callback.from_user.id
        lang = await self.get_user_language(user_id)

        if callback.data == "back_to_menu":
            await callback.message.edit_text(
                TRANSLATIONS[lang]["menu_title"],
                reply_markup=get_main_menu_keyboard(user_id, user_languages),
                parse_mode="Markdown"
            )
        elif callback.data.startswith("category_"):
            category = callback.data.split("_", 1)[1]
            await callback.message.edit_text(
                f"*{category}*",
                reply_markup=get_category_keyboard(category, user_id, user_languages),
                parse_mode="Markdown"
            )
        elif callback.data.startswith("subcategory_"):
            _, category, subcategory = callback.data.split("_", 2)
            await callback.message.edit_text(
                f"*{category} - {subcategory}*",
                reply_markup=get_subcategory_keyboard(category, subcategory, user_id, user_languages),
                parse_mode="Markdown"
            )
        elif callback.data.startswith("a"):  # Handle add item callback
            try:
                item_id = int(callback.data[1:])
                category, item, subcategory = menu_manager.get_item_by_id(item_id)
                if item:
                    await self.add_to_cart(user_id, item)
                    item_name = item['russian'] if lang == "Russian" else item['english']
                    await callback.answer(f"Added {item_name} to cart!")
            except Exception:
                await callback.answer("Invalid item selection!") 