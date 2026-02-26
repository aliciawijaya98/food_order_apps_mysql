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

    add_order("Dine-in", current_user, table_num)

def takeaway(current_user):

    # Ask for invoice number and ensure it's a positive integer
    while True:
        try:
            invoice_num = int(input("Insert invoice number: "))
            if invoice_num <= 0:
                print("Table number must be greater than 0. Try again.")
                continue
            break
        except ValueError:
            print("Table number must be a number. Try again.")

    add_order("Takeaway", current_user, invoice_num)

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
            print("\n=== ORDER SUMMARY ===") 
            show_orders(order_id)              
            break
        
        # Validate item number
        if not (1 <= item_no <= len(menu_list)):
            print("Invalid selection. Try again.")
            continue

        # Input quantity for selected item
        item_selected = menu_list[item_no - 1]
        
        try:
            qty = int(input(f"Insert the quantity for {item_selected['item']}: "))
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

def show_orders(order_id):
    order_data = get_order_detail(order_id)

    if not order_data or not order_data["items"]:
        print("No orders found.")
        return
    
    order = order_data["order"]
    items = order_data["items"]
    
    # Display cashier who handled the order
    print(f"\nInvoice: {order['invoice_code']}")
    print(f"Cashier: {order['user_id']}")
    print(f"Order Type: {order['order_type']}")

    # Print order summary header
    print(f"=== ALL ORDER SUMMARY FOR {order_id}===")
    column_width = "{:<5} | {:<30} | {:<10} | {:<15} | {:<15}"
    header = column_width.format("No.", "Item", "Qty", "Price", "Total")
    print(header)
    print("-" * len(header))

    # Loop through each item in the order and display details
    grand_total = 0
    for idx, item in enumerate(items, start=1):
        price_format = f"Rp{int(item['price']):,}".replace(",", ".")
        subtotal_format = f"Rp{int(item['subtotal']):,}".replace(",", ".")
        print(column_width.format(
            idx,
            item['item'],
            item['quantity'],
            price_format,
            subtotal_format
        ))
        grand_total += item['subtotal']

    # Display the grand total for this order
    grand_total_format = f"Rp{int(grand_total):,}".replace(",", ".")
    print(f"\nGrand Total: {grand_total_format}")

if __name__ == "__main__":
    current_user = input("Enter cashier/user ID: ").strip()
    order_type(current_user)
