from zeep import Client


def main():
    client = Client('http://localhost:8000/?wsdl')

    print("===== Password Reset Service =====")
    attempts = 0

    while attempts < 5:
        username = input("\nEnter your username: ")

        print("Verifying username...")
        if not client.service.verify_username(username):
            print("Username not found or account is blocked. Try again later.")
            attempts += 1
            continue

        keyword = input("Enter your keyword: ")
        print("Verifying keyword...")
        if not client.service.verify_by_keyword(username, keyword):
            print("Invalid keyword or account blocked. Try again later.")
            attempts += 1
            continue

        email = input("Enter your alternative email: ")
        print("Verifying email...")
        if not client.service.verify_by_email(username, email):
            print("Invalid email or account blocked. Try again later.")
            attempts += 1
            continue

        print("\nAll verifications passed. Now you can set a new password.")
        print("Password must be at least 8 characters and contain at least one letter and one digit.")

        new_password = input("Enter new password: ")
        confirm_password = input("Confirm new password: ")

        print("Resetting password...")
        if client.service.reset_password(username, new_password, confirm_password):
            print("\nPassword reset successful!")
            return True
        else:
            print("\nPassword reset failed. Passwords must match and follow security rules.")
            attempts += 1

    print("\nToo many failed attempts. Please try again later.")
    return False


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")