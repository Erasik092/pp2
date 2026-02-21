numbers = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)

numbers = [1, 2, 3, 4, 5, 6, 7, 8]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
one_digit_numbers = list(filter(lambda x: x < 10, numbers))
print(one_digit_numbers)

numbers = [1, 2, 3, 4, 5, 6, 7, 8]
power_of_two = list(filter(lambda n: (n & (n - 1)) == 0 and n != 0, numbers))
print(power_of_two)

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
two_digit_numbers = list(filter(lambda x: x >= 10, numbers))
print(two_digit_numbers)