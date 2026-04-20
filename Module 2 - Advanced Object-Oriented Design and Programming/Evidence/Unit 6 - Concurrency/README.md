# Unit 6: Thread-Safe Bank Account System

## Project Overview
This project implements a **thread-safe Bank Account system** in Python. The system allows multiple users to perform concurrent transactions (deposit, withdraw, and check balance) on the same bank account without causing race conditions or data inconsistencies.

The main goal of this assignment was to demonstrate understanding of **concurrency control**, **thread safety**, and how to integrate these concepts with object-oriented design.

## Features
- Thread-safe `BankAccount` class with deposit, withdraw, and get_balance methods
- Protection against race conditions using `threading.Lock()`
- `TransactionSimulator` class to simulate multiple users performing concurrent transactions
- Deadlock prevention mechanisms
- Proper error handling for insufficient funds
- Unit tests to validate thread safety

## Key Learning Outcomes
- Understanding and implementing thread safety in Python
- Using synchronisation mechanisms (`threading.Lock`)
- Preventing race conditions in shared resources
- Combining OOP principles with concurrency
- Testing concurrent applications

## Project Structure