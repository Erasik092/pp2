def my_function(fname):
  print(fname + " Refsnes")
my_function("Emil")
my_function("Tobias")
my_function("Linus") 

def my_function(fname, lname):
  print(fname + " " + lname)
my_function("Emil", "Refsnes") 

def my_function(name = "friend"):
  print("Hello", name)
my_function("Emil")
my_function("Tobias")
my_function()
my_function("Linus") 

def my_function(country = "Norway"):
  print("I am from", country)
my_function("Sweden")
my_function("India")
my_function()
my_function("Brazil") 

def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)
my_function(animal = "dog", name = "Buddy") 

def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)
my_function("dog", "Buddy") 

def my_function(fruits):
  for fruit in fruits:
    print(fruit)
my_fruits = ["apple", "banana", "cherry"]
my_function(my_fruits) 

def my_function():
  return ["apple", "banana", "cherry"]
fruits = my_function()
print(fruits[0])
print(fruits[1])
print(fruits[2]) 