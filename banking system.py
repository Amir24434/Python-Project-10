"""
Simple Banking System Project
-----------------------------
This project is a console-based banking application that allows users to:

1. Create an account
2. Login to an existing account
3. Deposit money
4. Withdraw money
5. Check account balance
6. View transaction history

Account data is stored in a JSON file (`accounts.json`).

Author: Abdulsobur Adegboyega
"""

from datetime import datetime
import os
import json
import hashlib



class BankSystem:
    """
    A simple banking system class for handling user accounts,
    deposits, withdrawals, and transaction history.
    """

    def __init__(self, balance=0, trans_hist=None):
        """
        Initialize the bank system.

        Args:
            balance (float): Starting account balance.
            trans_hist (list): Transaction history list.
        """
        self.balance = balance

        # If no transaction history is provided,
        # initialize with an empty list.
        self.trans_hist = trans_hist if trans_hist is not None else []

    def load_Database(self):
        """
        Load account data from the JSON database file.

        Returns:
            dict: Account data dictionary.
        """
        filename = "accounts.json"

        # Check if the file exists
        if os.path.exists(filename):
            try:
                with open(filename, "r") as file:
                    return json.load(file)

            # Handle invalid or empty JSON files
            except json.JSONDecodeError:
                return {}

        # Return an empty dictionary if file does not exist
        return {}

    def create_account(self, name, password):
        """
        Create a new user account.

        Args:
            name (str): Username.
            password (str): User password.
        """

        self.name = name
        self.password = hash_password(password)

        # Load existing data
        with open("accounts.json", "r") as file:
            data = json.load(file)

        # Create new account structure
        data[name] = {
            "password": self.password,
            "balance": self.balance,
            "transactions": self.trans_hist,
        }

        # Save updated data back to file
        with open("accounts.json", "w") as file:
            json.dump(data, file, indent=4)

    def login(self, name, password):
        """
        Authenticate a user login.

        Args:
            name (str): Username.
            password (str): Password.

        Returns:
            bool: True if login is successful, otherwise False.
        """

        self.name = name
        self.password = hash_password(password)

        # Load account data
        with open("accounts.json", "r") as file:
            data = json.load(file)

        # Verify username and password
        if self.name in data and data[self.name]["password"] == self.password:
            print("Login successful!")
            print(f"Welcome back, {self.name}!")
            return True

        else:
            print("Incorrect username or password!")
            return False

    def deposit(self, amount):
        """
        Deposit money into the user's account.

        Args:
            amount (float): Amount to deposit.
        """

        # Update object balance
        self.balance += amount

        # Generate timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save transaction
        self.trans_hist.append(
            f"Deposit of {amount} on {timestamp}"
        )

        # Load database
        with open("accounts.json", "r") as file:
            data = json.load(file)

        # Update stored balance
        data[self.name]["balance"] += self.balance

        # Add transaction to history
        data[self.name]["transactions"].extend(self.trans_hist)

        # Save updated data
        with open("accounts.json", "w") as file:
            json.dump(data, file, indent=4)

    def withdraw(self, amount):
        """
        Withdraw money from the user's account.

        Args:
            amount (float): Amount to withdraw.
        """

        # Load account data
        with open("accounts.json", "r") as file:
            data = json.load(file)

        # Check if sufficient balance exists
        if data[self.name]["balance"] >= amount:

            # Generate timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Save transaction
            self.trans_hist.append(
                f"Withdrawal of {amount} on {timestamp}"
            )

            # Deduct amount from balance
            data[self.name]["balance"] -= amount

            # Update transaction history
            data[self.name]["transactions"].extend(self.trans_hist)

            # Save updated data
            with open("accounts.json", "w") as file:
                json.dump(data, file, indent=4)

                # Extra transaction tuple
                self.trans_hist.append(
                    ("withdraw", amount, timestamp)
                )

        else:
            print("Insufficient funds!")

    def check_balance(self):
        """
        Check the current account balance.

        Returns:
            float: Current account balance.
        """

        with open("accounts.json", "r") as file:
            data = json.load(file)

            return data[self.name]['balance']

    def view_transaction_history(self):
        """
        Display all transactions made by the user.
        """

        with open("accounts.json", "r") as file:
            data = json.load(file)

            trans_data = data[self.name]['transactions']

        # Print transaction list
        for index, transaction in enumerate(trans_data, start=1):
            print(f"{index}. {transaction}")
            
            
    def transfer(self, recipient, amount):
        """
        Transfer money from current user to another user.
        """

        with open("accounts.json", "r") as file:
            data = json.load(file)

        # Check recipient exists and is not sender
        if recipient not in data or recipient == self.name:
            print("Recipient account does not exist!")
            return

        # Check balance
        if data[self.name]["balance"] < amount:
            print("Insufficient funds for transfer!")
            return

        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Deduct and add balances
        data[self.name]["balance"] -= amount
        data[recipient]["balance"] += amount

        # Sender transaction
        sender_tx = f"Transfer of {amount} to {recipient} on {timestamp}"
        data[self.name]["transactions"].append(sender_tx)

        # Recipient transaction
        recipient_tx = f"Transfer of {amount} from {self.name} on {timestamp}"
        data[recipient]["transactions"].append(recipient_tx)

        # Save changes
        with open("accounts.json", "w") as file:
            json.dump(data, file, indent=4)

        print("Transfer successful!")
        
    
    


