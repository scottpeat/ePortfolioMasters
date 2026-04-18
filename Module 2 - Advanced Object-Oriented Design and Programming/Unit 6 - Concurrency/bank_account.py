
import threading # Importing threading module to ensure thread safety when modifying balance
import time  # Importing time module for simulating delays in transactions
import random  # Importing random module for simulating random transaction amounts
from concurrent.futures import ThreadPoolExecutor, as_completed  # Importing ThreadPoolExecutor for managing threads in tests

class BankAccount:
    def __init__(self, account_number: str, initial_balance: float = 0.0):
        self.__account_number = str(account_number)          # ensure it's always str
        self.__balance = float(initial_balance)              # ensure float
        self.__lock = threading.Lock()                       # correct placement

    def deposit(self, amount: float) -> None:
        """Deposits a positive amount to the account balance."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        
        with self.__lock:
            self.__balance += amount
            new_balance = self.__balance  # snapshot while still holding lock

        # Printing/logging should be done OUTSIDE the lock
        print(f"Deposited £{amount:,.2f}. New balance: £{new_balance:,.2f}")
``
    def withdraw(self, amount: float) -> None:
        """Withdraws a positive amount if sufficient funds are available."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        
        with self.__lock:
            if amount > self.__balance:
                raise ValueError("Insufficient funds.")
            
            self.__balance -= amount
            new_balance = self.__balance  # snapshot under lock

        print(f"Withdrew £{amount:,.2f}. New balance: £{new_balance:,.2f}")

    def get_balance(self) -> float:
        """Returns the current balance of the account (thread-safe)."""
        with self.__lock:
            return self.__balance

    def get_account_number(self) -> str:
        """Returns the account number (thread-safe)."""
        with self.__lock:
            return self.__account_number

    def __str__(self) -> str:
        """String representation with masked account number."""
        with self.__lock:
            masked = "X" * (len(self.__account_number) - 4) + self.__account_number[-4:] \
                if len(self.__account_number) >= 4 else self.__account_number
            balance = self.__balance
        return f"Account {masked} | Balance: £{balance:,.2f}"  


class TransactionSimulator:
    """Simulates multiple users performing transactions on a shared BankAccount instance to test thread safety."""
    def __init__(self, account: BankAccount, num_users=5, num_transactions=10):
        self.account = account 
        self.num_users = num_users
        self.num_transactions = num_transactions
    
    def user_work(self, user_id):
        """Simulates a user performing a series of random deposits and withdrawals."""
        for _ in range(self.num_transactions):
            action = random.choice(['deposit', 'withdraw'])
            amount = round(random.uniform(1, 100), 2)  # Random amount between £1 and £100
            try:
                if action == 'deposit':
                    self.account.deposit(amount)
                else:
                    self.account.withdraw(amount)
            except ValueError as e:
                print(f"User {user_id}: {e}")
            time.sleep(random.uniform(0.1, 0.5))  # Simulate delay between transactions
    
    def run_simulation(self):
        """Starts the simulation with multiple threads representing different users."""
        print("Before simulation:")
        print(self.account)           
        print("-" * 50)

        threads = []
        for i in range(1, self.num_users + 1):
            t = threading.Thread(target=self.user_work, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print("-" * 50)
        print("After simulation:")
        print(self.account)  