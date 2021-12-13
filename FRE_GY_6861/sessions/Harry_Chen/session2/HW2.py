#!/usr/bin/env python
# coding: utf-8

# # Ex.1

# In[1]:


import numpy as np


# In[2]:


A = 14
B = 41


# In[3]:


print('Before swapping:')
print('A = ',A,' and B = ',B)


# In[4]:


#Swap A and B
A,B = B,A
print('After swapping:')
print('A = ', A, ' and B = ',B)


# # Ex.2

# In[5]:


# Program to check if a string is palindrome or not
print('Please type in your word:')
x=input()

my_str = x

# reverse the string
rev_str = reversed(my_str)

# check if the string is equal to its reverse
if list(my_str) == list(rev_str):
    print(my_str,"is a palindrome.")
else:
    print(my_str,"is not a palindrome.")


# # Ex.3

# In[6]:


for fizzbuzz in range(1,101):
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


# # Ex.4

# In[7]:


import math

#Function that distinguish prime number
def isPrime(n):
    if(n <=1 ):
        return 0
    if(n <= 3):
        return 1
    if(n%2 == 0 or n%3 == 0):
        return 0
    for i in range(5, int(math.sqrt(n)+1), 6):
        if(n%i == 0 or n%(i+2) == 0):
            return 0
    return 1

#Function to return the smallest prime number over N
def nextPrime(N):
    if(N <= 1):
        return 2
    prime = N
    found = 0
    
    while(not found):
        prime +=1
        
        if(isPrime(prime) == 1):
            found = 1
            
    return prime

print('Please type an integer: ')
x=int(input())
print(nextPrime(x))


# In[ ]:





# In[ ]:




