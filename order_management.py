from menu_database import get_menu

# Dictionary to store orders by table or invoice (only the lastest order will be stored)
orders = {}

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

    # If table has existing order, show it
    if table_num in orders:
        print("Existing order found:")
        show_orders(table_num)

    print(f"Dine-in selected. Table number: {table_num}")
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

    # If invoice has existing order, show it
    if invoice_num in orders:
        print("Existing order found:")
        show_orders(invoice_num)
        
    print(f"Takeaway selected. Invoice number: {invoice_num}")
    add_order("Takeaway", invoice_num, current_user)

def add_order(order_type, table_num=None, invoice_num=None, current_user=None):

    # Fetch latest menu
    current_menu = get_menu()

    # Temporary list to store this order session
    current_order = []

    # Determine the identifier for this order
    order_id = table_num if order_type == "Dine-in" else invoice_num

    while True:

        # Display menu table header
        print("\n=== MENU ===")
        column_width = "{:<5} | {:<20} | {:<55} | {:<10}"
        header = column_width.format("No.", "Category", "Item" , "Price")
        print(header)
        print("-" * len(header))

        # Display the menu
        for i, item in enumerate(current_menu, start=1):
            price_format = f"Rp{item['price']:,}".replace(",",".")
            print(column_width.format(i, item["category"], item["item"], price_format))
        
        # Display current order
        if current_order:
            print("\nCurrent Order:")
            for i, order in enumerate(current_order, start=1):
                print(f"{i}. {order['quantity']} x {order['item']} = Rp{order['total']:,}".replace(",", "."))

            # Option to delete an item from current order
            while True:
                delete_input = input("Type 'd' to delete an item, or Enter to continue: ").strip().lower()
                if delete_input in ["d", ""]:
                    break
                print("Invalid input. Type 'd' or press Enter to continue.")
            
            if delete_input == "d":
                try:
                    del_index = int(input("Which item number to delete? "))
                    if 1 <= del_index <= len(current_order):
                        removed_item = current_order.pop(del_index - 1)
                        print(f"Removed {removed_item['item']} from order")
                    else:
                        print("Invalid item number")
                except ValueError:
                    print("Must be a number")
                continue  # back to taking order

        # Input item number
        try:
            user_input = int(input("\nSelect item number (type '0' to finish): "))
        except ValueError:
            print("Must be a number. Try again.")
            continue

        if user_input == 0:
            if not current_order:
                print("No items ordered")
            else:
                #Save to order dictionary
                if order_type == "Dine-in":
                    print(f"Finish ordering. Table {order_id}")
                else:
                    print(f"Finish ordering. Invoice {order_id}")
                
                # If there is an existing order, merge items
                if order_id in orders:
                    orders[order_id]["items"].extend(current_order)
                    orders[order_id]["cashier"] = current_user
                else:
                    orders[order_id] = {
                        "cashier": current_user,
                        "items": current_order
                    }
                
                #Display the final order summary
                show_orders(order_id)
            break 
        
        # Validate item number
        elif not (1 <= user_input <= len(current_menu)):
            print("Invalid input. Try again")
            continue

        # Input quantity for selected item
        item = current_menu[user_input - 1]
        
        try:
            qty = int(input(f"Insert the quantity for {item['item']}: "))
            if qty <= 0:
                print("Quantity must be greater than 0. Try again.")
                continue
        except ValueError:
            print("Must be number. Try again.")
            continue
        
        # Store the order item in temporary list
        order_item = {
            "order_type": order_type,
            "order_id": order_id,
            "category": item['category'],
            "item": item['item'],
            "price": item['price'],
            "quantity": qty,
            "total": item['price'] * qty
        }

        current_order.append(order_item)

def show_orders(order_id):

    # Check if there is any order for the given order_id
    if order_id not in orders or not orders[order_id]:
        print(f"No orders yet for {order_id}.")
        return

    # Retrieve the order details from the global orders dictionary
    order_data = orders[order_id]
    current_order = order_data["items"]
    
    # Display cashier who handled the order
    print(f"\nCashier: {order_data['cashier']}")

    # Print order summary header
    print(f"=== ALL ORDER SUMMARY FOR {order_id}===")
    column_width = "{:<5} | {:<30} | {:<10} | {:<15} | {:<15}"
    header = column_width.format("No.", "Item", "Qty", "Price", "Total")
    print(header)
    print("-" * len(header))

    # Loop through each item in the order and display details
    grand_total = 0
    for idx, order in enumerate(current_order, start=1):
        price_format = f"Rp{order['price']:,}".replace(",", ".")
        total_format = f"Rp{order['total']:,}".replace(",", ".")
        print(column_width.format(idx, order['item'], order['quantity'], price_format, total_format))
        grand_total += order['total']

    # Display the grand total for this order
    grand_total_format = f"Rp{grand_total:,}".replace(",", ".")
    print(f"\nGrand Total: {grand_total_format}")

if __name__ == "__main__":
    order_type()
