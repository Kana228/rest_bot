from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from typing import Dict, List

# Global state storage
user_carts: Dict[int, List[dict]] = {}
user_languages: Dict[int, str] = {}
user_order_state: Dict[int, str] = {}
user_order_data: Dict[int, dict] = {}

class BaseHandler:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp

    def register_handlers(self):
        """Register all handlers for this module"""
        raise NotImplementedError("Subclasses must implement register_handlers()")

    async def get_user_language(self, user_id: int) -> str:
        """Get user's language preference"""
        return user_languages.get(user_id, "English")

    async def get_user_cart(self, user_id: int) -> List[dict]:
        """Get user's cart"""
        return user_carts.get(user_id, [])

    async def add_to_cart(self, user_id: int, item: dict):
        """Add item to user's cart"""
        if user_id not in user_carts:
            user_carts[user_id] = []
        user_carts[user_id].append(item)

    async def remove_from_cart(self, user_id: int, index: int) -> dict:
        """Remove item from user's cart"""
        if user_id in user_carts and 0 <= index < len(user_carts[user_id]):
            return user_carts[user_id].pop(index)
        return None

    async def clear_cart(self, user_id: int):
        """Clear user's cart"""
        if user_id in user_carts:
            user_carts[user_id] = []

    async def get_cart_total(self, user_id: int) -> float:
        """Calculate total price of items in cart"""
        cart = await self.get_user_cart(user_id)
        return sum(item['price'] for item in cart) 