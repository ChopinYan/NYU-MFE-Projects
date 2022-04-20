#pragma once
#include "BinomialTreeModel02.h"

namespace fre {
	// input and display option data
	int GetInputData(int& N, double& K);

	// price Option
	double* PriceByCRR(const BinomialTreeModel& Model, int N, double K,
		double (*Payoff)(double z, double K));

	// compute European Call payoff
	double EuroCallPayoff(double z, double K);

	// compute European Put payoff
	double EuroPutPayoff(double z, double K);
}
