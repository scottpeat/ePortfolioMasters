# Unit 3 – Factory Method Design Pattern

## Purpose of the Task
The goal of this task was to implement the **Factory Method** creational design pattern. We were asked to design a system for a fictional car manufacturing company that can create different types of cars without the main program needing to know the exact class being instantiated.

## OOP Concepts Demonstrated
- **Abstraction** (using an abstract base class)
- **Inheritance**
- **Polymorphism**
- **Creational Design Pattern** – Factory Method

## Code Structure
- `CarFactory` – Abstract base class
- `SedanFactory`, `SUVFactory`, `SportsCarFactory` – Concrete factory classes
- `Car` – Abstract product class
- `Sedan`, `SUV`, `SportsCar` – Concrete product classes

## What the Code Achieves
- Allows easy creation of different car types through factory classes
- Follows the **Open-Closed Principle** – new car types can be added without modifying existing code
- Demonstrates how the Factory Method pattern provides a clean and extensible way to create objects

## Key Learning
This exercise helped me understand how to use abstraction and inheritance effectively to create flexible object creation systems.

## Files
- `FactoryAbstract.py` – Main implementation & Demonstration of the pattern in action

---

**Status:** Completed ✅