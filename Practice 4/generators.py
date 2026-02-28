def squares_up_to_n(n):
    """Generator that yields squares of numbers from 0 to n"""
    for i in range(n + 1):
        yield i ** 2


def even_numbers(n):
    """Generator that yields even numbers from 0 to n"""
    for i in range(0, n + 1, 2):
        yield i


def print_even_numbers():
    n = int(input("Enter a number n: "))
    even_nums = even_numbers(n)
    result = ", ".join(str(num) for num in even_nums)
    print(result)


def divisible_by_3_and_4(n):
    """Generator that yields numbers divisible by both 3 and 4 between 0 and n"""
    for i in range(0, n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


def squares(a, b):
    """Generator that yields the square of all numbers from a to b"""
    for i in range(a, b + 1):
        yield i ** 2


def countdown(n):
    """Generator that yields numbers from n down to 0"""
    while n >= 0:
        yield n
        n -= 1