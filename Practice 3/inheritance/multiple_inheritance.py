# Example 1: Multiple inheritance with FlyingCar inheriting from Car and Airplane
class Car:
    def drive(self):
        return "Driving"

class Airplane:
    def fly(self):
        return "Flying"

class FlyingCar(Car, Airplane):
    pass

fc = FlyingCar()
print(fc.drive())  # Output: Driving
print(fc.fly())    # Output: Flying

# Example 2: Multiple inheritance with StudentAthlete inheriting from Student and Athlete
class Student:
    def study(self):
        return "Studying"

class Athlete:
    def play(self):
        return "Playing sports"

class StudentAthlete(Student, Athlete):
    pass

sa = StudentAthlete()
print(sa.study())  # Output: Studying
print(sa.play())   # Output: Playing sports

# Example 3: Multiple inheritance with RobotDog inheriting from Robot and Dog
class Robot:
    def charge(self):
        return "Charging"

class Dog:
    def bark(self):
        return "Barking"

class RobotDog(Robot, Dog):
    pass

rd = RobotDog()
print(rd.charge())  # Output: Charging
print(rd.bark())    # Output: Barking

# Example 4: Multiple inheritance with AmphibiousVehicle inheriting from Boat and Car
class Boat:
    def sail(self):
        return "Sailing"

class Car:
    def drive(self):
        return "Driving"

class AmphibiousVehicle(Boat, Car):
    pass

av = AmphibiousVehicle()
print(av.sail())   # Output: Sailing
print(av.drive())  # Output: Driving

# Example 5: Multiple inheritance with SmartPhone inheriting from Phone and Computer
class Phone:
    def call(self):
        return "Calling"

class Computer:
    def compute(self):
        return "Computing"

class SmartPhone(Phone, Computer):
    pass

sp = SmartPhone()
print(sp.call())     # Output: Calling
print(sp.compute())  # Output: Computing