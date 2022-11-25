import math


def swap(a, b):
    """
    Given two numbers (arbitrary chosen), A = 14, B = 41,
    exchange values without creating another variable.
    :param a: an integer
    :param b: an integer
    :return: exchanged integers
    """
    return b, a


def if_palindrome(string):
    """
    Given a word string, check if it is a palindrome
    (sequence of characters which reads same backward as forward,
    such as “kayak”, “level”).
    :param string: a string
    :return: boolean (whether it is a palindrome or not)
    """
    return string == string[::-1]


def print_fizz_buzz(num):
    """
    Print integers from 1 to 100 (inclusive),
    using following rules:
    for multiples of 3, print “Fizz” (instead of the number);
    for multiples of 5, print “Buzz” (instead of the number);
    for multiples of both 3 and 5, print “FizzBuzz” (instead of the number)
    :param num: length of interation of numbers
    :return:
    """
    for i in range(1, num+1):
        if (i % 3) == 0:
            print("Fizz")
        elif (i % 5) == 0:
            print("Buzz")
        elif ((i % 3) == 0) and ((i % 5) == 0):
            print("FizzBuzz")
        else:
            print(i)
    pass


def if_prime(n):
    """
    Given an integer, determine whether it is a prime or not
    :param n: a given integer
    :return: boolean, whether it is a prime or not
    """
    for i in range(2, int(math.sqrt(n)) + 1):
        if (n % i) == 0:
            return False
    return True


def next_prime(x):
    """
    Given an arbitrary integer x, implement a snippet that returns the next biggest prime number
    (a whole number greater than 1 whose only factors are 1 and itself)
    :param x: a given integer
    :return: the next prime larger than x
    """
    next_biggest = x
    while True:
        next_biggest += 1
        if if_prime(next_biggest):
            return next_biggest


def main():
    """
    main function: run the test of all the functions
    :return:
    """
    # question 1
    a = 14
    b = 41
    a, b = swap(a, b)
    print(f"swapped variables {a} and {b}")

    # question 2
    m = "level"
    n = "kayak"
    print(f"Whether {m} is a palindrome: {if_palindrome(m)}")
    print(f"Whether {n} is a palindrome: {if_palindrome(n)}")

    # question 3
    print_fizz_buzz(100)

    # question 4
    number = 8
    print(f'next nearest prime for {number} is {next_prime(number)}')


if __name__ == "__main__":
    main()
