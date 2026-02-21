# Example 1: Basic method in a class
class Person:
    def greet(self):
        return "Hello!"

person = Person()
print(person.greet())

# Example 2: Method with parameters
class Calculator:
    def add(self, a, b):
        return a + b

calc = Calculator()
print(calc.add(5, 3))

# Example 3: Method that modifies instance variable
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

counter = Counter()
counter.increment()
print(counter.count)

# Example 4: Method that returns a formatted string
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def info(self):
        return f"'{self.title}' by {self.author}"

book = Book("1984", "George Orwell")
print(book.info())

# Example 5: Method calling another method
class Robot:
    def __init__(self):
        self.battery = 100

    def work(self):
        self.battery -= 10
        return "Working..."

    def status(self):
        return f"Battery: {self.battery}%"

robot = Robot()
print(robot.work())
print(robot.status())