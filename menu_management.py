from menu_database import get_menu, add_menu_item, food_menu

# View the menu
def view_menu(menu_to_show, allow_edit=False):
    # Print table header
    column_width = "{:<5} | {:<20} | {:<55} | {:<10}"
    header = column_width.format("No.", "Category", "Item" , "Price")
    print(header)
    print("-" * len(header))

    # Print each menu item in formatted table
    for i, item in enumerate(menu_to_show, start=1):
        price_format = f"Rp{item['price']:,}".replace(",",".")
        print(column_width.format(i, item["category"], item["item"], price_format))

    # User can edit/delete items in the menu directly right after the menu is displayed
    if allow_edit:
        while True:
            edit_choice = input("Do you want to edit/delete an item? (y/n): ").strip()
            if edit_choice == "y":
                edit_delete_item(menu_to_show)
                break
            elif edit_choice == "n":
                break
            else: 
                print("Please type 'y' or 'n'")


# Search the menu
def search_menu(menu_to_show):
    while True:
        # Ask user for search query
        query = input("Search by category or item (or type 'q' to quit): ").strip().lower()
        
        if query == "q":
            print ("Exiting search...")
            break 

        # Filter menu items that match query
        filtered = [item for item in menu_to_show 
                    if query in item["category"].lower() 
                    or query in item["item"].lower()] 
    
        if filtered:
            print(f"\nFound {len(filtered)} item(s) matching '{query}':")

            # Show filtered menu
            view_menu(filtered)

            # Ask if user wants to edit/delete filtered items
            edit_choice = input("Do you want to edit/delete these items? (y/n): ").strip().lower()
            if edit_choice == "y":
                edit_delete_item(filtered)
                break
            elif edit_choice == "n":
                break
            else: 
                print("Please type 'y' or 'n'")
        else:
            print(f"No items found matching '{query}'. Try again.")

# Edit or delete item
def edit_delete_item(menu_to_show):

    # Return if menu is empty
    if not menu_to_show:
        print("No items available to edit/delete.")
        return
    
    # Show menu
    view_menu(menu_to_show)

    # Ask for index of item to edit/delete
    delete_index = input("Enter the index of the item to edit/delete (or 'q' to quit): ").strip()
    if delete_index.lower() == "q":
        return
    elif not delete_index.isdigit() or int(delete_index) < 1 or int(delete_index) >  len(menu_to_show):
        print("Invalid index.")
        return

    selected_item = menu_to_show[int(delete_index) - 1]
    print(f"Selected: {selected_item['item']}")

    # Ask whether to edit or delete
    edit_choice = input("Type 'e' to edit, 'd' to delete: ").strip().lower()

    if edit_choice == "e":
        # Prompt new category/name; Enter keeps old value
        new_category = input(f"New category (Enter to keep '{selected_item['category']}'): ").strip()
        new_name = input(f"New item name (Enter to keep '{selected_item['item']}'): ").strip()
        
        # Loop until a valid price is entered
        while True:
            new_price = input(f"New price (Enter to keep '{selected_item['price']}'): ").strip()
            
            # Keep old price if Enter pressed
            if not new_price:
                break
            
            try:
                new_price_int = int(new_price)

                # Reject negative price
                if new_price_int < 0:
                    print("Price can't be negative. Try again.")
                    continue

                # Update price
                selected_item["price"] = new_price_int
                break
            except ValueError:
                print("Invalid price. Keeping old value.")

        # Update category and name
        if new_category:
            selected_item["category"] = new_category
        if new_name:
            selected_item["item"] = new_name

        print("Item updated successfully!")

    elif edit_choice == "d":
        
        # Confirm deletion
        confirm = input(
            f"Are you sure you want to delete '{selected_item['item']}'? (y/n): "
        ).strip().lower()

        if confirm == "y":
            try:
                food_menu.remove(selected_item)
                print("Item deleted successfully!")
            except ValueError:
                print("Item not found in main menu.")

#Add item
def add_item():

    # Prompt for category
    category = input("Enter category: ").strip().title()

    # Prompt for item name and check duplicates
    while True:
        item_name = input("Enter item name: ").strip().title()

        # Check duplicates
        if any(item["item"] == item_name for item in food_menu):
            print(f"Item '{item_name}' already exists. Try another name.")
            continue
        break
    
    # Prompt for price, ensure integer and non-negative
    while True:
        try:
            price = int(input("Enter price: ").strip())
            if price < 0:
                print("Price can't be negative. Try again.")
                continue
            break
        except ValueError:
            print("Price must be a number.")

    # Add new item to menu
    add_menu_item({
        "category": category,
        "item": item_name,
        "price": price
    })

    print("Item added successfully!")


if __name__ == "__main__":
    # Show full menu and allow edits
    view_menu(get_menu(), allow_edit=True)

    # Allow user to search menu and edit/delete items
    search_menu(get_menu())
