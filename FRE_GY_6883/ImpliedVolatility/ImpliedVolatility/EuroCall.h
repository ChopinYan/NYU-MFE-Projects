#pragma once
#include "NonlinearSolver02.h"
namespace fre {
	class EuroCall
	{
	private:
		double T, K;
	public:
		EuroCall(double T_, double K_): T(T_), K(K_) {}
		double d_plus(double S0, double sigma, double r);
		double d_minus(double S0, double sigma, double r);
		double PriceByBSFormula(double S0, double sigma, double r);
		double VegaByFormula(double S0, double sigma, double r);
	};
	class Intermediary : public EuroCall, public Function
	{
	private:
		double S0, r;
	public:
		Intermediary(double S0_, double r_, double T_, double K_)
			:EuroCall(T_, K_), S0(S0_), r(r_) {}
		double Value(double sigma);
		double Deriv(double sigma);
	};
}