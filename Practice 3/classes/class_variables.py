# Example 1: Basic class variable
class Person:
    species = "Human"

    def __init__(self, name):
        self.name = name

person1 = Person("Alice")
person2 = Person("Bob")
print(f"{person1.name} is {person1.species}")
print(f"{person2.name} is {person2.species}")

# Example 2: Class variable as counter
class Student:
    count = 0

    def __init__(self, name):
        self.name = name
        Student.count += 1

student1 = Student("John")
student2 = Student("Jane")
print(f"Total students: {Student.count}")

# Example 3: Class variable modified by class method
class Car:
    total_cars = 0

    def __init__(self, make):
        self.make = make
        Car.total_cars += 1
    @classmethod
    def get_total(cls):
        return cls.total_cars

car1 = Car("Toyota")
car2 = Car("Honda")
print(f"Total cars: {Car.get_total()}")

# Example 4: Class variable vs instance variable
class Dog:
    species = "Canine"  # Class variable

    def __init__(self, name):
        self.name = name  # Instance variable

dog1 = Dog("Buddy")
dog2 = Dog("Max")
print(f"{dog1.name} is a {dog1.species}")
print(f"{dog2.name} is a {dog2.species}")

# Example 5: Modifying class variable affects all instances
class Circle:
    pi = 3.14  # Class variable

    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return Circle.pi * self.radius ** 2

circle1 = Circle(5)
circle2 = Circle(10)
print(f"Circle1 area: {circle1.area()}")
print(f"Circle2 area: {circle2.area()}")

# Modifying class variable
Circle.pi = 3.14159
print(f"After change - Circle1 area: {circle1.area()}")