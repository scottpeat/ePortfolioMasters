from abc import ABC, abstractmethod


# Strategy Design Pattern
class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

# concrete strategy for credit card payment
class CreditCardPayment(PaymentStrategy):
    def process_payment(self, amount):
        print(f"Processing credit card payment of £{amount}")
    
# concrete strategy for PayPal payment
class PayPalPayment(PaymentStrategy):
    def process_payment(self, amount):
        print(f"Processing PayPal payment of £{amount}")

# crypto strategy for cryptocurrency payment
class CryptoPayment(PaymentStrategy):
    def process_payment(self, amount):
        print(f"Processing cryptocurrency payment of £{amount}")

# Context class that uses the payment strategy
class PaymentProcessor:
    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def process_payment(self, amount):
        return self._strategy.process_payment(amount)

# Example usage
if __name__ == "__main__":
    # Create a payment processor with a credit card strategy
    processor = PaymentProcessor(CreditCardPayment())
    processor.process_payment(100)

    # Change the strategy to PayPal
    processor.set_strategy(PayPalPayment())
    processor.process_payment(200)

    # Change the strategy to cryptocurrency
    processor.set_strategy(CryptoPayment())
    processor.process_payment(300)