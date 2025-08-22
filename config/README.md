# Restaurant Bot

A Telegram bot for restaurant ordering built with aiogram 3.x.

## Project Structure

```
rest_bot/
├── .env                    # Environment variables (secrets)
├── .gitignore             # Git ignore rules
├── main.py                # Main bot entry point
├── requirements.txt       # Python dependencies
├── pytest.ini            # Pytest configuration
├── README.md              # This file
├── assets/                # Static assets (images, menu files)
│   └── images/           # Menu images
├── config/                # Configuration files
│   ├── __init__.py
│   ├── settings.py        # Bot settings and constants
│   └── logging_config.py  # Logging configuration
├── handlers/              # Bot logic handlers
│   ├── __init__.py
│   ├── base_handler.py    # Base handler class
│   ├── cart_handler.py    # Cart management
│   ├── menu_handler.py    # Menu display and navigation
│   └── order_handler.py   # Order processing
├── keyboards/             # Inline keyboard layouts
│   ├── __init__.py
│   ├── cart_keyboards.py  # Cart interaction keyboards
│   └── menu_keyboards.py  # Menu navigation keyboards
├── models/                # Data models
│   ├── __init__.py
│   └── menu.py           # Menu data management
├── tests/                 # Test files
│   ├── __init__.py
│   └── test_handlers.py  # Handler tests
└── utils/                 # Utility functions
    ├── __init__.py
    └── translations.py    # Multi-language support
```

## Features

- **Multi-language Support**: English and Russian
- **Menu Navigation**: Hierarchical menu with categories and subcategories
- **Shopping Cart**: Add/remove items, modify quantities
- **Order Processing**: Complete order flow with user details
- **Admin Notifications**: Orders sent to admin chat
- **Comprehensive Logging**: File and console logging with rotation

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd rest_bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your bot token and admin chat ID
   ```

4. **Run the bot**
   ```bash
   python main.py
   ```

## Environment Variables

Create a `.env` file with:
```env
BOT_TOKEN=your_bot_token_here
ADMIN_CHAT_ID=your_admin_chat_id_here
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
```

## Testing

Run tests with pytest:
```bash
pytest
```

## Logging

Logs are stored in the `logs/` directory with automatic rotation:
- Console output for development
- File logging with 10MB rotation
- Configurable log levels via environment

## Contributing

1. Follow the existing code structure
2. Add tests for new functionality
3. Update documentation as needed
4. Use proper logging for debugging

## License

[Your License Here]
