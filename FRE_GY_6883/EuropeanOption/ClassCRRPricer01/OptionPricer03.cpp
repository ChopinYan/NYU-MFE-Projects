#include "BinomialTreeModel02.h"
#include "Option03.h"
#include <iostream>
#include <iomanip>
using namespace std;
using namespace fre;

int main()
{
	int N = 8;
	double U = 1.15125, D = 0.86862, R = 1.00545;
	double S0 = 106.00, K = 100.00;
	BinomialTreeModel BinModel(S0, U, D, R);
	if (BinModel.ValidateInputData() != 0) return -1;

	double* OptionPrice;
	OptionPrice = PriceByCRR(BinModel, N, K, EuroCallPayoff);
	cout << "European Call option price = " << fixed << setprecision(2)
		<< OptionPrice[0] << endl;
	delete [] OptionPrice;

	OptionPrice = PriceByCRR(BinModel, N, K, EuroPutPayoff);
	cout << "European Put option price = " << fixed << setprecision(2)
		<< OptionPrice[0] << endl;
	delete [] OptionPrice;
	
	OptionPrice = NULL;

	return 0;
}
