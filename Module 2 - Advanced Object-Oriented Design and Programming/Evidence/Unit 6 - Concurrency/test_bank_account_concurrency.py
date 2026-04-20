import unittest # For unit testing
import threading
import random
from concurrent.futures import ThreadPoolExecutor, as_completed # For managing threads in tests


class BankAccount:
    def __init__(self, account_number: str, initial_balance: float = 0.0):
        self.__account_number = account_number
        self.__balance = initial_balance
        self.__lock = threading.Lock()  # For thread safety

    def deposit(self, amount: float) -> None:
        """Deposits a positive amount to the account balance."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        with self.__lock:
            self.__balance += amount
            new_balance = self.__balance
        print(f"Deposited £{amount:,.2f}. New balance: £{new_balance:,.2f}")

    def withdraw(self, amount: float) -> None:
        """Withdraws a positive amount if sufficient funds are available."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        with self.__lock:
            if amount > self.__balance:
                print("Insufficient funds or invalid amount.")
                raise ValueError("Insufficient funds.")
            self.__balance -= amount
            new_balance = self.__balance
        print(f"Withdrew £{amount:,.2f}. New balance: £{new_balance:,.2f}")

    def get_balance(self) -> float:
        with self.__lock:
            return self.__balance

    def get_account_number(self) -> str:
        with self.__lock:
            return self.__account_number

    def __str__(self):
        with self.__lock:
            masked = "X" * (len(str(self.__account_number)) - 4) + str(self.__account_number)[-4:] \
                if len(str(self.__account_number)) >= 4 else str(self.__account_number)
            balance = self.__balance
        return f"Account {masked} | Balance: £{balance:,.2f}"


# ── Unit Tests ─────────────────────────────────────────────────────────────

class TestBankAccount(unittest.TestCase):

    def setUp(self):
        """Create a fresh account before each test"""
        self.account = BankAccount("123456789012", 2000.00)

    # ── Basic functionality ────────────────────────────────────────────────


    # ── Concurrency / Thread-safety tests ──────────────────────────────────

    def test_concurrent_deposits_no_lost_updates(self):
        initial = self.account.get_balance()
        added = 0.0

        def worker():
            nonlocal added
            for _ in range(300):
                amt = round(random.uniform(5.0, 40.0), 2)
                self.account.deposit(amt)
                added += amt

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        final = self.account.get_balance()
        self.assertAlmostEqual(
            final,
            initial + added,
            delta=0.1,
            msg=f"Deposits mismatch: expected ~{initial + added:.2f}, got {final:.2f}"
        )


if __name__ == '__main__':
    unittest.main(verbosity=1)