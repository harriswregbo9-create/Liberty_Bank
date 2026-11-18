
import csv
import os
from datetime import date
from decimal import Decimal, InvalidOperation


# ==========================================
# LIBERTY BANK - BANKING APPLICATION
# INFO 301 FINAL PROJECT
# ==========================================

CUSTOMER_FILE = "customers.csv"
ACCOUNT_FILE = "accounts.csv"
TRANSACTION_FILE = "transactions.csv"

CUSTOMER_HEADERS = ["customer_id", "name", "phone", "email"]

ACCOUNT_HEADERS = ["account_number", "customer_id", "balance"]

TRANSACTION_HEADERS = [
    "transaction_id",
    "account_number",
    "transaction_type",
    "amount",
    "date"
]


# ==========================================
# 1. INITIALIZE CSV FILES
# ==========================================

def initialize_files():

    files = {
        CUSTOMER_FILE: CUSTOMER_HEADERS,
        ACCOUNT_FILE: ACCOUNT_HEADERS,
        TRANSACTION_FILE: TRANSACTION_HEADERS
    }

    for filename, headers in files.items():

        if not os.path.exists(filename):

            with open(filename, "w", newline="", encoding="utf-8") as file:

                writer = csv.writer(file)
                writer.writerow(headers)


# ==========================================
# 2. READ CSV DATA
# ==========================================

def read_data(filename):

    try:

        with open(filename, "r", newline="", encoding="utf-8") as file:

            reader = csv.DictReader(file)
            return list(reader)

    except FileNotFoundError:

        print("File not found:", filename)
        return []


# ==========================================
# 3. SAVE CSV DATA
# ==========================================

def save_data(filename, headers, records):

    with open(filename, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=headers)

        writer.writeheader()
        writer.writerows(records)


# ==========================================
# 4. GENERATE UNIQUE IDS
# ==========================================

def generate_id(records, field, prefix):

    numbers = []

    for record in records:

        try:

            number = int(
                record[field].replace(prefix, "")
            )

            numbers.append(number)

        except (ValueError, KeyError, AttributeError):

            continue

    next_number = max(numbers, default=0) + 1

    return prefix + str(next_number).zfill(4)


# ==========================================
# 5. REGISTER CUSTOMER
# ==========================================

def register_customer():

    print("\n========== CUSTOMER REGISTRATION ==========")

    name = input("Enter customer name: ").strip()
    phone = input("Enter phone number: ").strip()
    email = input("Enter email address: ").strip()

    if not name or not phone or not email:

        print("All fields are required.")
        return

    if "@" not in email or "." not in email:

        print("Please enter a valid email address.")
        return

    customers = read_data(CUSTOMER_FILE)

    customer_id = generate_id(
        customers,
        "customer_id",
        "CUS"
    )

    new_customer = {
        "customer_id": customer_id,
        "name": name,
        "phone": phone,
        "email": email
    }

    customers.append(new_customer)

    save_data(
        CUSTOMER_FILE,
        CUSTOMER_HEADERS,
        customers
    )

    print("\nCustomer registered successfully!")
    print("Customer ID:", customer_id)


# ==========================================
# 6. VIEW ALL CUSTOMERS
# ==========================================

def view_customers():

    customers = read_data(CUSTOMER_FILE)

    print("\n========== REGISTERED CUSTOMERS ==========")

    if not customers:

        print("No customers registered.")
        return

    for customer in customers:

        print("--------------------------------")
        print("Customer ID:", customer["customer_id"])
        print("Name:", customer["name"])
        print("Phone:", customer["phone"])
        print("Email:", customer["email"])


# ==========================================
# 7. CREATE BANK ACCOUNT
# ==========================================

