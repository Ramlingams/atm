
# Simple ATM Simulator

A beginner-friendly ATM simulator CLI application in Python.

## Features
- Create account (4-digit PIN)
- Login using account number and PIN
- Check balance
- Deposit
- Withdraw
- Transfer between accounts
- Transaction history
- Data persisted in `accounts.json`

## Run
1. Make sure you have Python 3 installed.
2. Open terminal in project folder.
3. Run: `python atm.py`

Notes:
- PIN input is hidden while typing.
- Balances are in INR (₹) for display only.

## Files
- `atm.py` - main application
- `accounts.json` - data file (created/updated automatically)
- `.vscode/launch.json` - optional VS Code debug launch config
