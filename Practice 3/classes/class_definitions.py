# Example 1: Basic class definition
class Person:
    pass

person = Person()
print("Person object created")

# Example 2: Class with attributes
class Car:
    def __init__(self, make, model):
        self.make = make
        self.model = model

car = Car("Toyota", "Corolla")
print(f"Car: {car.make} {car.model}")

# Example 3: Class with methods
class Dog:
    def bark(self):
        return "Woof!"

dog = Dog()
print(dog.bark())

# Example 4: Class with both attributes and methods
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

rect = Rectangle(10, 5)
print(f"Area: {rect.area()}")

# Example 5: Empty class for later extension
class Animal:
    pass

animal = Animal()
print("Animal object created")