# Dictionary to store all user data
users = {}

# ---------- BASIC VALIDATION ----------
def only_alpha(text):
    return all(char.isalpha() or char == " " for char in text)

def only_int(text):
    return text.isdigit()

def only_float(text):
    try:
        float(text)
        return True
    except:
        return False


# ---------- EMAIL VALIDATION ----------
def validate_email(email):
    if email.count("@") != 1:
        return False

    user, domain_full = email.split("@")

    #User check
    if not user or not "." in domain_full:
        return False

    if not user[0].isalnum():
        return False

    for char in user:
        if not (char.isalnum() or char in "._"):
            return False

    #Domain check   
    if domain_full.count(".") != 1:
        return False
    
    hosting, extension = domain_full.split(".")

    #Hosting check
    if not hosting.isalnum():
        return False
    
    #Extension check
    if not extension.isalpha() or len(extension) > 5:
        return False

    return True


# ---------- USER ID VALIDATION ----------
def validate_userid(uid):
    uid = uid.strip()

    if len(uid) < 6 or len(uid) > 20:
        return False

    has_letter = False
    has_digit = False

    for char in uid:
        if not (char.isalnum() or char in "._"):
            return False
        if char.isalpha():
            has_letter = True
        if char.isdigit():
            has_digit = True

    if not (has_letter and has_digit):
        return False

    if uid in users:
        return False

    return True


# ---------- PASSWORD VALIDATION ----------
def validate_password(pw):
    if len(pw) < 8:
        return False
    
    special = "/.,@#$%"
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" + special

    up = low = digit = spec = False
    
    for char in pw:
        if char not in allowed:
            return False

    for char in pw:
        if char.isupper():
            up = True
        if char.islower():
            low = True
        if char.isdigit():
            digit = True
        if char in special:
            spec = True

    return up and low and digit and spec


# ---------- REGISTRATION ----------
def register():
    print("\nWelcome New Member, Please Register")
    print("Enter Your Personal Data:")

    # ---------- UserID ----------
    print("\n[UserID Rules]")
    print("- Length 6–20 characters")
    print("- Must contain at least a letter and number")
    print("- Only letters, numbers, dot (.) and underscore (_) are allowed")

    while True:
        uid = input("UserID: ").strip()
        if validate_userid(uid):
            break
        print("UserID invalid or already exists")

    # ---------- Password ----------
    print("\n[Password Rules]")
    print("- Minimum 8 characters")
    print("- Must include at least one uppercase letter, one lowercase letter, and one number")
    print("- Must include at least one special character: / . , @ # $ % (no other symbols allowed)")

    while True:
        pw = input("Password: ")
        if validate_password(pw):
            break
        print("Password does not meet requirements")

    # ---------- Email ----------
    print("\n[Email Rules]")
    print("- Must contain '@' and a dot (.) after it")
    print("- Example: user@mail.com")

    while True:
        email = input("Email: ").strip()
        if validate_email(email):
            break
        print("Invalid email format")

    # ---------- Name ----------
    print("\n[Name Rules]")
    print("- Letters only")
    print("- Spaces allowed")

    while True:
        name = input("Name: ").strip()
        if name and all(char.isalpha() or char == " " for char in name):
            break
        print("Name must contain only letters")

    # ---------- Gender ----------
    print("\n[Gender Rules]")
    print("- Input: Male or Female")

    while True:
        gender = input("Gender (Male/Female): ").strip().lower()
        if gender in ["male", "female"]:
            break
        print("Please input Male or Female")

    # ---------- Age ----------
    print("\n[Age Rules]")
    print("- Between 17 and 80")

    while True:
        age = input("Age: ")
        if only_int(age):
            age = int(age)
            if 17 <= age <= 80:
                break
        print("Age must be between 17 and 80")

    # ---------- Job ----------
    print("\n[Job Rules]")
    print("- Letters only")

    while True:
        job = input("Job: ").strip()
        if only_alpha(job):
            break
        print("Job must contain letters only")

    # ---------- Hobby ----------
    print("\n[Hobby Rules]")
    print("- Minimum two words")
    print("- Letters only")

    while True:
        hobby = input("Hobby (separate multiple hobbies with comma): ").strip()
        hobbies = [h.strip() for h in hobby.split(",") if h.strip()]

        if len(hobbies) >= 2 and all(all(c.isalpha() or c == " " for c in activity) for activity in hobbies):
            break
        print("Hobby must contain at least two activities (letters only)")

    # ---------- Address ----------
    print("\nAddress Information")

    while True:
        city = input("City Name: ").strip()
        if only_alpha(city):
            break
        print("City must contain letters only")

    while True:
        rt = input("RT: ")
        if only_int(rt):
            break
        print("RT must be numeric")

    while True:
        rw = input("RW: ")
        if only_int(rw):
            break
        print("RW must be numeric")

    while True:
        zipcode = input("Zip Code (5 digits): ")
        if only_int(zipcode) and len(zipcode) == 5:
            break
        print("ZIP must be 5 digits")

    # ---------- Coordinates ----------
    print("\nGeo Coordinates Example: -6.200 or 106.816")

    while True:
        lat = input("Latitude: ")
        if only_float(lat):
            break
        print("Invalid latitude format")

    while True:
        longitude = input("Longitude: ")
        if only_float(longitude):
            break
        print("Invalid longitude format")

    # ---------- Phone ----------
    print("\n[Phone Number Rules]")
    print("- Numeric only")
    print("- Length 11–13 digits")

    while True:
        phone = input("Phone Number: ")
        if only_int(phone) and 11 <= len(phone) <= 13:
            break
        print("Phone number must be 11–13 digits")


    confirm = input("Save data? (Y/N): ").strip().lower()

    if confirm == "y":
        users[uid] = {
            "password": pw,
            "name": name,
            "email": email,
            "gender": gender,
            "age": age,
            "job": job,
            "hobby": hobbies,
            "address": {
                "city": city,
                "rt": rt,
                "rw": rw,
                "zip": zipcode,
                "lat": lat,
                "long": longitude,
            },
            "phone": phone,
        }
        print("Registration successful")
    else:
        print("Registration cancelled")


# ---------- LOGIN ----------
def login():
    attempts = 0

    while attempts < 5:
        print(f"\nLogin attempt ({attempts+1}/5)")
        uid = input("UserID: ")
        pw = input("Password: ")

        if uid not in users:
            print("User not registered")
            attempts += 1
            continue

        if users[uid]["password"] != pw:
            print("Wrong password")
            attempts += 1
            continue

        print("Login successful")
        return uid

    print("Too many attempts")
    return None


# ---------- PROFILE ----------
def profile(uid):
    u = users[uid]

    print("\n=== PROFILE ===")
    print("Name:", u["name"])
    print("Email:", u["email"])
    print("Gender:", u["gender"])
    print("Age:", u["age"])
    print("Job:", u["job"])
    print("Hobby:", ", ".join(u["hobby"]))


    addr = u["address"]

    print("\nAddress")
    print("City:", addr["city"])
    print("RT:", addr["rt"])
    print("RW:", addr["rw"])
    print("Zip:", addr["zip"])

    print("\nGeo")
    print("Latitude:", addr["lat"])
    print("Longitude:", addr["long"])

    print("Phone:", u["phone"])
    
# ---------- Edit User Data ----------
def edit_profile(uid):
    u = users[uid]

    print("\n=== Edit Profile ===")
    print("Press Enter to skip any field.\n")

    # Name
    print(f"Current Name : {u['name']}")
    new_name = input("New Name: ").strip()
    if new_name:
        u["name"] = new_name

    # Email
    print(f"\nCurrent Email: {u['email']}")
    new_email = input("New Email: ").strip()
    if new_email:
        if validate_email(new_email):
            u["email"] = new_email
        else:
            print("Invalid email format. Email not updated.")

    # Job
    print(f"\nCurrent Job  : {u['job']}")
    new_job = input("New Job: ").strip()
    if new_job:
        u["job"] = new_job

    # Phone
    print(f"\nCurrent Phone: {u['phone']}")
    while True:
        new_phone = input("New Phone: ").strip()
        if not new_phone:
            break
        if only_int(new_phone) and 11 <= len(new_phone) <= 13:
            u["phone"] = new_phone
            break
        else:
            print("Phone must be numeric and 11-13 digits. Try again.")

    # Address
    addr = u["address"]

    print("\n--- Address Update ---")

    print(f"Current City: {addr['city']}")
    new_city = input("New City: ").strip()
    if new_city and only_alpha(new_city):
        addr["city"] = new_city

    print(f"Current RT: {addr['rt']}")
    new_rt = input("New RT: ").strip()
    if new_rt and only_int(new_rt):
        addr["rt"] = new_rt

    print(f"Current RW: {addr['rw']}")
    new_rw = input("New RW: ").strip()
    if new_rw and only_int(new_rw):
        addr["rw"] = new_rw

    print(f"Current Zip: {addr['zip']}")
    new_zip = input("New Zip Code: ").strip()
    if new_zip and only_int(new_zip) and len(new_zip) == 5:
        addr["zip"] = new_zip
        
    # Geo
    
    print(f"Current Latitude: {addr['lat']}")
    new_lat = input("New Latitude: ").strip()
    if new_lat and only_float(new_lat):
        addr["lat"] = new_lat

    print(f"Current Longitude: {addr['long']}")
    new_long = input("New Longitude: ").strip()
    if new_long and only_float(new_long):
        addr["long"] = new_long

    print("\nProfile updated successfully.")

# ---------- Delete Account ----------
def delete_account(uid):
    confirm = input("Delete account permanently? (Y/N): ").lower()

    if confirm == "y":
        del users[uid]
        print("Account deleted")
        return True

    print("Deletion cancelled")
    return False

# ---------- View Users ----------
def view_users():
    if not users:
        print("No users registered")
        return

    print("\n=== REGISTERED USERS ===")
    for uid, data in users.items():
        print(f"{uid} - {data['name']}")


    
# ---------- AUTH MENU ----------
def auth_menu():
    while True:
        print("\n=== AUTH MENU ===")
        print("1. Register new user")
        print("2. Login")
        print("3. Back to Main Menu")

        try:
            choice = int(input("Choose: "))
        except ValueError:
            print("Please enter a valid number!")
            continue

        if choice == 1:
            register()

        elif choice == 2:
            user = login()
            if user:
                return user  # langsung kirim user ke main

        elif choice == 3:
            print("Program closed.")
            return None

        else:
            print("Invalid option. Please choose 1-3.")

# ---------- USER MENU ----------
def user_menu(user):
    while True:
        print("\n=== USER MENU ===")
        print("1. View Profile")
        print("2. Edit Profile")
        print("3. Delete Account")
        print("4. Back to Main Menu")
        print("5. Logout")

        try:
            choice = int(input("Choose: "))
        except ValueError:
            print("Please enter a valid number!")
            continue

        if choice == 1:
            profile(user)

        elif choice == 2:
            edit_profile(user)

        elif choice == 3:
            if delete_account(user):
                return None  # akun dihapus

        elif choice == 4:
            return user  # kembali ke main menu

        elif choice == 5:
            print("Logged out")
            return None
        
        else:
            print("Invalid option! Please choose 1-5.")
