from datetime import datetime


class BankAccount:
    
    def __init__(self, name, balance=0, trans_hist=[]):
        self.name = name
        self.balance = balance
        self.trans_hist = trans_hist
        
    def deposit(self, amount):
        self.balance += amount
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.trans_hist.append(f"Deposit of {amount} at {timestamp}")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.trans_hist.append(f"Withdrawal of {amount} at {timestamp}")
        else:
            print("Account is too low for this withdrawal.")

    def view_balance(self):
        return self.balance
    
    def view_transaction_history(self):
       return self.trans_hist

    
print("Welcome to Amir Banking")
print("Create an account to get started.")
user = input("Enter your name: ")
account = BankAccount(user)
print(f"{user}! Welcome to Amir Banking. Your account has been created.")

while True:
    print("1. Deposit")
    print("2. Withdraw")
    print("3. View Balance")
    print("4. View Transaction History")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        amount = float(input("Enter amount to deposit: "))
        account.deposit(amount)
        print(f"Deposited {amount}. New balance: {account.view_balance()}")

    elif choice == '2':
        amount = float(input("Enter amount to withdraw: "))
        account.withdraw(amount)

    elif choice == '3':
        print(f"Current balance: {account.view_balance()}")

        break
    elif choice == '4':
        print("Transaction History:")
        for index, transaction in enumerate(account.view_transaction_history(), start=1):
            print(f"{index}. {transaction}")

    elif choice == '5':
        print("Thank you for using the Banking System. Goodbye!")            

    else:
        print("Invalid choice. Please try again.")
        
    again = input(("Do you want to perform another operation? (yes/no): "))
    if again.lower() != 'yes':
        print("Thank you for using the Banking System. Goodbye!")
        exit()