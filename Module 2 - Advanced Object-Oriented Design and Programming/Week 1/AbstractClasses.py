# import
from abc import ABC, abstractmethod
import math

# Task 1: Basic Class Hierarchy (Inheritance)
class Vehicle:

    def __init__(self, brand, fuel_type):
        self.brand = brand
        self.fuel_type = fuel_type

class Car(Vehicle):
    def __init__(self, brand, fuel_type, num_doors):
        super().__init__(brand, fuel_type)
        self.num_doors = num_doors


# Task 2: Polymorphism with Methods

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * (self.radius**2)

    def __str__(self):
        return f'Circle with radius {self.radius}'

# Rectangle Subclass
class Rectangle(Shape):
    def __init__(self, width, length):
        self.width = width
        self.length = length

    def area(self):
        return self.width * self.length

    def __str__(self):
        return f'Rectangle with width {self.width} with length {self.length}'

# Task 3: Encapsulation with Access Control
class BankAccount:
    def __init__(self, __balance):
        self.__balance = __balance #private variable

    def deposit(self, amount):
        self.__balance += amount

    def withdraw(self, amount):
        self.__balance -= amount

    def get_balance(self):
        return self.__balance

#Task 4: Abstraction with Base Class
class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        pass

class Dog(Animal):
    def make_sound(self):
        return 'Woof!'

class Cat(Animal):
    def make_sound(self):
        return 'Meow!'

# Task 5: Constructor and Destructor
class Person:
    def __init__(self, name):
        self.name = name

    def __del__(self):
        print('Goodbye, {name}!')

Person1 = Person('Bob')
Person2 = Person('Alice')
Person3 = Person('Charlotte')
del Person1
del Person2
del Person3