# Create bank system object
bank = BankSystem()

# Load existing account data
load = bank.load_Database()


def new_choice():
    """
    Ask the user whether they want to continue.
    """

    new_choice = input(
        "Do you still want to perform more task? (y/n): "
    )

    if new_choice.lower() != "y":
        exit()


def hash_password(password):
    """
    Convert password into a hashed string.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def perform_task():
    """
    Display banking options and perform selected operations.
    """

    print("Select an option to proceed.")

    choice = input(
        "1. Deposit\n"
        "2. Withdraw\n"
        "3. Transfer\n"
        "4. View Balance\n"
        "5. View Transaction History\n"
        "6. Exit\n"
        "Enter your choice: "
    )

    # Deposit option
    if choice == "1" or choice == "Deposit".lower():

        amount = float(input("Enter the amount to deposit: "))

        bank.deposit(amount)

        print(f"Deposited ${amount} successfully!")

        new_choice()

    # Withdraw option
    elif choice == "2" or choice == "Withdraw".lower():

        amount = float(input("Enter the amount to withdraw: "))

        bank.withdraw(amount)

        new_choice()
        
    # Transfer option
    elif choice == "3" or choice == "Transfer".lower():

        recipient = input("Enter the recipient's username: ")

        amount = float(input("Enter the amount to transfer: "))

        bank.transfer(recipient, amount)
        if True:
            print(f"Transferred ${amount} to {recipient} successfully!")
            
        else:
            print("Transfer failed!")

        new_choice()

    # View balance option
    elif choice == "4" or choice == "View Balance".lower():

        balance = bank.check_balance()

        print(f"Your current balance is: ${balance}")

        new_choice()

    # View transaction history option
    elif choice == "5" or choice == "View Transaction History".lower():

        print("Transaction History:")

        bank.view_transaction_history()

        new_choice()

    # Exit option
    elif choice == "6" or choice == "Exit".lower():

        print("Thank you for using our banking system. Goodbye!")

        exit()


# Main program loop
while True:

    choice = input(
        "What do you want to do? \n"
        "1. Create an Account. \n"
        "2. Login. \n"
        "Enter your choice: "
    )

    # Create account option
    if choice == "1" or choice == "Create an account".lower():

        print("Create an account here.")

        username = input("Enter your name: ")

        # Check if user already exists
        if username in load:

            print("You already have an account with us!")

            print("Login to your account here.")

            while True:

                password = input("Enter your password: ")

                if bank.login(username, password) is True:

                    while True:
                        perform_task()

                else:
                    continue

        # Create new account
        else:

            password = input("Enter your password: ")

            bank.create_account(username, password)

            print(
                "Account created successfully! "
                "You have been successfully logged in."
            )

            # Reload updated database
            load = bank.load_Database()

            while True:
                perform_task()

    # Login option
    elif choice == "2" or choice == "Login".lower():

        print("Welcome back!")

        username = input("Enter your name: ")

        # Check if account exists
        if username not in load:

            print(
                "You don't have an account with us! "
                "Please create an account first."
            )

        else:

            while True:

                password = input("Enter your password: ")

                if bank.login(username, password) is True:

                    print(f"Welcome back {username}!")

                else:
                    continue

                while True:
                    perform_task()

    # Invalid input
    else:
        print("Invalid input!")
        continue