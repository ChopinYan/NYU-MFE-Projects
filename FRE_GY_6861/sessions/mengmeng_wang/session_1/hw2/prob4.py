#!/usr/bin/env python3

#Given an arbitrary integer x, implement a snippet that returns the next biggest prime number (a whole number greater than 1 whose only factors are 1 and itself)
def if_prime(x):
	i=2
	while(i*i<=x):
		if x%i==0:
			return False
		i+=1
	return True
a=15  # can define your own number here
x=a+1
while(1):
	if(if_prime(x)):
		print(x)
		break
	else:
		x+=1