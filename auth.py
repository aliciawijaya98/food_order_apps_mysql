from user_database_mysql import ( 
    register_user,
    login_user,
    get_user_by_userid,
    update_user,
    delete_user,
    get_all_users
)

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
    if not user or "." not in domain_full:
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
    
    if not all(c.isalnum() or c in "._" for c in uid):
        return False
    
    has_letter = any(c.isalpha() for c in uid)
    has_digit = any(c.isdigit() for c in uid)
    
    if not (has_letter and has_digit):
        return False
    
    # cek ke database
    if get_user_by_userid(uid):
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
        success, message = register_user({
        "user_id": uid,
        "password": pw,
        "email": email,
        "name": name,
        "gender": gender,
        "age": age,
        "job": job,
        "hobby": hobbies,
        "city": city,
        "rt": rt,
        "rw": rw,
        "zip": zipcode,
        "lat": lat,
        "long": longitude,
        "phone": phone
    })

        print(message)
    else:
        print("Registration cancelled")


# ---------- LOGIN ----------
def login():
    attempts = 0

    while attempts < 5:
        print(f"\nLogin attempt ({attempts+1}/5)")
        uid = input("UserID: ")
        pw = input("Password: ")

        success, result = login_user(uid,pw)
        
        if not success:
            print(result)
            attempts += 1
            continue

        print("Login successful")
        return uid

    print("Too many attempts")
    return None


# ---------- PROFILE ----------
def profile(uid):
    user = get_user_by_userid(uid)
     
    if not user:
        print("User not found.")
        return
    
    print("\n=== PROFILE ===")
    print("Name:", user["name"])
    print("Email:", user["email"])
    print("Gender:", user["gender"])
    print("Age:", user["age"])
    print("Job:", user["job"])
    print("Hobby:", ", ".join(user["hobby"].split(",")))
    
    print("\nAddress")
    print("City:", user["city"])
    print("RT:", user["rt"])
    print("RW:", user["rw"])
    print("Zip:", user["zip"])

    print("\nGeo")
    print("Latitude:", user["latitude"])
    print("Longitude:", user["longitude"])

    print("Phone:", user["phone"])
    
# ---------- Edit User Data ----------
def edit_profile(uid):
    user = get_user_by_userid(uid) 
    
    if not user:
        print("User not found.")
        return

    print("\n=== Edit Profile ===")
    print("Press Enter to skip any field.\n")

    # Name
    print(f"Current Name : {user['name']}")
    new_name = input("New Name: ").strip()
    if new_name and not only_alpha(new_name):
        print("Name must contain letters only.")
        new_name = user["name"]
    elif not new_name: 
        new_name = user["name"]

    # Email
    print(f"\nCurrent Email: {user['email']}")
    new_email = input("New Email: ").strip()
    if new_email:
        if not validate_email(new_email):
            print("Invalid email format.")
            new_email = user["email"]
    else:
        new_email = user["email"]
            
    # Job
    print(f"\nCurrent Job  : {user['job']}")
    new_job = input("New Job: ").strip()
    if new_job and not only_alpha(new_job):
        new_job = user ["job"]
    elif not new_job:
        new_job = user ["job"]

    # Phone
    print(f"\nCurrent Phone: {user['phone']}")
    new_phone = input("New Phone: ").strip()
    if new_phone:
        if not (only_int(new_phone) and 11 <= len(new_phone) <= 13):
            print("Phone must be numeric and 11-13 digits.")
            new_phone = user["phone"]
    else:
        new_phone = user["phone"]
            
    # city
    print("\n--- Address Update ---")
    print(f"\nCurrent City: {user['city']}")
    new_city = input("New City: ").strip()
    if new_city and not only_alpha(new_city):
        print ("City must contain letters only")
        new_city = user["city"]
    elif not new_city:
        new_city = user["city"]

    #RT
    print(f"Current RT: {user['rt']}")
    new_rt = input("New RT: ").strip()
    if new_rt and not only_int(new_rt):
        print ("RT must be numeric.")
        new_rt = user["rt"]
    elif not new_rt:
        new_rt = user["rt"]

    #RW
    print(f"Current RW: {user['rw']}")
    new_rw = input("New RW: ").strip()
    if new_rw and not only_int(new_rw):
        print ("RW must be numeric.")
        new_rw = user["rw"]
    elif not new_rw: 
        new_rw = user["rw"]

    #ZIP
    print(f"Current Zip: {user['zip']}")
    new_zip = input("New Zip Code: ").strip()
    if new_zip:
        if not (only_int(new_zip) and len(new_zip) == 5):
            print("Zip must be 5 digits")
            new_zip = user["zip"]
    else:
        new_zip = user["zip"]
        
    # LATITUDE
    
    print(f"Current Latitude: {user['latitude']}")
    new_lat = input("New Latitude: ").strip()
    if new_lat and not only_float(new_lat):
        print("Invalid latitude format.")
        new_lat = user["latitude"]
    elif not new_lat:
        new_lat = user["latitude"]

    #LONGITUDE
    print(f"Current Longitude: {user['longitude']}")
    new_long = input("New Longitude: ").strip()
    if new_long and not only_float(new_long):
        print("Invalid longitude format.")
        new_long = user["longitude"]
    elif not new_long:
        new_long = user["longitude"]
        
    # Update Database
    updated_data = {
        "name": new_name,
        "email": new_email,
        "job": new_job,
        "phone": new_phone,
        "city": new_city,
        "rt": new_rt,
        "rw": new_rw,
        "zip": new_zip,
        "lat": new_lat,
        "long": new_long,
    }
    
    success, message = update_user(uid, updated_data)
    print (message)

# ---------- Delete Account ----------
def delete_account(uid):
    confirm = input("Delete account permanently? (Y/N): ").lower()

    if confirm == "y":
        success, message = delete_user(uid) 
        print(message)
        return success

    print("Deletion cancelled")
    return False

# ---------- View Users ----------
def view_users():
    users = get_all_users()
    
    if not users:
        print("No users registered")
        return

    print("\n=== REGISTERED USERS ===")
    for user in users:
        print(f"{user['user_id']} - {user['name']}")


    
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
