from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def name(self, name):
        pass

class CreditCardPayment(PaymentMethod):
    def name(self, name):
        return f"Processing payment with {name}."

class PayPalPayment(PaymentMethod):
    def name(self, name):
        return f"Processing payment with {name}."

class CryptoPayment(PaymentMethod):
    def name(self, name):
        return f"Processing payment with {name}."


class PaymentProcessor:
    def __init__(self, payment_method: PaymentMethod) -> None:
        self.payment_method = payment_method
        

    def process_payment(self, name):
        return self.payment_method.name(name)


class Order:
    def __init__(self, ):
        self.items = []
    def add_item(self, item):
        self.items.append(item)
    
    def calculate_total(self):
        return sum(item.price for item in self.items)

