from aiogram.types import Message, CallbackQuery
from .base_handler import BaseHandler, user_order_state, user_order_data
from config.settings import ADMIN_CHAT_ID
from utils.translations import TRANSLATIONS

class OrderHandler(BaseHandler):
    def register_handlers(self):
        """Register all order-related handlers"""
        self.dp.message.register(
            self.order_process_handler,
            lambda m: m.from_user.id in user_order_state
        )
        self.dp.callback_query.register(
            self.handle_order_callback,
            lambda c: c.data == "place_order"
        )

    async def handle_order_callback(self, callback: CallbackQuery):
        """Handle order-related callback queries"""
        user_id = callback.from_user.id
        if callback.data == "place_order":
            cart = await self.get_user_cart(user_id)
            if not cart:
                lang = await self.get_user_language(user_id)
                await callback.answer(TRANSLATIONS[lang]["empty_cart"])
                return
            
            user_order_state[user_id] = "waiting_name"
            user_order_data[user_id] = {}
            await callback.message.answer("Please enter your full name:")

    async def order_process_handler(self, message: Message):
        """Handle the order process flow"""
        user_id = message.from_user.id
        if user_id not in user_order_state:
            return  # Not in order process

        state = user_order_state[user_id]
        text = message.text.strip()

        if state == "waiting_name":
            user_order_data[user_id]["name"] = text
            user_order_state[user_id] = "waiting_address"
            await message.answer("Please send your address as a Google Maps link (or type your address):")
        
        elif state == "waiting_address":
            user_order_data[user_id]["address"] = text
            user_order_state[user_id] = "waiting_desc"
            await message.answer("Please provide additional details (condo, floor, apartment, etc.):")
        
        elif state == "waiting_desc":
            user_order_data[user_id]["desc"] = text
            user_order_state[user_id] = "waiting_phone"
            await message.answer("Please enter your phone number (optional, or type 'skip'):")
        
        elif state == "waiting_phone":
            if text.lower() != "skip":
                user_order_data[user_id]["phone"] = text
            else:
                user_order_data[user_id]["phone"] = ""
            user_order_state[user_id] = "waiting_confirm"

            # Show order summary
            cart = await self.get_user_cart(user_id)
            total = await self.get_cart_total(user_id)
            cart_lines = "\n".join(
                f"{idx+1}. {item['english']} - ${item['price']:.2f}"
                for idx, item in enumerate(cart)
            )
            summary = (
                f"Order summary:\n"
                f"Name: {user_order_data[user_id]['name']}\n"
                f"Address: {user_order_data[user_id]['address']}\n"
                f"Details: {user_order_data[user_id]['desc']}\n"
                f"Phone: {user_order_data[user_id]['phone']}\n"
                f"Cart:\n{cart_lines}\n"
                f"Total: ${total:.2f}\n\n"
                "Is everything correct? (yes/no)"
            )
            await message.answer(summary)
        
        elif state == "waiting_confirm":
            if text.lower() in ["yes", "y", "да"]:
                # Prepare order summary for admin
                cart = await self.get_user_cart(user_id)
                total = await self.get_cart_total(user_id)
                cart_lines = "\n".join(
                    f"{idx+1}. {item['english']} - ${item['price']:.2f}"
                    for idx, item in enumerate(cart)
                )
                summary = (
                    f"New Order!\n"
                    f"User ID: {user_id}\n"
                    f"Name: {user_order_data[user_id]['name']}\n"
                    f"Address: {user_order_data[user_id]['address']}\n"
                    f"Details: {user_order_data[user_id]['desc']}\n"
                    f"Phone: {user_order_data[user_id]['phone']}\n"
                    f"Cart:\n{cart_lines}\n"
                    f"Total: ${total:.2f}"
                )
                # Send to admin
                await self.bot.send_message(ADMIN_CHAT_ID, summary)
                await message.answer("Thank you! Your order has been placed. We will contact you soon.")
                await self.clear_cart(user_id)
                user_order_state.pop(user_id)
                user_order_data.pop(user_id)
            else:
                await message.answer("Order cancelled. You can start again with /menu.")
                user_order_state.pop(user_id)
                user_order_data.pop(user_id) 