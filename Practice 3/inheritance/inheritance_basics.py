# Example 1: Basic inheritance with Animal and Dog
class Animal:
    def speak(self):
        return "Animal speaks"

class Dog(Animal):
    pass

dog = Dog()
print(dog.speak())  # Output: Animal speaks

# Example 2: Inheritance with Vehicle and Car
class Vehicle:
    def move(self):
        return "Vehicle moves"

class Car(Vehicle):
    pass

car = Car()
print(car.move())  # Output: Vehicle moves

# Example 3: Inheritance with Person and Student
class Person:
    def introduce(self):
        return "I am a person"

class Student(Person):
    pass

student = Student()
print(student.introduce())  # Output: I am a person

# Example 4: Inheritance with Shape and Circle
class Shape:
    def area(self):
        return 0

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2

circle = Circle(5)
print(circle.area())  # Output: 78.5

# Example 5: Inheritance with Appliance and WashingMachine
class Appliance:
    def power_on(self):
        return "Appliance is on"

class WashingMachine(Appliance):
    pass

wm = WashingMachine()
print(wm.power_on())  # Output: Appliance is on