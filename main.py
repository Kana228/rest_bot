import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config.settings import BOT_TOKEN
from config.logging_config import setup_logging
from handlers.menu_handler import MenuHandler
from handlers.cart_handler import CartHandler
from handlers.order_handler import OrderHandler
from utils.translations import TRANSLATIONS

async def help_command(message: Message):
    """Show help message"""
    user_id = message.from_user.id
    lang = await MenuHandler.get_user_language(user_id)
    await message.answer(TRANSLATIONS[lang]["help_text"], parse_mode="Markdown")

async def contacts(message: Message):
    """Show contact information"""
    await message.answer(
        "Working hours: 16:00 - 23:00\n\n"
        "Contacts: +66974165008 \n"
        "Our location: https://maps.app.goo.gl/PodwxLKnwSNQzAuCA \n"
        "Instagram: https://www.instagram.com/theqazaqs"
    )

async def main():
    # Setup logging
    logger = setup_logging()
    
    # Initialize bot and dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Register handlers
    logger.info("Registering bot handlers...")
    menu_handler = MenuHandler(bot, dp)
    cart_handler = CartHandler(bot, dp)
    order_handler = OrderHandler(bot, dp)

    menu_handler.register_handlers()
    cart_handler.register_handlers()
    order_handler.register_handlers()
    logger.info("All handlers registered successfully")

    # Register additional commands
    dp.message.register(help_command, Command("help"))
    dp.message.register(contacts, Command("contacts"))

    # Start polling
    logger.info("Starting bot polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

