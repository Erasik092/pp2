def get_greeting():
  return "Hello from a function"
message = get_greeting()
print(message) 

def fahrenheit_to_celsius(fahrenheit):
  return (fahrenheit - 32) * 5 / 9
print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50)) 

def celsius_to_fahrenheit(celsius):
  return celsius * 9 / 5 + 32

def calculate_area(radius):
  import math
  return math.pi * radius ** 2

def calculate_area(side_length):
  return side_length ** 2

def myfunc(n): 
    return lambda a : a * n
mydoubler = myfunc(2)
print(mydoubler(11))