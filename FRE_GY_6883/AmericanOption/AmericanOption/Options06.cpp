#include <iostream>
#include <cmath>
#include <vector>
#include "Options06.h"
#include "BInomialTreeModel02.h"
using namespace std;
namespace fre {
	Option::~Option() {}
	double Call::PayOff(double z) const
	{
		if (z > K) return z - K;
		return 0.0;
	}
	double Put::PayOff(double z) const
	{
		if (z < K) return K - z;
		return 0.0;
	}
	double OptionCalculation::PriceByCRR(const BinomialTreeModel& Model)
	{
		double q = Model.RiskNeutralProb();
		int N = pOption->GetN();
		vector<double>Price(N + 1);
		for (int i = 0; i <= N; i++)
		{
			Price[i] = pOption->PayOff(Model.CalculateAssetPrice(N, i));
		}
		for (int n = N - 1; n >= 0; n--)
		{
			for (int i = 0; i <= n; i++)
			{
				Price[i] = (q * Price[i + 1] + (1 - q) * Price[i]) / Model.GetR();
			}
		}
		return Price[0];
	}
	double OptionCalculation::PriceBySnell(const BinomialTreeModel& Model)
	{
		double q = Model.RiskNeutralProb();
		int N = pOption->GetN();
		vector<double>Price(N + 1);
		double ContVal = 0;
		for (int i = 0; i <= N; i++)
		{
			Price[i] = pOption->PayOff(Model.CalculateAssetPrice(N, i));
		}
		for (int n = N - 1; n >= 0; n--)
		{
			for (int i = 0; i <= n; i++)
			{
				ContVal = (q * Price[i + 1] + (1 - q) * Price[i]) / Model.GetR();
				Price[i] = pOption->PayOff(Model.CalculateAssetPrice(n, i));
				if (ContVal > Price[i]) Price[i] = ContVal;
			}
		}
		return Price[0];
	}
	int GetInputData(int& N, double& K)
	{
		cout << "Enter steps to expiration N: "; cin >> N;
		cout << "Enter strike price K: "; cin >> K;
		cout << endl;
		return 0;
	}
}