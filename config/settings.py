import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot settings
BOT_TOKEN = os.getenv("MY_API_KEY")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

# File paths
MENU_EXCEL_PATH = "~/Desktop/git_proj/rest_bot/menu/menu.xlsx"

# Order states
ORDER_STATES = [
    "waiting_name",
    "waiting_address",
    "waiting_desc",
    "waiting_phone",
    "waiting_confirm"
]

# Menu categories and their emojis
CATEGORY_EMOJI_MAP = {
    "Central Asian Food": "🍢",
    "Slavic Food": "🥟",
    "Thai Food": "🍛",
    "Fast Food": "🍔",
    "Dessert": "🍨"
}

# Subcategory emojis
SUBCATEGORY_EMOJI = {
    "Grilled & Fried Meats": "🥩",
    "Noodles & Pasta": "🍜",
    "Soups": "🍲",
    "Dumplings & Stuffed": "🥟",
    "Salads & Cold Dishes": "🥗",
    "Seafood Specialties": "🐟",
    "Curries & Stir-Fries": "🍛",
    "Rice Dishes": "🍚",
    "Burgers & Sandwiches": "🍔",
    "Fast Food Sides": "🍟",
    "Desserts": "🍰"
} 