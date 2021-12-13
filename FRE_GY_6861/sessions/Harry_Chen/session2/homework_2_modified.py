import numpy as np
import math


# 1 Swap 2 numbers without creating another variable
def swap(num_1, num_2):
    print('Before swapping:')
    print('A = ', num_1, 'and B= ', num_2)
    num_1, num_2 = num_2, num_1
    print('After swapping:')
    print('A = ', num_1, 'and B= ', num_2)


swap(14, 41)
print('--------------------------')


# 2  Program to check if a string is palindrome or not
def palindrome_identifier(input_string):
    rev_str = reversed(input_string)
    if list(input_string) == list(rev_str):
        print(input_string, 'is a palindrome.')
    else:
        print(input_string, 'is not a palindrome.')


palindrome_identifier('level')
print('--------------------------')


# 3  Fizz Buzz Game
def fizzbuzz():
    for fizzbuzz in range(1, 101):
        if fizzbuzz % 15 == 0:
            print("FizzBuzz")
            continue

        elif fizzbuzz % 3 == 0:
            print("Fizz")
            continue

        elif fizzbuzz % 5 == 0:
            print("Buzz")
            continue

        print(fizzbuzz)


fizzbuzz()
print('--------------------------')


# 4 Function that distinguish prime number
def next_prime(input):
    def isPrime(n):
        if (n <= 1):
            return 0
        if (n <= 3):
            return 1
        if (n % 2 == 0 or n % 3 == 0):
            return 0
        for i in range(5, int(math.sqrt(n) + 1), 6):
            if (n % i == 0 or n % (i + 2) == 0):
                return 0
        return 1

    # Function to return the smallest prime number over N
    def nextPrime(N):
        if (N <= 1):
            return 2
        prime = N
        found = 0

        while (not found):
            prime += 1

            if (isPrime(prime) == 1):
                found = 1

        return prime

    print(nextPrime(input))


next_prime(220)
