#Initial menu data
food_menu = [
    {"category": "Appetizers", "item": "Spring Rolls", "price": 30000},
    {"category": "Appetizers", "item": "Garlic Bread", "price": 25000},
    {"category": "Appetizers", "item": "Chicken Wings", "price": 40000},

    {"category": "Main Courses", "item": "Grilled Chicken with Rice", "price": 65000},
    {"category": "Main Courses", "item": "Beef Steak", "price": 120000},
    {"category": "Main Courses", "item": "Fried Rice", "price": 45000},
    
    {"category": "Drinks", "item": "Mineral Water", "price": 10000},
    {"category": "Drinks", "item": "Iced Tea", "price": 15000},
    {"category": "Drinks", "item": "Coffee", "price": 20000},

    {"category": "Desserts", "item": "Ice Cream", "price": 20000},
    {"category": "Desserts", "item": "Chocolate Cake", "price": 30000},
    {"category": "Desserts", "item": "Vanilla Panna Cotta", "price": 40000},
]
#Return the lastest menu
def get_menu():
    return food_menu

#Add a new item to the menu
def add_menu_item(new_item):
    if "category" in new_item and \
        "item" in new_item and \
        "price" in new_item:
        food_menu.append(new_item)
