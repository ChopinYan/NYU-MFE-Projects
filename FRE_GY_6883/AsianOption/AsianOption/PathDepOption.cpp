#include "PathDepOption.h"
#include <cmath>
namespace fre {
	double PathDepOption::PriceByMC(const MCModel& Model, long N, double epsilon)
	{
		double H = 0.0, Hsq = 0.0, HepsPos = 0.0, HepsNeg = 0.0;
		SamplePath S(m);
		for (long i = 0; i < N; i++)
		{
			Model.GenerateSamplePath(T, m, S);
			// payoff for asian option
			H = (i * H + Payoff(S)) / (i + 1.0);
			// E[H(T)**2] for stdev
			Hsq = (i * Hsq + pow(Payoff(S), 2.0)) / (i + 1.0);
			// rescale 1 + epsilon for delta
			Rescale(S, 1.0 + epsilon);
			HepsPos = (i * HepsPos + Payoff(S)) / (i + 1.0);
			// rescale back and rescale 1 - epsilon for gamma
			Rescale(S, (1.0 - epsilon) / (1.0 + epsilon));
			HepsNeg = (i * HepsNeg + Payoff(S)) / (i + 1.0);
		}
		Price = exp(-Model.GetR() * T) * H;
		PricingError = exp(-Model.GetR() * T) * sqrt(Hsq - H * H) / sqrt(N - 1.0);
		delta = exp(-Model.GetR() * T) * (HepsPos - H) / (Model.GetS0() * epsilon);
		gamma = exp(-Model.GetR() * T) * (HepsPos - 2 * H + HepsNeg) / pow((Model.GetS0() * epsilon), 2);
		return Price;
	}
	double ArthmAsianCall::Payoff(const SamplePath& S) const
	{
		double Ave = 0.0;
		for (int k = 0; k < m; k++) Ave = (k * Ave + S[k]) / (k + 1.0);
		if (Ave < K) return 0.0;
		return Ave - K;
	}
	void Rescale(SamplePath& S, double x)
	{
		int m = S.size();
		for (int j = 0; j < m; j++) S[j] = x * S[j];
	}
}