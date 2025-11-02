# main.py

from bank import Bank
from account import SavingsAccount, CheckingAccount

def display_menu():
    print("\n=== Bank Management System ===")
    print("1. Create Savings Account")
    print("2. Create Checking Account")
    print("3. Deposit Money")
    print("4. Withdraw Money")
    print("5. Show All Accounts")
    print("6. Exit")

def main():
    bank = Bank("ChatGPT Bank")

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            acc_num = input("Enter account number: ")
            owner = input("Enter owner name: ")
            balance = float(input("Enter initial balance: "))
            acc = SavingsAccount(acc_num, owner, balance)
            bank.add_account(acc)

        elif choice == "2":
            acc_num = input("Enter account number: ")
            owner = input("Enter owner name: ")
            balance = float(input("Enter initial balance: "))
            acc = CheckingAccount(acc_num, owner, balance)
            bank.add_account(acc)

        elif choice == "3":
            acc_num = input("Account number: ")
            amount = float(input("Amount to deposit: "))
            bank.deposit_to_account(acc_num, amount)

        elif choice == "4":
            acc_num = input("Account number: ")
            amount = float(input("Amount to withdraw: "))
            bank.withdraw_from_account(acc_num, amount)

        elif choice == "5":
            bank.show_all_accounts()

        elif choice == "6":
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()
