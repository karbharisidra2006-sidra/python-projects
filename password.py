import json
import os
import base64
import hashlib
import getpass
import random
import string

FILE = "vault.json"

def encrypt(text, key):
    encoded = "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))
    return base64.b64encode(encoded.encode()).decode()

def decrypt(text, key):
    decoded = base64.b64decode(text).decode()
    return "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(decoded))

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

def generate_password():
    chars = string.ascii_letters + string.digits + "@#$%^&*"
    return "".join(random.choice(chars) for _ in range(12))

def main():
    print("Secure Password Manager")

    master = getpass.getpass("Enter master password: ")
    master_hash = hash_password(master)

    data = load_data()

    if "master" not in data:
        data["master"] = master_hash
        save_data(data)
        print("Master password set")

    elif data["master"] != master_hash:
        print("Incorrect password")
        return

    while True:
        print("\n1 Add Password\n2 View Passwords\n3 Generate Password\n4 Exit")
        choice = input("Choose: ")

        if choice == "1":
            site = input("Website: ")
            username = input("Username: ")
            password = getpass.getpass("Password: ")

            encrypted = encrypt(password, master)
            data[site] = {"username": username, "password": encrypted}
            save_data(data)

            print("Saved")

        elif choice == "2":
            for site in data:
                if site == "master":
                    continue
                decrypted = decrypt(data[site]["password"], master)
                print("\nSite:", site)
                print("Username:", data[site]["username"])
                print("Password:", decrypted)

        elif choice == "3":
            print("Generated Password:", generate_password())

        elif choice == "4":
            break

        else:
            print("Invalid choice")

main()