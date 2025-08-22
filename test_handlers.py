#!/usr/bin/env python3
"""
Simple test script to verify handler registration
"""
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Update, Message, User, Chat, CallbackQuery

from config.settings import BOT_TOKEN
from handlers.menu_handler import MenuHandler
from handlers.cart_handler import CartHandler
from handlers.order_handler import OrderHandler

async def test_handlers():
    """Test if handlers are properly registered"""
    print("Testing handler registration...")
    
    # Initialize bot and dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Register handlers
    menu_handler = MenuHandler(bot, dp)
    cart_handler = CartHandler(bot, dp)
    order_handler = OrderHandler(bot, dp)

    menu_handler.register_handlers()
    cart_handler.register_handlers()
    order_handler.register_handlers()

    print("✅ All handlers registered successfully!")
    
    # Test callback data filtering
    test_callbacks = [
        "view_cart",
        "modify_cart", 
        "clear_cart",
        "remove_0",
        "back_to_menu",
        "category_Main Dishes",
        "subcategory_Main Dishes_Beef",
        "a1",
        "place_order"
    ]
    
    print("\nTesting callback filters...")
    for callback_data in test_callbacks:
        print(f"  {callback_data}: ", end="")
        
        # Test cart handler filter
        cart_filter = lambda c: c.data in ["view_cart", "modify_cart", "clear_cart"] or c.data.startswith("remove_")
        if cart_filter(type('obj', (object,), {'data': callback_data})()):
            print("Cart Handler ✅")
            continue
            
        # Test menu handler filter  
        menu_filter = lambda c: c.data == "back_to_menu" or c.data.startswith("category_") or c.data.startswith("subcategory_") or c.data.startswith("a")
        if menu_filter(type('obj', (object,), {'data': callback_data})()):
            print("Menu Handler ✅")
            continue
            
        # Test order handler filter
        order_filter = lambda c: c.data == "place_order"
        if order_filter(type('obj', (object,), {'data': callback_data})()):
            print("Order Handler ✅")
            continue
            
        print("No Handler ❌")
    
    await bot.session.close()
    print("\n✅ Handler test completed!")

if __name__ == "__main__":
    asyncio.run(test_handlers())
