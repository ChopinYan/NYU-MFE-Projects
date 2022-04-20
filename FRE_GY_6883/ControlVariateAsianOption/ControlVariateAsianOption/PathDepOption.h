// There will be three derived classes for PathDepOption
// 1. ArthmAsianCall
// 2. GmtrAsianCall
// 3. DifferenceOfOptions

#pragma once
#include "MCModel.h"
namespace fre {
	class PathDepOption
	{
	protected:
		double Price, PricingError, delta, gamma;
		double K, T;
		int m;
	public:
		PathDepOption(double T_, double K_, int m_) :
			Price(0.0), PricingError(0.0), delta(0.0), gamma(0.0), T(T_), K(K_), m(m_) {}
		virtual ~PathDepOption() {}
		virtual double Payoff(const SamplePath& S) const = 0;  // pure virtual, inherited by all derived classes
		double PriceByMC(const MCModel& Model, long N, double epsilon);
		// for diff by Monte Carlo
		double PriceByVarRedMC(const MCModel& Model, long N, PathDepOption& CVOption, double epsilon);
		// regular virtual, only inherited by GmtrAsianCall (if pure virtual Arthm and Diff will be abstract and cannot be instantized)
		virtual double PriceByBSFormula(const MCModel& Model) { return 0.0; }  
		double GetT() { return T; }
		double GetPrice() { return Price; }
		double GetPricingError() { return PricingError; }
		double GetDelta() { return delta; }
		double GetGamma() { return gamma; }
	};
	class DifferenceOfOptions : public PathDepOption
	{
	private:
		PathDepOption* Ptr1;
		PathDepOption* Ptr2;
	public:
		DifferenceOfOptions(double T_, double K_, int m_, PathDepOption* Ptr1_, PathDepOption* Ptr2_):
			PathDepOption(T_, K_, m_), Ptr1(Ptr1_), Ptr2(Ptr2_) {}
		double Payoff(const SamplePath& S) const  // override
		{
			return Ptr1->Payoff(S) - Ptr2->Payoff(S);  // difference between Arthm and Gmtr
		}
	};
	class ArthmAsianCall : public PathDepOption
	{
	public:
		ArthmAsianCall(double T_, double K_, int m_) : PathDepOption(T_, K_, m_) {}
		double Payoff(const SamplePath& S) const;
	};
	void Rescale(SamplePath& S, double x);
}
