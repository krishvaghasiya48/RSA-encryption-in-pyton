import time
import random


user_password = "1234"
user_mobile = 8866447404

def send_otp():
   
    otp = str(random.randint(1000, 9999))
    print(f"[Simulated SMS] OTP sent to your mobile: {otp}")
    return otp

def register_user():
    global user_password, user_mobile
    print("=== User Registration ===")
    user_mobile = input("Enter your mobile number: ")
    user_password = input("Set your new password: ")
    print("Registration complete!\n")

def forgot_password():
    global user_password
    print("\n=== Forgot Password ===")
    mobile_input = input("Enter your registered mobile number: ")

    if mobile_input == user_mobile:
        otp = send_otp()
        entered_otp = input("Enter the OTP sent to your mobile: ")
        if entered_otp == otp:
            user_password = input("Enter new password: ")
            print("Password reset successful!\n")
        else:
            print("Incorrect OTP. Cannot reset password.\n")
    else:
        print("Mobile number not recognized.\n")

def door_lock_system():
    print("Welcome to the Automatic Door Lock System")

    while True:
        print("\n1. Unlock Door")
        print("2. Forgot Password")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            attempts = 3
            while attempts > 0:
                entered_password = input("Enter password to unlock the door: ")

                if entered_password == user_password:
                    print("\nAccess Granted!")
                    print("Door is UNLOCKED.")
                    time.sleep(3)
                    print("Door is now LOCKED again.")
                    break
                else:
                    attempts -= 1
                    print(f"Incorrect password. Attempts left: {attempts}")
                    if attempts == 0:
                        print("\nMaximum attempts reached. Door remains LOCKED.")
            continue

        elif choice == "2":
            forgot_password()
        
        elif choice == "3":
            print("Exiting system. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

if _name_ == "_main":
    register_user()
    door_lock_system()