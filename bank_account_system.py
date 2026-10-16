"""Bank account management module."""
import hashlib
import json
import os
import secrets

SERVICE_FEE = 2.50

account_data = {}

def create_account(acc_id, name, initial_deposit=0, transactions=None):
    """Create an account; return False if the id already exists."""
    if transactions is None:
        transactions = []
    if acc_id in account_data:
        return False
    account_data[acc_id] = {"name": name, "balance": initial_deposit}
    transactions.append(f"Created {acc_id} with initial balance {initial_deposit}")
    return True

def deposit(acc_id, amount):
    """Add a positive amount to an account; return True on success."""
    if acc_id not in account_data or amount <= 0:
        return False
    account_data[acc_id]["balance"] += amount
    return True

def withdraw(acc_id, amount):
    """Withdraw amount plus the service fee; return True on success."""
    if acc_id not in account_data or amount <= 0:
        return False
    total = amount + SERVICE_FEE
    if account_data[acc_id]["balance"] < total:
        return False
    account_data[acc_id]["balance"] -= total
    return True

def compute_bonus(acc_id, rate):
    """Return the promotional bonus: balance multiplied by rate."""
    return account_data[acc_id]["balance"] * rate

def get_hash(pin, salt=None):
    """Return 'salt$hash' for a PIN using salted PBKDF2-SHA256."""
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", pin.encode(), salt, 200_000)
    return salt.hex() + "$" + digest.hex()

def generate_temp_pin():
    """Return a cryptographically secure 4-digit temporary PIN."""
    return secrets.randbelow(9000) + 1000

def backup_data(filename="backup.txt"):
    """Write all account data to a JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(account_data, file)
    print("Backup complete:", filename)

def main():
    """Run a small demonstration of the banking functions."""
    admin_token = os.environ.get("BANK_ADMIN_TOKEN")
    create_account("A01", "Alice", 1000)
    deposit("A01", 500)
    withdraw("A01", 200)
    print("Bonus:", compute_bonus("A01", 0.05))
    print("PIN Hash:", get_hash("1234"))
    print("Temp PIN:", generate_temp_pin())
    backup_data()
    print("Token initialized:", admin_token is not None)

if __name__ == "__main__":
    main()
