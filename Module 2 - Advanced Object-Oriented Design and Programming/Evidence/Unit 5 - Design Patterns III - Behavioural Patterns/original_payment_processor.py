class PaymentProcessor:
    def process_payment(self, payment_type, amount):
        if payment_type == "credit_card":
            print(f"Processing credit card payment of ${amount}")
        elif payment_type == "paypal":
            print(f"Processing PayPal payment of ${amount}")
        elif payment_type == "bank_transfer":
            print(f"Processing bank transfer of ${amount}")
        else:
            raise ValueError("Invalid payment type")