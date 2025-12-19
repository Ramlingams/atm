#!/usr/bin/env python3
"""
Simple ATM Simulator
Run: python atm.py

Features:
- Create account (username, PIN)
- Login with account number and PIN
- Check balance
- Deposit
- Withdraw (with insufficient funds check)
- Transfer to another account
- View transaction history
- Data persisted in accounts.json
"""

import json
import os
import getpass
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "accounts.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"next_acc": 1001, "accounts": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def create_account(data):
    name = input("Full name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    while True:
        pin = getpass.getpass("Choose a 4-digit PIN: ").strip()
        if len(pin) == 4 and pin.isdigit():
            pin_confirm = getpass.getpass("Confirm PIN: ").strip()
            if pin == pin_confirm:
                break
            else:
                print("PINs do not match. Try again.")
        else:
            print("PIN must be exactly 4 digits.")
    acc_num = str(data["next_acc"])
    data["next_acc"] += 1
    data["accounts"][acc_num] = {
        "name": name,
        "pin": pin,
        "balance": 0.0,
        "history": [
            {"time": datetime.utcnow().isoformat()+"Z", "type": "create", "amount": 0, "note": "Account created"}
        ]
    }
    save_data(data)
    print(f"Account created. Your account number is: {acc_num}")
    print("Please remember your account number and PIN.")

def authenticate(data):
    acc = input("Account number: ").strip()
    pin = getpass.getpass("PIN: ").strip()
    acc_data = data["accounts"].get(acc)
    if not acc_data:
        print("Account not found.")
        return None
    if acc_data["pin"] != pin:
        print("Invalid PIN.")
        return None
    return acc

def show_balance(data, acc):
    bal = data["accounts"][acc]["balance"]
    print(f"Current balance: ₹{bal:.2f}")

def add_history(data, acc, typ, amount, note=""):
    data["accounts"][acc]["history"].append({
        "time": datetime.utcnow().isoformat()+"Z",
        "type": typ,
        "amount": amount,
        "note": note
    })

def deposit(data, acc):
    try:
        amt = float(input("Amount to deposit: ").strip())
    except ValueError:
        print("Invalid amount.")
        return
    if amt <= 0:
        print("Amount must be positive.")
        return
    data["accounts"][acc]["balance"] += amt
    add_history(data, acc, "deposit", amt, "Cash deposit")
    save_data(data)
    print(f"Deposited ₹{amt:.2f}.")

def withdraw(data, acc):
    try:
        amt = float(input("Amount to withdraw: ").strip())
    except ValueError:
        print("Invalid amount.")
        return
    if amt <= 0:
        print("Amount must be positive.")
        return
    if data["accounts"][acc]["balance"] < amt:
        print("Insufficient funds.")
        return
    data["accounts"][acc]["balance"] -= amt
    add_history(data, acc, "withdraw", amt, "Cash withdrawal")
    save_data(data)
    print(f"Withdrew ₹{amt:.2f}.")

def transfer(data, acc):
    to_acc = input("Recipient account number: ").strip()
    if to_acc == acc:
        print("Cannot transfer to the same account.")
        return
    if to_acc not in data["accounts"]:
        print("Recipient account not found.")
        return
    try:
        amt = float(input("Amount to transfer: ").strip())
    except ValueError:
        print("Invalid amount.")
        return
    if amt <= 0:
        print("Amount must be positive.")
        return
    if data["accounts"][acc]["balance"] < amt:
        print("Insufficient funds.")
        return
    data["accounts"][acc]["balance"] -= amt
    data["accounts"][to_acc]["balance"] += amt
    add_history(data, acc, "transfer_out", amt, f"To {to_acc}")
    add_history(data, to_acc, "transfer_in", amt, f"From {acc}")
    save_data(data)
    print(f"Transferred ₹{amt:.2f} to account {to_acc}.")

def view_history(data, acc):
    hist = data["accounts"][acc]["history"]
    print("--- Transaction history (most recent first) ---")
    for entry in reversed(hist):
        t = entry.get("time", "")
        typ = entry.get("type", "")
        amt = entry.get("amount", 0)
        note = entry.get("note", "")
        print(f"{t} | {typ:12} | ₹{amt:.2f} | {note}")

def account_menu(data, acc):
    while True:
        print("\n--- Account Menu ---")
        print("1) Check balance")
        print("2) Deposit")
        print("3) Withdraw")
        print("4) Transfer")
        print("5) Transaction history")
        print("6) Logout")
        choice = input("Choose: ").strip()
        if choice == "1":
            show_balance(data, acc)
        elif choice == "2":
            deposit(data, acc)
        elif choice == "3":
            withdraw(data, acc)
        elif choice == "4":
            transfer(data, acc)
        elif choice == "5":
            view_history(data, acc)
        elif choice == "6":
            print("Logging out.")
            break
        else:
            print("Invalid choice.")

def main():
    data = load_data()
    print("Welcome to Simple ATM Simulator")
    while True:
        print("\n1) Create account")
        print("2) Login")
        print("3) Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            create_account(data)
        elif choice == "2":
            acc = authenticate(data)
            if acc:
                account_menu(data, acc)
            data = load_data()  # reload in case external edits
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()


\\ipdate



ggsgsgsgdsg