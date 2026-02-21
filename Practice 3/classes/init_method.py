# Example 1: Basic __init__ method
class Person:
    def __init__(self, name):
        self.name = name

person = Person("Alice")
print(f"Person name: {person.name}")

# Example 2: __init__ with multiple parameters
class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

car = Car("Toyota", "Corolla", 2020)
print(f"Car: {car.year} {car.make} {car.model}")

# Example 3: __init__ with default parameters
class Book:
    def __init__(self, title, author, pages=100):
        self.title = title
        self.author = author
        self.pages = pages

book1 = Book("1984", "Orwell")
book2 = Book("Harry Potter", "Rowling", 500)
print(f"{book1.title} has {book1.pages} pages")
print(f"{book2.title} has {book2.pages} pages")

# Example 4: __init__ calling other methods
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.area_value = self.calculate_area()

    def calculate_area(self):
        return self.width * self.height

rect = Rectangle(10, 5)
print(f"Rectangle area: {rect.area_value}")

# Example 5: __init__ with validation
class Student:
    def __init__(self, name, age):
        if age < 0:
            raise ValueError("Age cannot be negative")
        self.name = name
        self.age = age

student = Student("John", 20)
print(f"Student: {student.name}, Age: {student.age}")

# This would raise an error: student2 = Student("Jane", -5)