def create_account():

    print("\n========== CREATE BANK ACCOUNT ==========")

    customer_id = input("Enter customer ID: ").strip()

    customers = read_data(CUSTOMER_FILE)

    customer_exists = any(
        customer["customer_id"] == customer_id
        for customer in customers
    )

    if not customer_exists:

        print("Customer not found. Register customer first.")
        return

    try:

        opening_balance = Decimal(
            input("Enter opening balance: $").strip()
        )

        if not opening_balance.is_finite() or opening_balance < 0:

            print("Opening balance must be zero or greater.")
            return

    except InvalidOperation:

        print("Invalid amount. Enter a valid number.")
        return

    accounts = read_data(ACCOUNT_FILE)

    account_number = generate_id(
        accounts,
        "account_number",
        "ACC"
    )

    new_account = {
        "account_number": account_number,
        "customer_id": customer_id,
        "balance": str(opening_balance.quantize(Decimal("0.01")))
    }

    new_transaction = {
        "transaction_id": generate_id(
            read_data(TRANSACTION_FILE),
            "transaction_id",
            "TXN"
        ),
        "account_number": account_number,
        "transaction_type": "Opening Balance",
        "amount": str(opening_balance.quantize(Decimal("0.01"))),
        "date": date.today().isoformat()
    }

    accounts.append(new_account)

    transactions = read_data(TRANSACTION_FILE)
    transactions.append(new_transaction)

    try:

        save_data(ACCOUNT_FILE, ACCOUNT_HEADERS, accounts)

        save_data(
            TRANSACTION_FILE,
            TRANSACTION_HEADERS,
            transactions
        )

    except OSError:

        accounts.remove(new_account)

        try:
            save_data(ACCOUNT_FILE, ACCOUNT_HEADERS, accounts)
        except OSError:
            pass

        print("Account creation failed. Check file permissions.")
        return

    print("\nAccount created successfully!")
    print("Account Number:", account_number)
    print("Customer ID:", customer_id)
    print("Opening Balance: $", new_account["balance"])


# ==========================================
# 8. VIEW ACCOUNT BALANCE
# ==========================================

def view_balance():

    print("\n========== ACCOUNT BALANCE ==========")

    account_number = input("Enter account number: ").strip()

    accounts = read_data(ACCOUNT_FILE)

    for account in accounts:

        if account["account_number"] == account_number:

            customers = read_data(CUSTOMER_FILE)

            customer_name = "Unknown"

            for customer in customers:

                if customer["customer_id"] == account["customer_id"]:

                    customer_name = customer["name"]
                    break

            print("\nAccount Found!")
            print("--------------------------------")
            print("Account Number:", account["account_number"])
            print("Customer Name:", customer_name)
            print("Customer ID:", account["customer_id"])
            print("Current Balance: $", account["balance"])
            return

    print("Account not found.")


# ==========================================
# 9. PROCESS DEPOSIT AND WITHDRAWAL
# ==========================================

def process_transaction(transaction_type):

    print("\n==========", transaction_type.upper(), "==========")

    account_number = input("Enter account number: ").strip()

    accounts = read_data(ACCOUNT_FILE)

    account = None

    for item in accounts:

        if item["account_number"] == account_number:

            account = item
            break

    if account is None:

        print("Account not found.")
        return

    try:

        amount = Decimal(
            input("Enter amount: $").strip()
        )

        if not amount.is_finite() or amount <= 0:

            print("Amount must be greater than zero.")
            return

    except InvalidOperation:

        print("Invalid amount. Please enter a number.")
        return

    amount = amount.quantize(Decimal("0.01"))

    current_balance = Decimal(account["balance"])

    # Withdrawal validation

    if transaction_type == "Withdrawal":

        if amount > current_balance:

            print("\nInsufficient funds!")
            print("Available Balance: $", current_balance)
            return

        new_balance = current_balance - amount

    else:

        new_balance = current_balance + amount

    # Update account balance

    account["balance"] = str(new_balance)

    transactions = read_data(TRANSACTION_FILE)

    transaction_id = generate_id(
        transactions,
        "transaction_id",
        "TXN"
    )

    new_transaction = {
        "transaction_id": transaction_id,
        "account_number": account_number,
        "transaction_type": transaction_type,
        "amount": str(amount),
        "date": date.today().isoformat()
    }

    # Save account and transaction records

    old_accounts = read_data(ACCOUNT_FILE)

    try:

        transactions.append(new_transaction)

        save_data(
            ACCOUNT_FILE,
            ACCOUNT_HEADERS,
            accounts
        )

        save_data(
            TRANSACTION_FILE,
            TRANSACTION_HEADERS,
            transactions
        )

    except OSError:

        # Attempt to restore the original account records

        try:

            save_data(
                ACCOUNT_FILE,
                ACCOUNT_HEADERS,
                old_accounts
            )

        except OSError:

            print("Warning: Account file restoration failed.")

        print("Transaction could not be completed.")
        return

    print("\nTransaction successful!")
    print("Transaction ID:", transaction_id)
    print("Transaction Type:", transaction_type)
    print("Amount: $", amount)
    print("New Account Balance: $", new_balance)


