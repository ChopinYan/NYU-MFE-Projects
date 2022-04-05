#include "BInomialTreeModel02.h"
#include "Options06.h"
#include <iostream>
#include <iomanip>
using namespace std;
using namespace fre;


int main()
{
	BinomialTreeModel Model;
	Model.GetInputData();
	if (Model.ValidateInputData() != 0)
		return -1;

	double K; int N;
	cout << "Enter strike price and expiration steps: " << endl;
	GetInputData(N, K);
	
	Call call(N, K);
	OptionCalculation callCalculation(&call);
	cout << "European Call Option Price = " << fixed
		<< setprecision(2) << callCalculation.PriceByCRR(Model) << endl;

	Put put(N, K);
	OptionCalculation putCalculation(&put);
	cout << "European Put Option Price = " << fixed
		<< setprecision(2) << putCalculation.PriceByCRR(Model) << endl;

	cout << "American Call Option Price = " << fixed
		<< setprecision(2) << callCalculation.PriceBySnell(Model) << endl;

	cout << "American Put Option Price = " << fixed
		<< setprecision(2) << putCalculation.PriceBySnell(Model) << endl;

	return 0;
}
