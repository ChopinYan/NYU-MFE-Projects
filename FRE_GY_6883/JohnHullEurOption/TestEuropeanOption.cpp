// TestEuropeanOption.cpp
// Test program for the exact solutions of European options.
// (C) Datasim Component Technology BV 2003-2006
//

#include "EuropeanOption.hpp"
#include <iostream>

int main()
{
	// Call option on a stock
	EuropeanOption callOption;
	cout << "Call option on a stock: " << callOption.Price() << endl;
	cout << "Delta on a call option: " << callOption.Delta() << endl;

	// Put option on a stock index
	EuropeanOption indexOption;
	indexOption.optType = "P";
	indexOption.U = 100.0;
	indexOption.K = 95.0;
	indexOption.T = 0.5;
	indexOption.r = 0.10;
	indexOption.sig = 0.20;

	double q = 0.05;		// Dividend yield
	indexOption.b = indexOption.r - q;

	cout << "Put option on an index: " << indexOption.Price() << endl;
	cout << "Delta on a put option: " << indexOption.Delta() << endl;

	return 0;
}

