from datetime import datetime
import json
import os

class BankAccount:

    def __init__(self, name, balance=0, trans_hist=None):
        self.name = name
        self.balance = balance
        self.trans_hist = trans_hist if trans_hist is not None else []

    def deposit(self, amount):
        self.balance += amount
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.trans_hist.append(f"Deposit of {amount} on {timestamp}")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.trans_hist.append(f"Withdrawal of {amount} on {timestamp}")
        else:
            print("Account balance is too low for this withdrawal.")

    def view_balance(self):
        return self.balance

    def view_transaction_history(self):
        return self.trans_hist

    def to_dict(self):
        return {
            "name": self.name,
            "balance": self.balance,
            "transactions": self.trans_hist
        }

   
    
    def save_data(self):
        filename = "accounts.json"

        # 1. Load existing data
        if os.path.exists(filename):
            with open(filename, "r") as file:
                try:
                    data = json.load(file)
                    if not isinstance(data, list):
                        data = []
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        # 2. Check if user already exists
        for account in data:
            if account["name"] == self.name:
                # update existing account
                account["balance"] = self.balance

                # merge transactions (IMPORTANT PART)
                account["transactions"].extend(self.trans_hist)
                break
        else:
            # user not found → create new account
            data.append(self.to_dict())

        # 3. Save back to file
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)


print("Welcome to Amir Banking")
print("Create an account to get started.")

user = input("Enter your name: ")

account = BankAccount(user)

print(f"{user}! Welcome to Amir Banking. Your account has been created.")

while True:

    print("\n1. Deposit")
    print("2. Withdraw")
    print("3. View Balance")
    print("4. View Transaction History")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        amount = float(input("Enter amount to deposit: "))
        account.deposit(amount)

        print(f"Deposited {amount}")
        print(f"New balance: {account.view_balance()}")

    elif choice == '2':
        amount = float(input("Enter amount to withdraw: "))
        account.withdraw(amount)

    elif choice == '3':
        print(f"Current balance: {account.view_balance()}")

    elif choice == '4':
        print("Transaction History:")

        for index, transaction in enumerate(account.view_transaction_history(), start=1):
            print(f"{index}. {transaction}")

    elif choice == '5':
        account.save_data()

        print("Thank you for using the Banking System. Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")

    again = input("Do you want to perform another operation? (yes/no): ")

    if again.lower() != 'yes':
        account.save_data()

        print("Thank you for using the Banking System. Goodbye!")
        break



