#-----------------------------------------------------------------------------------------
""" Importing the Abstract base class"""
#-----------------------------------------------------------------------------------------

from abc import ABC, abstractmethod

#-----------------------------------------------------------------------------------------
"""1. Abstract class representing a car."""
"""This ensures all concrete car classes implement the drive method."""
#-----------------------------------------------------------------------------------------
class Car(ABC):
    @abstractmethod
    def drive(self):
        pass
#-----------------------------------------------------------------------------------------
"""2. Implementing concrete car classes that inherit from the abstract Car class."""
#-----------------------------------------------------------------------------------------

class Sedan(Car):
    def drive(self):
        return "I am driving an sedan.  I am comfortable and fuel efficient."

class SUV(Car):
    def drive(self):
        return "I am driving an SUV.  I am spacious and powerful."
    
class Hatchback(Car):
    def drive(self):
        return "I am driving a hatchback.  I am compact and easy to park."  

#-----------------------------------------------------------------------------------------
"""3. Abstract factory class for creating cars with own create_car method."""
#-----------------------------------------------------------------------------------------
class CarFactory(ABC):
    @abstractmethod
    def create_car(self):
        pass
#-----------------------------------------------------------------------------------------
"""4. Concrete factory classes for each type of car."""
#-----------------------------------------------------------------------------------------      
class SedanFactory(CarFactory):
    def create_car(self):
        return Sedan()

class SUVFactory(CarFactory):
    def create_car(self):
        return SUV()
    
class HatchbackFactory(CarFactory):
    def create_car(self):
        return Hatchback()          
#-----------------------------------------------------------------------------------------
"""5. Demonstration of the Factory Method pattern."""
#-----------------------------------------------------------------------------------------
if __name__ == "__main__":
    
    sedan_factory = SedanFactory()
    sedan = sedan_factory.create_car()
    print(sedan.drive())

    suv_factory = SUVFactory()
    suv = suv_factory.create_car()
    print(suv.drive())
    
    hatchback_factory = HatchbackFactory()
    hatchback = hatchback_factory.create_car()
    print(hatchback.drive())