# ==========================================
# 10. DEPOSIT MONEY
# ==========================================

def deposit_money():

    process_transaction("Deposit")


# ==========================================
# 11. WITHDRAW MONEY
# ==========================================

def withdraw_money():

    process_transaction("Withdrawal")


# ==========================================
# 12. TRANSACTION HISTORY
# ==========================================

def transaction_history():

    print("\n========== TRANSACTION HISTORY ==========")

    account_number = input("Enter account number: ").strip()

    accounts = read_data(ACCOUNT_FILE)

    account_exists = any(
        account["account_number"] == account_number
        for account in accounts
    )

    if not account_exists:

        print("Account not found.")
        return

    transactions = read_data(TRANSACTION_FILE)

    account_transactions = [
        transaction for transaction in transactions
        if transaction["account_number"] == account_number
    ]

    if not account_transactions:

        print("No transactions found.")
        return

    total_opening = Decimal("0.00")
    total_deposits = Decimal("0.00")
    total_withdrawals = Decimal("0.00")

    print("\nAccount Number:", account_number)

    for transaction in account_transactions:

        amount = Decimal(transaction["amount"])

        print("--------------------------------")
        print("Transaction ID:", transaction["transaction_id"])
        print("Type:", transaction["transaction_type"])
        print("Amount: $", amount)
        print("Date:", transaction["date"])

        if transaction["transaction_type"] == "Opening Balance":

            total_opening += amount

        elif transaction["transaction_type"] == "Deposit":

            total_deposits += amount

        elif transaction["transaction_type"] == "Withdrawal":

            total_withdrawals += amount

    print("\n========== TRANSACTION SUMMARY ==========")
    print("Opening Balances: $", total_opening)
    print("Total Deposits: $", total_deposits)
    print("Total Withdrawals: $", total_withdrawals)
    print(
        "Net Recorded Movement: $",
        total_opening + total_deposits - total_withdrawals
    )


# ==========================================
# 13. BASIC BANKING REPORTS
# ==========================================

def basic_reports():

    customers = read_data(CUSTOMER_FILE)
    accounts = read_data(ACCOUNT_FILE)
    transactions = read_data(TRANSACTION_FILE)

    total_balance = Decimal("0.00")
    total_deposits = Decimal("0.00")
    total_withdrawals = Decimal("0.00")
    total_opening = Decimal("0.00")

    for account in accounts:

        total_balance += Decimal(account["balance"])

    for transaction in transactions:

        amount = Decimal(transaction["amount"])

        if transaction["transaction_type"] == "Deposit":

            total_deposits += amount

        elif transaction["transaction_type"] == "Withdrawal":

            total_withdrawals += amount

        elif transaction["transaction_type"] == "Opening Balance":

            total_opening += amount

    print("\n========== LIBERTY BANK REPORT ==========")

    print("Total Registered Customers:", len(customers))
    print("Total Bank Accounts:", len(accounts))
    print("Total Transactions:", len(transactions))

    print("--------------------------------")

    print("Total Opening Balances: $", total_opening)
    print("Total Deposits: $", total_deposits)
    print("Total Withdrawals: $", total_withdrawals)

    print("--------------------------------")

    print("Total Current Account Balances: $", total_balance)

    print("\n========== END OF REPORT ==========")


# ==========================================
# 14. CREATE 30 FICTIONAL DEMONSTRATION RECORDS
# ==========================================

