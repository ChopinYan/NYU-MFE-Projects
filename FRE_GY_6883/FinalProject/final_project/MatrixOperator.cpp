// File name: MatrixOperator.cpp
// Author: Team 2
// Class: FRE-GY 6883
// Assignment Number: Final Project
// Honor statement: We have neither given nor received help on this assignment

#include "MatrixOperator.h"
#include <cmath>
using namespace std;


Vector operator*(const double& a, const Vector& V)
{
	int d = (int)V.size();
	Vector U(d);
	for (int j = 0; j < d; j++) U[j] = a * V[j];
	return U;
}
Vector operator*(const Vector& V, const Vector& W)
{
	int d = (int)V.size();
	Vector U(d);
	for (int j = 0; j < d; j++) U[j] = V[j] * W[j];
	return U;
}
Vector operator+(const Vector& V, const Vector& W)
{
	int d = (int)V.size();
	Vector U(d);
	for (int j = 0; j < d; j++) { U[j] = V[j] + W[j]; }
	return U;
}

Vector operator+(const double& a, const Vector& V)
{
	int d = (int)V.size();
	Vector U(d);
	for (int j = 0; j < d; j++) U[j] = a + V[j];
	return U;
}

Matrix operator+(const Matrix& C, const Matrix& D)
{
	int m = (int)C.size();
	Matrix W(m);
	for (int i = 0; i < m; i++)
	{
			W[i] = C[i] + D[i];
	}
	return W;
}
Matrix operator*(const double& a, const Matrix& C) 
{
	int m = (int)C.size();
	Matrix W(m);
	for (int i = 0; i < m; i++) W[i] = a * C[i];
	return W;
}

Matrix operator^(const Matrix& C, const double& a)
{
	int m = (int)C.size();
	int n = C[0].size();
	Matrix W(m, Vector(n));
	for (int i = 0; i < m; i++)
	{
		for (int j = 0; j < n; j++)
		{
			W[i][j] = pow(C[i][j], a);
		}
	}
	return W;
}