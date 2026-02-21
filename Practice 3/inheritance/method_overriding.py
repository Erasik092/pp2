# Example 1: Method overriding with Animal and Dog
class Animal:
    def speak(self):
        return "Animal speaks"

class Dog(Animal):
    def speak(self):
        return "Woof!"

dog = Dog()
print(dog.speak())  # Output: Woof!

# Example 2: Method overriding with Vehicle and Car
class Vehicle:
    def move(self):
        return "Vehicle moves"

class Car(Vehicle):
    def move(self):
        return "Car drives"

car = Car()
print(car.move())  # Output: Car drives

# Example 3: Method overriding with Person and Student
class Person:
    def introduce(self):
        return "I am a person"

class Student(Person):
    def introduce(self):
        return "I am a student"

student = Student()
print(student.introduce())  # Output: I am a student

# Example 4: Method overriding with Shape and Circle
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

# Example 5: Method overriding with Appliance and WashingMachine
class Appliance:
    def power_on(self):
        return "Appliance is on"

class WashingMachine(Appliance):
    def power_on(self):
        return "Washing machine is spinning"

wm = WashingMachine()
print(wm.power_on())  # Output: Washing machine is spinning