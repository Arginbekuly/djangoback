# bank.py

from account import SavingsAccount, CheckingAccount

class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = []
#Changed
    def add_account(self, account):
        self.accounts.append(account)
        print(f"Account {account.account_number} added.'changing'")

    def find_account(self, account_number):
        for acc in self.accounts:
            if acc.account_number == account_number:
                return acc
        return None

    def deposit_to_account(self, account_number, amount):
        acc = self.find_account(account_number)
        if acc:
            acc.deposit(amount)
        else:
            print("Account not found.")

    def withdraw_from_account(self, account_number, amount):
        acc = self.find_account(account_number)
        if acc:
            acc.withdraw(amount)
        else:
            print("Account not found.")

    def show_all_accounts(self):
        if not self.accounts:
            print("No accounts in the bank.")
        for acc in self.accounts:
            print(acc.get_details())

if __name__ == "__main__":
    bank = Bank("AI Bank")
    acc1 = SavingsAccount("100", "John", 500)
    acc2 = CheckingAccount("101", "Jane", 1000)

    bank.add_account(acc1)
    bank.add_account(acc2)

    bank.deposit_to_account("100", 200)
    bank.withdraw_from_account("101", 300)

    bank.show_all_accounts()
