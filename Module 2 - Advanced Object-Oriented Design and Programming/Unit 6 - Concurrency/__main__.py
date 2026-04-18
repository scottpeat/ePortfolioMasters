from bank_account import BankAccount
from bank_account import TransactionSimulator

# Example usage
if __name__ == "__main__":
    account = BankAccount("1234567890", 1000.00)  # Create a bank account with an initial balance of £1000
    simulator = TransactionSimulator(account)  # Create a transaction simulator for the account
    simulator.run_simulation()  # Run the simulation of transactions