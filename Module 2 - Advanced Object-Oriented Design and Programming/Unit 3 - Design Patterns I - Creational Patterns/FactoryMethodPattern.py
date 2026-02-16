"""
Factory Method Pattern: Car Creation System
This module demonstrates the Factory Method Pattern for creating different types of cars
without hardcoding their classes in the main program.
"""

from abc import ABC, abstractmethod


# ============================================================================
# STEP 1: Define the Car Interface/Abstract Class
# ============================================================================

class Car(ABC):
    """Abstract base class representing a car."""
    
    @abstractmethod
    def drive(self):
        """Abstract method that all concrete car classes must implement."""
        pass


# ============================================================================
# STEP 2: Implement Concrete Car Classes
# ============================================================================

class Sedan(Car):
    """Concrete class representing a Sedan."""
    
    def drive(self):
        return "🚗 Driving a Sedan: Smooth and comfortable ride on highways."


class SUV(Car):
    """Concrete class representing an SUV."""
    
    def drive(self):
        return "🚙 Driving an SUV: Powerful and excellent off-road capability."


class Hatchback(Car):
    """Concrete class representing a Hatchback."""
    
    def drive(self):
        return "🚕 Driving a Hatchback: Compact and great for city driving."


# ============================================================================
# STEP 3: Define the CarFactory Abstract Class
# ============================================================================

class CarFactory(ABC):
    """Abstract base class for car factories."""
    
    @abstractmethod
    def create_car(self):
        """
        Abstract factory method that subclasses must override.
        Returns a Car object.
        """
        pass


# ============================================================================
# STEP 4: Implement Concrete Factories
# ============================================================================

class SedanFactory(CarFactory):
    """Factory for creating Sedan objects."""
    
    def create_car(self):
        """Creates and returns a Sedan object."""
        return Sedan()


class SUVFactory(CarFactory):
    """Factory for creating SUV objects."""
    
    def create_car(self):
        """Creates and returns an SUV object."""
        return SUV()


class HatchbackFactory(CarFactory):
    """Factory for creating Hatchback objects."""
    
    def create_car(self):
        """Creates and returns a Hatchback object."""
        return Hatchback()


# ============================================================================
# STEP 5: Demonstrate the Factory Method Pattern
# ============================================================================

def main():
    """Main program demonstrating the Factory Method Pattern."""
    
    print("=" * 70)
    print("Factory Method Pattern: Car Creation System")
    print("=" * 70)
    print()
    
    # Create factories (client doesn't know the concrete car classes)
    factories = [
        SedanFactory(),
        SUVFactory(),
        HatchbackFactory()
    ]
    
    # Use factories to create cars without knowing their concrete classes
    print("Creating different types of cars using factories:\n")
    
    for factory in factories:
        # The factory method creates the appropriate car
        car = factory.create_car()
        
        # Client code only depends on the abstract Car interface
        print(car.drive())
        print()
    
    print("=" * 70)
    print("Benefits of Factory Method Pattern:")
    print("=" * 70)
    print("""
1. Encapsulation: Object creation logic is encapsulated in factories.
2. Loose Coupling: Client code depends only on abstractions (Car, CarFactory).
3. Flexibility: New car types can be added without modifying existing code.
4. Single Responsibility: Each factory is responsible for creating one type.
5. Open/Closed Principle: Open for extension, closed for modification.
    """)
    
    print("\nExample of extensibility - Creating cars dynamically:\n")
    
    # Simulating dynamic factory selection based on user input
    def get_car(car_type):
        """Helper function to get the appropriate factory based on type."""
        factories_map = {
            'sedan': SedanFactory(),
            'suv': SUVFactory(),
            'hatchback': HatchbackFactory()
        }
        
        factory = factories_map.get(car_type.lower())
        if factory:
            return factory.create_car()
        else:
            raise ValueError(f"Unknown car type: {car_type}")
    
    # Dynamic car creation
    car_types = ['sedan', 'suv', 'hatchback', 'suv']
    
    for car_type in car_types:
        car = get_car(car_type)
        print(f"Created a {car_type}: {car.drive()}")
        print()


if __name__ == "__main__":
    main()
