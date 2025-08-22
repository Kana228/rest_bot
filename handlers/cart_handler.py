from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from .base_handler import BaseHandler, user_languages
from keyboards.cart_keyboards import get_cart_keyboard
from keyboards.menu_keyboards import get_main_menu_keyboard
from utils.translations import TRANSLATIONS

class CartHandler(BaseHandler):
    def register_handlers(self):
        """Register all cart-related handlers"""
        self.dp.message.register(self.show_cart, Command("cart"))
        self.dp.callback_query.register(
            self.handle_cart_callback,
            lambda c: c.data in ["view_cart", "modify_cart", "clear_cart"] or c.data.startswith("remove_")
        )

    async def show_cart(self, message: Message):
        """Show user's cart"""
        user_id = message.from_user.id
        lang = await self.get_user_language(user_id)
        cart = await self.get_user_cart(user_id)
        
        if not cart:
            await message.answer(TRANSLATIONS[lang]["empty_cart"])
            return

        cart_text = TRANSLATIONS[lang]["cart_title"]
        total = await self.get_cart_total(user_id)
        
        for idx, item in enumerate(cart, 1):
            item_name = item['russian'] if lang == "Russian" else item['english']
            cart_text += f"{idx}. {item_name} - ${item['price']:.2f}\n"
        
        cart_text += f"\n*{TRANSLATIONS[lang]['total'].format(total)}*"
        
        await message.answer(
            cart_text,
            reply_markup=get_cart_keyboard(cart, user_id, user_languages, is_modify_view=False),
            parse_mode="Markdown"
        )

    async def handle_cart_callback(self, callback: CallbackQuery):
        """Handle all cart-related callback queries"""
        user_id = callback.from_user.id
        lang = await self.get_user_language(user_id)
        cart = await self.get_user_cart(user_id)

        if callback.data == "view_cart":
            if not cart:
                await callback.answer(TRANSLATIONS[lang]["empty_cart"])
                return
            
            cart_text = TRANSLATIONS[lang]["cart_title"]
            total = await self.get_cart_total(user_id)
            
            for idx, item in enumerate(cart, 1):
                item_name = item['russian'] if lang == "Russian" else item['english']
                cart_text += f"{idx}. {item_name} - ${item['price']:.2f}\n"
            
            cart_text += f"\n*{TRANSLATIONS[lang]['total'].format(total)}*"
            
            await callback.message.edit_text(
                cart_text,
                reply_markup=get_cart_keyboard(cart, user_id, user_languages, is_modify_view=False),
                parse_mode="Markdown"
            )

        elif callback.data == "modify_cart":
            if not cart:
                await callback.answer(TRANSLATIONS[lang]["empty_cart"])
                return
            
            cart_text = TRANSLATIONS[lang]["modify_cart_title"]
            total = await self.get_cart_total(user_id)
            
            for idx, item in enumerate(cart, 1):
                cart_text += f"{idx}. {item['english']} - ${item['price']:.2f}\n"
            
            cart_text += f"\n*{TRANSLATIONS[lang]['total'].format(total)}*\n\n"
            cart_text += TRANSLATIONS[lang]["select_items"]
            
            await callback.message.edit_text(
                cart_text,
                reply_markup=get_cart_keyboard(cart, user_id, user_languages, is_modify_view=True),
                parse_mode="Markdown"
            )

        elif callback.data.startswith("remove_"):
            if not cart:
                await callback.answer(TRANSLATIONS[lang]["empty_cart"])
                return
            
            idx = int(callback.data.split("_")[1])
            removed_item = await self.remove_from_cart(user_id, idx)
            
            if removed_item:
                await callback.answer(f"Removed {removed_item['english']} from cart!")
                
                if cart:  # If cart is not empty
                    cart_text = TRANSLATIONS[lang]["modify_cart_title"]
                    total = await self.get_cart_total(user_id)
                    
                    for idx, item in enumerate(cart, 1):
                        cart_text += f"{idx}. {item['english']} - ${item['price']:.2f}\n"
                    
                    cart_text += f"\n*{TRANSLATIONS[lang]['total'].format(total)}*\n\n"
                    cart_text += TRANSLATIONS[lang]["select_items"]
                    
                    await callback.message.edit_text(
                        cart_text,
                        reply_markup=get_cart_keyboard(cart, user_id, user_languages, is_modify_view=True),
                        parse_mode="Markdown"
                    )
                else:  # If cart is now empty
                    await callback.message.edit_text(
                        TRANSLATIONS[lang]["cart_cleared"],
                        reply_markup=get_main_menu_keyboard(user_id, user_languages)
                    )
            else:
                await callback.answer("Invalid item index!")

        elif callback.data == "clear_cart":
            await self.clear_cart(user_id)
            await callback.message.edit_text(
                TRANSLATIONS[lang]["cart_cleared"],
                reply_markup=get_main_menu_keyboard(user_id, user_languages)
            ) 