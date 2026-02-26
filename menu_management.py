from menu_database_mysql import (
    get_menu, 
    add_menu_item, 
    update_menu_item,
    delete_menu_item
)

# View the menu

def view_menu(menu_to_show=None, allow_edit=False):
    
    if menu_to_show is None:
        menu_to_show = get_menu()
    
    if not menu_to_show:
        print ("Menu is empty.")
        return
    
    # Print table header
    column_width = "{:<5} | {:<20} | {:<55} | {:<10}"
    header = column_width.format("ID", "Category", "Item" , "Price")
    print(header)
    print("-" * len(header))

    # Print each menu item in formatted table
    for item in menu_to_show:
        price_format = f"Rp{item['price']:,}".replace(",",".")
        print(column_width.format(item["id"], item["category"], item["item"], price_format))

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
def search_menu():
    
    while True:
        menu_to_show = get_menu()
        
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
    menu_id_input = input("Enter the ID of the item to edit/delete (or 'q' to quit): ").strip()
    if menu_id_input.lower() == "q":
        return
    elif not menu_id_input.isdigit():
        print("Invalid ID.")
        return

    menu_id = int(menu_id_input)
    
    selected_item = next(
        (item for item in menu_to_show if item["id"] == menu_id),
        None
    )

    if not selected_item:
        print("Item not found.")
        return
    
    # Ask whether to edit or delete
    edit_choice = input("Type 'e' to edit, 'd' to delete: ").strip().lower()

    if edit_choice == "e":
        # Prompt new category/name; Enter keeps old value
        new_category = input(f"New category (Enter to keep '{selected_item['category']}'): ").strip()
        new_name = input(f"New item name (Enter to keep '{selected_item['item']}'): ").strip()
        
        # Loop until a valid price is entered
        while True:
            new_price_input = input(f"New price (Enter to keep '{selected_item['price']}'): ").strip()
            
            # Keep old price if Enter pressed
            if not new_price_input:
                new_price_final = selected_item ["price"]
                break
            
            try:
                new_price_int = int(new_price_input)

                # Reject negative price
                if new_price_int < 0:
                    print("Price can't be negative. Try again.")
                    continue
                new_price_final = new_price_int
                break
            except ValueError:
                print("Invalid price. Keeping old value.")
                
        #Keep old Values if empty
        category_final = new_category if new_category else selected_item["category"]
        name_final = new_name if new_name else selected_item["item"]         

        # Update category and name
        success, message = update_menu_item(
            selected_item["id"],
            category_final,
            name_final,
            new_price_final
        )

        print(message)
        
        if success:
            view_menu()

    elif edit_choice == "d":
        
        # Confirm deletion
        confirm = input(
            f"Are you sure you want to delete '{selected_item['item']}'? (y/n): "
        ).strip().lower()

        if confirm == "y":
            try:
                success, message = delete_menu_item(selected_item["id"])
                print(message)

                if success:
                    view_menu()
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
        menu_list = get_menu()
        if any(item["item"] == item_name for item in menu_list):
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
    success, message = add_menu_item({
    "category": category,
    "item": item_name,
    "price": price
    })

    print(message)

    if success:
        view_menu()


if __name__ == "__main__":
    # Show full menu and allow edits
    view_menu(allow_edit=True)
    search_menu()