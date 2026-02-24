from menu_management import (
    view_menu,
    add_item,
    edit_delete_item,
    search_menu,
)

from order_management import order_type, show_orders
from menu_database_mysql import get_menu
from auth import auth_menu, user_menu


# Store current logged-in user
current_user = None


# 1. MAIN MENU
def main_menu():
    global current_user

    while True:
        print("\n=== RestoApps ===")

        # Temporary list to hold current menu options
        menu = []

        # Show login option if user not logged in
        if not current_user:
            menu.append("Login and Register")
        else:
            menu.append("User Menu")

        # Main features
        menu += ["Menu Management", "Order Management"]

        # Logout only visible if user logged in
        if current_user:
            menu.append("Logout")

        menu.append("Exit Program")

        #Print the main_menu with numbers
        for index, item in enumerate(menu, start=1):
            print(f"{index}. {item}")

        #Get user choice
        try:
            choice = int(input("Choose: "))
        except ValueError:
            print("Please enter a valid number!")
            continue

        #User choice to action dynamically
        index = choice - 1
        if not (0 <= index < len(menu)):
            print("Invalid option. Please try again.")
            continue
        
        selected_choice = menu[index]
        
        # ---------- LOGIN / USER MENU ----------
        if selected_choice in ["Login and Register", "User Menu"]:
            # Login/Register flow
            if not current_user:
                user = auth_menu()
                if user:
                    current_user = user
            # Open user menu
            else:
                result = user_menu(current_user)

                # User logged out or deleted account
                if result is None:
                    current_user = None
                else:
                    current_user = result

        # ---------- MENU MANAGEMENT ----------
        elif selected_choice == "Menu Management":
            if not current_user:
                print("Please Login First!")
                continue

            menu_management()

        # ---------- ORDER MANAGEMENT ----------
        elif selected_choice == "Order Management":
            if not current_user:
                print("Please Login First!")
                continue

            order_management()

        # ---------- LOGOUT ----------
        elif selected_choice == "Logout" and current_user:
            print(f"User '{current_user}' logged out")
            current_user = None

        # ---------- EXIT PROGRAM ----------
        elif selected_choice == "Exit Program":
            print("Session ended")
            break

        else:
            print("Invalid option. Please try again.")


# 2. MENU MANAGEMENT
def menu_management():
    while True:
        print("\n=== MANAGE MENU ===")
        print("1. View full menu")
        print("2. Add new menu item")
        print("3. Edit/delete item on the menu")
        print("4. Search menu")
        print("5. Back to Main Menu")

        # Get user input for submenu choice
        try:
            user_input = int(input("Choose between 1-5: "))
        except ValueError:
            print("Must be a number.")
            continue

        # View all menu items
        if user_input == 1:
            view_menu(get_menu(), allow_edit=True)

        # Add new item
        elif user_input == 2:
            add_item()

        # Edit or delete menu item
        elif user_input == 3:
            edit_delete_item(get_menu())

        # Search item
        elif user_input == 4:
            search_menu(get_menu())

        # Back to main menu
        elif user_input == 5:
            print("\nReturning to Main Menu.")
            break

        else:
            print("Invalid option. Please choose 1-5.")


# 3. ORDER MANAGEMENT
def order_management():
    global current_user

    while True:
        print("\n=== ORDER MENU ===")
        print("1. Take order")
        print("2. Review order")
        print("3. Back to Main Menu")

        # Get user input for submenu choice
        try:
            user_input = int(input("Choose between 1-3: "))
        except ValueError:
            print("Must be a number. Try again.")
            continue

        # Take new order
        if user_input == 1:
            order_type(current_user)

        # Review existing order
        elif user_input == 2:
            table_or_invoice = input(
                "Enter table number or invoice to review: "
            ).strip()
            show_orders(table_or_invoice)

        # Back to main menu
        elif user_input == 3:
            print("\nReturning to Main Menu.")
            break

        else:
            print("Invalid option. Please choose 1-3.")


# PROGRAM ENTRY POINT  
# Ensures program runs only when file executed directly
if __name__ == "__main__":
    main_menu()
