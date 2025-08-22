# Restaurant Telegram Bot

A Telegram bot for restaurant ordering system that supports multiple languages (English and Russian) and provides a menu-based ordering experience.

## Features

- Multi-language support (English and Russian)
- Interactive menu with categories and subcategories
- Shopping cart functionality
- Order placement system
- Admin notifications for new orders
- Excel-based menu management

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with the following variables:
   ```
   MY_API_KEY=your_telegram_bot_token
   ADMIN_CHAT_ID=your_admin_chat_id
   ```
5. Place your menu Excel file in the `menu/` directory
6. Run the bot:
   ```bash
   python main.py
   ```

## Project Structure

```
rest_bot/
├── config/         # Configuration settings
├── handlers/       # Message and callback handlers
├── keyboards/      # Keyboard markup generators
├── models/         # Data models
├── utils/          # Utilities and constants
└── main.py         # Application entry point
```

## Menu Excel Format

The menu should be provided in an Excel file with the following columns:
- Category
- Subcategory_eng
- English (item name in English)
- Russian (item name in Russian)
- Price

## Contributing

Feel free to submit issues and enhancement requests!
