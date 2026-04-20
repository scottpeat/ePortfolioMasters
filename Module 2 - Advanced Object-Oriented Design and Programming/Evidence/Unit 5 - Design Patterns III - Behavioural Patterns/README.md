Markdown# Unit 5: Design Patterns III - Behavioural Patterns

## Overview
This repository contains my work for **Unit 5: Behavioural Design Patterns**. The main task was to analyse a poorly designed payment processing system and refactor it using the **Strategy Pattern**.

## Task Summary
The original code used a long if-elif chain inside the `PaymentProcessor` class to handle different payment methods (Credit Card, PayPal, Bank Transfer). This design violated the **Open/Closed Principle** and made the code difficult to maintain and extend.

The goal was to:
- Identify the problems in the original implementation
- Refactor the code using the **Strategy Pattern**
- Discuss the benefits of this refactoring

## Refactored Code (Using Strategy Pattern)

The refactored solution separates each payment method into its own strategy class. This makes the code much cleaner, more extensible, and easier to maintain.

### Key Improvements:
- Each payment method is now in its own class (`CreditCardPayment`, `PayPalPayment`, `BankTransferPayment`)
- `PaymentProcessor` depends on the `PaymentStrategy` abstraction instead of concrete logic
- New payment methods can be added without modifying existing code (Open/Closed Principle)

## Files
- `payment_processor.py` – Contains the Strategy Pattern implementation
- `original_payment_processor.py` – Original version (for comparison)

## What I Learned
- How the Strategy Pattern helps encapsulate varying behaviour
- The importance of the Open/Closed Principle in real code
- How behavioural patterns improve flexibility and maintainability
- Better separation of concerns in object-oriented design

This exercise was very useful in understanding how design patterns can solve common maintainability problems in software development.

---