#!/usr/bin/env python3

#Given a word string, check if it is a palindrome (sequence of characters which reads same backward as forward, such as “kayak”, “level”).

def check_palindrome(s):
	n=len(s)
	for i in range(0,n//2):
		if s[i]!=s[n-1-i]:
			return False
	return True
A="shahehfndfjvn"
print(check_palindrome(A))
B="ababababababa"
print(check_palindrome(B))
C="acca"
print(check_palindrome(C))
	