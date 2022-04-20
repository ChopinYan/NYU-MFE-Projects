#pragma once
#include "MCModel02.h"
namespace fre {
	class PathDepOption
	{
	protected:
		double Price;
		double K, T;
		int m;
		Vector delta;
	public:
		PathDepOption(double T_, double K_, int m_, Vector delta_) :
			Price(0.0), delta(delta_), T(T_), K(K_), m(m_) {}
		virtual ~PathDepOption() {}
		virtual double Payoff(const SamplePath& S) const = 0;  // pure virtual, inherited by all derived classes
		double PriceByMC(MCModel& Model, long N, double epsilon);
		double GetPrice() { return Price; }
		Vector GetDelta() { return delta; }
	};
	class ArthmAsianCall : public PathDepOption
	{
	public:
		ArthmAsianCall(double T_, double K_, int m_, Vector delta_) : PathDepOption(T_, K_, m_, delta_) {}
		double Payoff(const SamplePath& S) const;
	};
	void Rescale(SamplePath& S, int d, double x);
}