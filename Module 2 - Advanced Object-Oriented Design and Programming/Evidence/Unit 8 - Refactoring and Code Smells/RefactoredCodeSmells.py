# Unit 8 - Refactoring and Code Smells
# This code has been refactored to remove code smells and improve readability and maintainability.
# I have decided to use the Strategy design pattern to handle different discount strategies for a shopping cart.

# importing abstract base class for creating abstract classes
from abc import ABC, abstractmethod

# Base class for items in the shopping cart
class DiscountStrategy(ABC):
    @abstractmethod
    def calculate_discount(self, price):
        pass

# Concrete strategy for no book discount
class NoDiscount(DiscountStrategy):
    def calculate_discount(self, price):
        return price

# Concrete strategy for book discount
class BookDiscount(DiscountStrategy):
    def calculate_discount(self, price):
        return price * 0.9 # 10% discount for books

# Concrete strategy for electronics discount
class ElectronicsDiscount(DiscountStrategy):
    def calculate_discount(self, price):
        return price * 0.8 # 20% discount for electronics

# Dictionary to hold the discount strategies for different item types
DISCOUNT_STRATEGIES = {
    'book': BookDiscount(),
    'electronics': ElectronicsDiscount(),
}

# Refactored function to calculate total price using the strategy pattern
def calculate_total_price(items):
    total = 0
    for item in items:  # Loop through each item in the shopping cart
        discount_strategy = DISCOUNT_STRATEGIES.get(item['type'], NoDiscount())
        total += discount_strategy.calculate_discount(item['price'])
    return total

# Example usage
if __name__ == "__main__":
    
    # Sample items in the shopping cart
    items = [
        {'type': 'book', 'price': 100},
        {'type': 'electronics', 'price': 200},
        {'type': 'clothing', 'price': 50}
    ]
    total_price = calculate_total_price(items)
    print(f"Total price after discounts: ${total_price:.2f}")

