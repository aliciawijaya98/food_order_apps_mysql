from menu_database_mysql import get_menu
from order_database_mysql import create_order, add_order_item, get_order_detail

#ORDER MENU DISPLAY
def order_type(current_user):
    while True:
        print("\nSelect the order type:")
        print("1. Dine-in")
        print("2. Takeaway")
        print("3. Back to Order Menu")

        # Get user input and validate
        try:
            user_input = int(input("Choose between 1-3: "))
        except ValueError:
            print("Must be a number.")
            continue

        if user_input == 1:
            dine_in(current_user)
        elif user_input == 2:
            takeaway(current_user)
        elif user_input == 3:
            print("\nSession ended.")
            break
        else:
            print("Invalid option. Please choose 1-3.")

def dine_in(current_user):

    # Ask for table number and ensure it's a positive integer
    while True:
        try:
            table_num = int(input("Insert table number: "))
            if table_num <= 0:
                print("Table number must be greater than 0. Try again.")
                continue
            break
        except ValueError:
            print("Table number must be a number. Try again.")

    add_order("Dine-in", table_num, current_user)

def takeaway(current_user):

    # Ask for invoice number and ensure it's a positive integer
    while True:
        try:
            invoice_num = int(input("Insert table number: "))
            if invoice_num <= 0:
                print("Table number must be greater than 0. Try again.")
                continue
            break
        except ValueError:
            print("Table number must be a number. Try again.")

    add_order("Takeaway", invoice_num, current_user)

def add_order(order_type, current_user, identifier):

    # Fetch latest menu
    menu_list = get_menu()
    if not menu_list:
        print("Menu is empty.")
        return
    
    order_id, invoice_code = create_order(current_user, order_type, identifier)
    if not order_id:
        print(f"Failed to create order: {invoice_code}")
        return

    while True:

        # Display menu table header
        print("\n=== MENU ===")
        column_width = "{:<5} | {:<20} | {:<55} | {:<10}"
        header = column_width.format("No.", "Category", "Item" , "Price")
        print(header)
        print("-" * len(header))

        # Display the menu
        for i, item in enumerate(menu_list, start=1):
            price_format = f"Rp{item['price']:,}".replace(",",".")
            print(column_width.format(i, item["category"], item["item"], price_format))
        
        # Input item number
        try:
            item_no = int(input("\nSelect item number (0 to finish): "))
        except ValueError:
            print("Must be a number. Try again.")
            continue

        if item_no == 0:
            order_data = get_order_detail(order_id)
            if not order_data["order"]:
                print("No items ordered.")
                return
            print(f"\nInvoice: {order_data['order']['invoice_code']}")
            print("{:<5} | {:<30} | {:<10} | {:<15} | {:<15}".format("No", "Item", "Qty", "Price", "Subtotal"))
            print("-"*85)
            grand_total = 0
            for idx, it in enumerate(order_data['items'], 1):
                print("{:<5} | {:<30} | {:<10} | Rp{:<15,} | Rp{:<15,}".format(
                    idx, it['item'], it['quantity'], it['price'], it['subtotal']).replace(",", "."))
                grand_total += it['subtotal']
            print(f"\nGrand Total: Rp{grand_total:,}".replace(",", "."))
            break 
        
        # Validate item number
        if not (1 <= item_no <= len(menu_list)):
            print("Invalid selection. Try again.")
            continue

        # Input quantity for selected item
        item_selected = menu_list[item_no - 1]
        
        try:
            qty = int(input(f"Insert the quantity for {item['item']}: "))
            if qty <= 0:
                print("Quantity must be greater than 0. Try again.")
                continue
        except ValueError:
            print("Must be number. Try again.")
            continue
        
        # Store in order database
        success, msg = add_order_item(order_id, item_selected['id'], qty, item_selected['price'])
        if success:
            print(f"Added {qty} x {item_selected['item']}")
        else:
            print(f"Failed to add item: {msg}")


if __name__ == "__main__":
    current_user = input("Enter cashier/user ID: ").strip()
    order_type(current_user)
