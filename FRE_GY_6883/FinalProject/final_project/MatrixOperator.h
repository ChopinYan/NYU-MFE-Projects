// File name: MatrixOperator.h
// Author: Team 2
// Class: FRE-GY 6883
// Assignment Number: Final Project
// Honor statement: We have neither given nor received help on this assignment

#pragma once
#include <vector>
#include <iostream>
using namespace std;

typedef vector<double> Vector;
typedef vector<Vector> Matrix;

Vector operator*(const double& a, const Vector& V);
Vector operator*(const Vector& V, const Vector& W);
Vector operator+(const double& a, const Vector& V);
Vector operator+(const Vector& V, const Vector& W);
Matrix operator+(const Matrix& C, const Matrix& D);
Matrix operator*(const double& a, const Matrix& C);
Matrix operator^(const Matrix& C, const double& a);
