
import threading # Importing threading module to ensure thread safety when modifying balance

class BankAccount: 
    def __init__(self, account_number: str, initial_balance: float = 0.0):
        self.__balance = initial_balance  
        self.__lock = threading.Lock()  
    
    # Bank Account Logic
    # the only ways to change balance no setters, 
    # only these methods can modify the balance

    def deposit(self, amount: float) -> None:  # Expects Float for currency handling, returns None since it modifies state but doesn't return a value
        """Deposits a positive amount to the account balance. Raises ValueError for non-positive amounts."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        with self.__lock:  # Ensure thread-safe modification of balance
            self.__balance += amount
            new_balance = self.__balance  # Store new balance for printing after releasing lock
            print(f"Deposited £{amount:,.2f}. New balance: £{new_balance:,.2f}")

    def withdraw(self, amount: float) -> None:  
        """Withdraws a positive amount from the account balance if sufficient funds are available. Raises ValueError for non-positive amounts."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        with self.__lock:  # Ensure thread-safe modification of balance
            if amount > self.__balance:
                print("Insufficient funds or invalid amount.")
                raise ValueError("Insufficient funds.")
            self.__balance -= amount
            new_balance = self.__balance  # Store new balance for printing after releasing lock
            print(f"Withdrew £{amount:,.2f}. New balance: £{new_balance:,.2f}")

    # String representation of the account, masking all but the last 4 digits of the account number for security
    def __str__(self):
        with self.__lock:  # Ensure thread-safe read of account number and balance for string representation
            masked = "X" * (len(str(self.__account_number)) - 4) + str(self.__account_number)[-4:]
            return f"Account {masked} | Balance: £{self.__balance:,.2f}"   




    

    
