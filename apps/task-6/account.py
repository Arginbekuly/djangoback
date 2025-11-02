# account.py

class Account:
    def __init__(self, account_number, owner, balance=0):
        self.account_number = account_number
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"{amount} deposited. New balance: {self.balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"{amount} withdrawn. New balance: {self.balance}")
        else:
            print("Invalid withdrawal amount.")

    def get_details(self):
        return f"Account: {self.account_number}, Owner: {self.owner}, Balance: {self.balance}"

class SavingsAccount(Account):
    def __init__(self, account_number, owner, balance=0, interest_rate=0.03):
        super().__init__(account_number, owner, balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        print(f"Interest applied: {interest}. New balance: {self.balance}")

class CheckingAccount(Account):
    def __init__(self, account_number, owner, balance=0, fee=5):
        super().__init__(account_number, owner, balance)
        self.fee = fee

    def deduct_fee(self):
        if self.balance >= self.fee:
            self.balance -= self.fee
            print(f"Fee deducted: {self.fee}. New balance: {self.balance}")
        else:
            print("Not enough balance to deduct fee.")

if __name__ == "__main__":
    acc = SavingsAccount("001", "Alice", 1000)
    acc.deposit(200)
    acc.apply_interest()
    print(acc.get_details())
