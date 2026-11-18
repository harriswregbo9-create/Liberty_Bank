# Liberty Bank – Banking Application

## Project Overview

Liberty Bank is a simple console-based banking application developed using Python 3. It simulates basic banking operations for educational purposes.

The application allows users to register customers, create bank accounts, check account balances, deposit money, withdraw money, and view transaction histories.

**Important:** This application is an educational simulation only. It is not a real banking system and must not be used to store real financial information.

## Technologies Used

- Python 3
- CSV file storage
- Python built-in `csv` module

## Main Features

1. Customer registration and customer records.
2. Unique customer identification numbers.
3. Bank account creation with unique account numbers.
4. Account balance inquiry.
5. Cash deposits.
6. Cash withdrawals.
7. Withdrawal protection against insufficient funds.
8. Transaction history for each account.
9. Unique transaction identification numbers.
10. Transaction dates and basic transaction reports.
11. Automatic saving of records using CSV files.

## Project Files

- `banking.py` – Main Python application.
- `customers.csv` – Stores customer information.
- `accounts.csv` – Stores bank account information and balances.
- `transactions.csv` – Stores transaction records.

## Installation and Execution

1. Install Python 3.
2. Open the project folder in Visual Studio Code.
3. Open the terminal.
4. Run the following command:

```bash
python banking.py
```

Alternatively:

```bash
py banking.py
```

5. Follow the options displayed in the application menu.

## Data Storage

The application stores customer, account, and transaction information in CSV files. Records remain available after closing and restarting the application.

## Testing

The application was tested for:

- Customer registration.
- Account creation.
- Balance inquiry.
- Successful deposits.
- Successful withdrawals.
- Rejection of withdrawals exceeding the available balance.
- Rejection of invalid transaction amounts.
- Transaction history.
- Data persistence after restarting the application.

## Educational Purpose

This project demonstrates basic Python programming concepts, including functions, loops, conditional statements, data validation, file handling, and CSV data storage.

**Developed as an academic project for INFO 301.**