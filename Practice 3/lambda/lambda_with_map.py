numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)

numbers = [1, 2, 3, 4, 5]
tripled = list(map(lambda x: x * 3, numbers))
print(tripled)

numbers = [1, 2, 3, 4, 5]
double_string = list(map(lambda x: str(x * 2), numbers))
print(double_string)

numbers = [1, 2, 3, 4, 5]
float_func = list(map(lambda x: float(x * 2), numbers))
print(float_func)

numbers = [1, 2, 3, 4, 5]
divide = list(map(lambda x: x / 2, numbers))
print(divide)

def function(n):
  return lambda a : a / n
divided_numbers = list(map(int, input().split()))
n = int(input())
divider = function(n)
result = list(map(divider, divided_numbers))