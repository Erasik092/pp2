# Example 1: Using super() to call parent method in Dog
class Animal:
    def speak(self):
        return "Animal speaks"

class Dog(Animal):
    def speak(self):
        parent_speak = super().speak()
        return parent_speak + " and Woof!"

dog = Dog()
print(dog.speak())  # Output: Animal speaks and Woof!

# Example 2: Using super() in Car to extend parent method
class Vehicle:
    def move(self):
        return "Vehicle moves"

class Car(Vehicle):
    def move(self):
        parent_move = super().move()
        return parent_move + " on roads"

car = Car()
print(car.move())  # Output: Vehicle moves on roads

# Example 3: Using super() in Student to call parent introduce
class Person:
    def introduce(self):
        return "I am a person"

class Student(Person):
    def introduce(self):
        parent_intro = super().introduce()
        return parent_intro + " and a student"

student = Student()
print(student.introduce())  # Output: I am a person and a student

# Example 4: Using super() in Circle to call parent area (though parent returns 0)
class Shape:
    def area(self):
        return 0

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        # Parent area is 0, but we can still call it
        parent_area = super().area()
        return parent_area + 3.14 * self.radius ** 2

circle = Circle(5)
print(circle.area())  # Output: 78.5

# Example 5: Using super() in WashingMachine to extend power_on
class Appliance:
    def power_on(self):
        return "Appliance is on"

class WashingMachine(Appliance):
    def power_on(self):
        parent_on = super().power_on()
        return parent_on + " and washing"

wm = WashingMachine()
print(wm.power_on())  # Output: Appliance is on and washing