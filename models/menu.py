import pandas as pd
from typing import Dict, Tuple
from config.settings import MENU_EXCEL_PATH

class MenuManager:
    def __init__(self):
        self.menu = {}
        self.menu_item_map = {}  # {category_item_id: (category, item_name, subcategory)}
        self.menu_item_counter = 0
        self.load_menu()

    def load_menu(self, file_path: str = MENU_EXCEL_PATH) -> Dict:
        """Load menu from Excel file and convert to nested dictionary format"""
        try:
            df = pd.read_excel(file_path)
            self.menu.clear()
            self.menu_item_map.clear()
            self.menu_item_counter = 0

            # Group by category and subcategory
            for category, group in df.groupby('Category'):
                self.menu[category] = {}
                for subcategory, sub_group in group.groupby('Subcategory_eng'):
                    self.menu[category][subcategory] = []
                    for _, row in sub_group.iterrows():
                        item = {
                            "english": row['English'],
                            "russian": row['Russian'],
                            "price": float(row['Price']),
                            "id": self.menu_item_counter,
                            "subcategory": subcategory
                        }
                        self.menu[category][subcategory].append(item)
                        self.menu_item_map[self.menu_item_counter] = (
                            category,
                            row['English'],
                            subcategory
                        )
                        self.menu_item_counter += 1
            return self.menu
        except Exception as e:
            print(f"Error loading menu: {e}")
            return {
                "Error": [{
                    "english": "Menu unavailable",
                    "russian": "Меню недоступно",
                    "price": 0.00,
                    "id": 0
                }]
            }

    def get_item_by_id(self, item_id: int) -> Tuple[str, dict, str]:
        """Get menu item details by its ID"""
        if item_id in self.menu_item_map:
            category, _, subcategory = self.menu_item_map[item_id]
            item = next(
                (i for i in self.menu[category][subcategory] if i["id"] == item_id),
                None
            )
            return category, item, subcategory
        return None, None, None

# Create a singleton instance
menu_manager = MenuManager() 