def create_demo_data():

    customers = read_data(CUSTOMER_FILE)
    accounts = read_data(ACCOUNT_FILE)
    transactions = read_data(TRANSACTION_FILE)

    sample_names = [
        "James Cooper", "Mary Johnson", "David Williams",
        "Sarah Brown", "Michael Davis", "Elizabeth Miller",
        "Robert Wilson", "Patricia Moore", "John Taylor",
        "Jennifer Anderson", "William Thomas", "Linda Jackson",
        "Richard White", "Barbara Harris", "Joseph Martin",
        "Susan Thompson", "Thomas Garcia", "Jessica Martinez",
        "Charles Robinson", "Karen Clark", "Daniel Lewis",
        "Nancy Lee", "Matthew Walker", "Lisa Hall",
        "Anthony Allen", "Margaret Young", "Mark King",
        "Sandra Wright", "Donald Scott", "Ashley Green"
    ]

    # Ensure at least 30 customers

    while len(customers) < 30:

        index = len(customers)

        customer_id = generate_id(
            customers, "customer_id", "CUS"
        )

        name = sample_names[index % len(sample_names)]

        customers.append({
            "customer_id": customer_id,
            "name": name,
            "phone": "000-000-" + str(index + 1).zfill(4),
            "email": "customer" + str(index + 1) + "@example.com"
        })

    save_data(CUSTOMER_FILE, CUSTOMER_HEADERS, customers)

    # Ensure at least 30 accounts

    customers_with_accounts = {
        account["customer_id"] for account in accounts
    }

    for customer in customers:

        if len(accounts) >= 30:
            break

        if customer["customer_id"] not in customers_with_accounts:

            account_number = generate_id(
                accounts, "account_number", "ACC"
            )

            opening_balance = Decimal(
                100 + len(accounts) * 10
            ).quantize(Decimal("0.01"))

            accounts.append({
                "account_number": account_number,
                "customer_id": customer["customer_id"],
                "balance": str(opening_balance)
            })

            customers_with_accounts.add(customer["customer_id"])

    save_data(ACCOUNT_FILE, ACCOUNT_HEADERS, accounts)

    # Ensure every account has at least one transaction

    accounts_with_transactions = {
        transaction["account_number"]
        for transaction in transactions
    }

    for account in accounts:

        if account["account_number"] not in accounts_with_transactions:

            transaction_id = generate_id(
                transactions, "transaction_id", "TXN"
            )

            transactions.append({
                "transaction_id": transaction_id,
                "account_number": account["account_number"],
                "transaction_type": "Opening Balance",
                "amount": account["balance"],
                "date": date.today().isoformat()
            })

    save_data(
        TRANSACTION_FILE,
        TRANSACTION_HEADERS,
        transactions
    )

    print("\nDemonstration data is ready.")
    print("Customers:", len(customers))
    print("Accounts:", len(accounts))
    print("Transactions:", len(transactions))


# ==========================================
# 15. MAIN APPLICATION MENU
# ==========================================

def main():

    initialize_files()

    create_demo_data()

    while True:

        print("\n")
        print("==========================================")
        print("          WELCOME TO LIBERTY BANK")
        print("       PYTHON BANKING APPLICATION")
        print("==========================================")

        print("1. Register Customer")
        print("2. View All Customers")
        print("3. Create Bank Account")
        print("4. View Account Balance")
        print("5. Deposit Money")
        print("6. Withdraw Money")
        print("7. Transaction History")
        print("8. Basic Banking Reports")
        print("9. Exit")

        print("==========================================")

        choice = input("Select an option (1-9): ").strip()

        if choice == "1":

            register_customer()

        elif choice == "2":

            view_customers()

        elif choice == "3":

            create_account()

        elif choice == "4":

            view_balance()

        elif choice == "5":

            deposit_money()

        elif choice == "6":

            withdraw_money()

        elif choice == "7":

            transaction_history()

        elif choice == "8":

            basic_reports()

        elif choice == "9":

            print("\nThank you for using Liberty Bank.")
            print("Goodbye!")
            break

        else:

            print("\nInvalid selection.")
            print("Please select a number between 1 and 9.")


# ==========================================
# 16. START THE APPLICATION
# ==========================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print("\nApplication stopped by user.")

    except (OSError, csv.Error) as error:

        print("\nA file operation error occurred:", error)
